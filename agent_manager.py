from datetime import datetime

class AgentManager:
    def __init__(self, db):
        self.db = db

    def create_agent(self, agent_id, capabilities):
        agent = {
            "agent_id": agent_id,
            "capabilities": capabilities,
            "efficiency_score": 0,
            "tokens": 100
        }
        self.db.get_collection('agents').insert_one(agent)

    def create_task(self, task_id, description):
        task = {
            "task_id": task_id,
            "description": description,
            "status": "pending",
            "timestamp": datetime.now()
        }
        self.db.get_collection('tasks').insert_one(task)

    def assign_task(self, agent_id, task_id):
        task = self.db.get_collection('tasks').find_one({"task_id": task_id})
        if task and task['status'] == 'pending':
            self.db.get_collection('agents').update_one(
                {"agent_id": agent_id},
                {"$set": {"status": "working", "current_task": task_id}}
            )
            self.db.get_collection('tasks').update_one(
                {"task_id": task_id},
                {"$set": {"status": "assigned"}}
            )

    def award_tokens(self, agent_id, tokens):
        self.db.get_collection('agents').update_one(
            {"agent_id": agent_id},
            {"$inc": {"tokens": tokens}}
        )

    def calculate_efficiency(self, agent_id, success_rate):
        self.db.get_collection('agents').update_one(
            {"agent_id": agent_id},
            {"$set": {"efficiency_score": success_rate}}
        )

    def log_to_blockchain(self, agent_id, task_id, tokens_awarded):
        block = {
            "agent_id": agent_id,
            "task_id": task_id,
            "tokens_awarded": tokens_awarded,
            "timestamp": datetime.now().isoformat()
        }
        self.db.get_collection('blockchain').insert_one(block)

# Usage:
# agent_manager = AgentManager(db)
# agent_manager.create_agent("agent123", ["math", "data_analysis"])
# agent_manager.create_task("task001", "Integrate GPT assistant with Notion and MongoDB")