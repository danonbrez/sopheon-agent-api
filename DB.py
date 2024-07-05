from pymongo import MongoClient

class Database:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def create_collection(self, name):
        if name not in self.db.list_collection_names():
            self.db.create_collection(name)

    def get_collection(self, name):
        return self.db[name]

# Usage:
# db = Database("your-mongodb-connection-string", "sopheonDB")