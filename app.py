from flask import Flask, request, jsonify
import uuid
import requests
from dotenv import load_dotenv
import os
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLS)

app = Flask(__name__)

agents = {}

load_dotenv()
GPT40_API_URL = "https://api.gpt40.com/v1/query"  # Replace with actual GPT-40 API URL
GPT40_API_KEY = os.getenv("GPT40_API_KEY")

def call_gpt40_api(task):
    headers = {
        "Authorization": f"Bearer {GPT40_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": task}
    session = requests.Session()
    session.mount("https://", SSLAdapter())
    response = session.post(GPT40_API_URL, json=payload, headers=headers, verify=False)
    return response.json()

@app.route('/agents', methods=['POST'])
def spawn_agent():
    data = request.json
    agent_id = str(uuid.uuid4())
    agents[agent_id] = {
        'name': data['name'],
        'task': data['task'],
        'priority': data['priority'],
        'status': 'idle',
        'result': None
    }
    return jsonify({'agentId': agent_id}), 201

@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent_status(agent_id):
    agent = agents.get(agent_id)
    if agent:
        return jsonify({
            'agentId': agent_id,
            'status': agent['status'],
            'result': agent['result']
        }), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/agents/<agent_id>/terminate', methods=['POST'])
def terminate_agent(agent_id):
    agent = agents.pop(agent_id, None)
    if agent:
        return jsonify({'message': 'Agent terminated successfully'}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/agents/<agent_id>/tasks', methods=['POST'])
def assign_task(agent_id):
    agent = agents.get(agent_id)
    if agent:
        data = request.json
        agent['task'] = data['task']
        agent['priority'] = data['priority']
        agent['status'] = 'working'
        result = call_gpt40_api(agent['task'])
        agent['result'] = result['response']  # Adjust based on API response structure
        agent['status'] = 'completed'
        return jsonify({'message': 'Task assigned successfully'}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)