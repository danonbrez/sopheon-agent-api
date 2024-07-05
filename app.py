from flask import Flask, request, jsonify
import uuid
from db import Database
from agent_manager import AgentManager
from notion_client import NotionClient
import openai
import os
import certifi
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, cert_reqs=ssl.CERT_REQUIRED,
            ca_certs=certifi.where())

app = Flask(__name__)

# Initialize environment variables
load_dotenv()

# Initialize database, Notion client, and agent manager
db = Database(os.getenv("MONGODB_URI"), os.getenv("MONGODB_DB_NAME"))
notion = NotionClient(os.getenv("NOTION_API_KEY"), os.getenv("NOTION_DATABASE_ID"))
agent_manager = AgentManager(db)

# Initialize OpenAI
openai.api_key = os.getenv("GPT40_API_KEY")
GPT40_API_URL = "https://api.gpt40.com/v1/query"

def call_gpt40_api(task):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    payload = {"query": task}
    session = requests.Session()
    session.mount("https://", SSLAdapter())
    try:
        response = session.post(GPT40_API_URL, json=payload, headers=headers, verify=certifi.where())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.SSLError as e:
        return {"error": "SSL error occurred", "details": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}

@app.route('/agents', methods=['POST'])
def spawn_agent():
    data = request.json
    if 'name' not in data or 'task' not in data or 'priority' not in data:
        return jsonify({'error': 'Missing required parameters: name, task, priority'}), 400
    agent_id = str(uuid.uuid4())
    agent_manager.create_agent(agent_id, data.get('capabilities', []))
    return jsonify({'agentId': agent_id}), 201

@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent_status(agent_id):
    agent = db.get_collection('agents').find_one({"agent_id": agent_id})
    if agent:
        return jsonify({
            'agentId': agent_id,
            'status': agent['status'],
            'result': agent.get('result', None)
        }), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/agents/<agent_id>/terminate', methods=['POST'])
def terminate_agent(agent_id):
    agent = db.get_collection('agents').find_one_and_delete({"agent_id": agent_id})
    if agent:
        return jsonify({'message': 'Agent terminated successfully'}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/agents/<agent_id>/tasks', methods=['POST'])
def assign_task(agent_id):
    data = request.json
    if 'task' not in data or 'priority' not in data:
        return jsonify({'error': 'Missing required parameters: task, priority'}), 400
    agent_manager.assign_task(agent_id, data['task_id'])
    result = call_gpt40_api(data['task'])
    agent_manager.calculate_efficiency(agent_id, result.get('success_rate', 0))
    agent_manager.log_to_blockchain(agent_id, data['task_id'], result.get('tokens_awarded', 0))
    return jsonify({'message': 'Task assigned successfully'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)