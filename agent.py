from uuid import uuid4
from gpt40_api import call_gpt40_api

agents = {}

def create_agent(name, task, priority):
    agent_id = str(uuid4())
    agents[agent_id] = {
        'name': name,
        'task': task,
        'priority': priority,
        'status': 'idle',
        'result': None
    }
    return agent_id

def assign_task(agent_id, task, priority):
    agent = agents.get(agent_id)
    if agent:
        agent['task'] = task
        agent['priority'] = priority
        agent['status'] = 'working'
        result = call_gpt40_api(agent['task'])
        agent['result'] = result.get('response', 'No response')
        agent['status'] = 'completed'
        return {"message": "Task assigned successfully"}
    else:
        return {"error": "Agent not found"}

def get_agent_status(agent_id):
    agent = agents.get(agent_id)
    if agent:
        return {
            "agentId": agent_id,
            "status": agent['status'],
            "result": agent['result']
        }
    else:
        return {"error": "Agent not found"}

def terminate_agent(agent_id):
    if agent_id in agents:
        del agents[agent_id]
        return {"message": "Agent terminated successfully"}
    else:
        return {"error": "Agent not found"}