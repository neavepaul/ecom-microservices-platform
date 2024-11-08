import os
from pymongo import MongoClient

# Get Mongo URI from environment variable
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Determine the database name based on whether we're in a test environment
db_name = "test_platform" if os.getenv("TESTING") == "true" else "ecom_platform"
db = client[db_name]

# Example: Accessing the "users" collection
users_collection = db["users"]

# Function to insert a user (just an example, modify for your logic)
def insert_user(user_data):
    users_collection.insert_one(user_data)

# Function to find a user by username (for authentication)
def find_user(username):
    return users_collection.find_one({"username": username})

