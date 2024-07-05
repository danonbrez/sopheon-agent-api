from notion_client import Client

class NotionClient:
    def __init__(self, api_key, database_id):
        self.client = Client(auth=api_key)
        self.database_id = database_id

    def fetch_pending_tasks(self):
        query = {
            "database_id": self.database_id,
            "filter": {
                "property": "Status",
                "select": {
                    "equals": "Pending"
                }
            }
        }
        return self.client.databases.query(**query)

# Usage:
# notion = NotionClient("your_notion_api_key", "your_notion_database_id")