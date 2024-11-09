import os
from pymongo import MongoClient

# Get Mongo URI from environment variable
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
client = MongoClient(MONGO_URI)

db = client["ecom_platform"]

# Access the "inventory" collection
inventory_collection = db["inventory"]


# Function to add inventory
def add_inventory(inventory_data):
    inventory_collection.insert_one(inventory_data)


# Function to get inventory by product ID
def get_inventory(product_id):
    return inventory_collection.find_one({"product_id": product_id})


# Function to update inventory by product ID
def update_inventory(product_id, update_data):
    result = inventory_collection.update_one({"product_id": product_id}, {"$set": update_data})
    return result.modified_count > 0


# Function to delete inventory by product ID
def delete_inventory(product_id):
    result = inventory_collection.delete_one({"product_id": product_id})
    return result.deleted_count > 0


# Function to list all inventory
def list_inventory():
    return list(inventory_collection.find())