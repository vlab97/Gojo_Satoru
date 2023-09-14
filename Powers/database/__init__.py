from sys import exit as exiter

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from Powers import DB_NAME, DB_URI, LOGGER

try:
    Powers_db_client = MongoClient(DB_URI)
except PyMongoError as f:
    LOGGER.error(f"Error in Mongodb: {f}")
    exiter(1)
Powers_main_db = Powers_db_client[DB_NAME]


class MongoDB:
    """Class for interacting with Bot database."""

    def __init__(self, collection) -> None:
        self.collection = Powers_main_db[collection]

    # Insert one entry into collection
    def insert_one(self, document):
        if isinstance(document, str):
            document = document.split()
        result = self.collection.insert_one({"words": document})
        return repr(result.inserted_id)


    # Find one entry from collection
    def find_one(self, query):
        if isinstance(query, str):
            query = query.split()
        result = self.collection.find_one({"words": query})
        if result:
            return result
        return False

    # Find entries from collection
    def find_all(self, query=None):
        if query is None:
            query = {}
        elif isinstance(query, str):
            query = query.split()
        return list(self.collection.find({"words": {"$all": query}}))

    # Count entries from collection
    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    # Delete entry/entries from collection
    def delete_one(self, query):
        if isinstance(query, str):
            query = query.split()
        self.collection.delete_many({"words": {"$all": query}})
        return self.collection.count_documents({})



    # Replace one entry in collection
    def replace(self, query, new_data):
        if isinstance(query, str):
            query = query.split()
        old = self.collection.find_one({"words": query})
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, {"words": new_data})
        new = self.collection.find_one({"_id": _id})
        return old, new

    # Update one entry from collection
    def update(self, query, update):
        if isinstance(query, str):
            query = query.split()
        result = self.collection.update_one({"words": query}, {"$set": {"words": update}})
        new_document = self.collection.find_one({"words": query})
        return result.modified_count, new_document

    @staticmethod
    def close():
        return Powers_db_client.close()


def __connect_first():
    _ = MongoDB("test")
    LOGGER.info("Initialized Database!\n")


__connect_first()
