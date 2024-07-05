from flask import Flask, request, jsonify
from agent import create_agent, assign_task, get_agent_status, terminate_agent
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/agents', methods=['POST'])
def create_agent_route():
    data = request.get_json()
    name = data.get('name')
    task = data.get('task')
    priority = data.get('priority')
    agent_id = create_agent(name, task, priority)
    return jsonify({"agentId": agent_id})

@app.route('/agents/<agent_id>/tasks', methods=['POST'])
def assign_task_route(agent_id):
    data = request.get_json()
    task = data.get('task')
    priority = data.get('priority')
    response = assign_task(agent_id, task, priority)
    return jsonify(response)

@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent_status_route(agent_id):
    response = get_agent_status(agent_id)
    return jsonify(response)

@app.route('/agents/<agent_id>', methods=['DELETE'])
def terminate_agent_route(agent_id):
    response = terminate_agent(agent_id)
    return jsonify(response)

if __name__ == '__main__':
    app.run()