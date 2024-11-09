import os
from pymongo import MongoClient

# Get Mongo URI from environment variable
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
client = MongoClient(MONGO_URI)

db = client["ecom_platform"]

# Access the "orders" collection
orders_collection = db["orders"]


# Function to create a new order
def create_order(order_data):
    orders_collection.insert_one(order_data)


# Function to get an order by ID
def get_order(order_id):
    return orders_collection.find_one({"order_id": order_id})


# Function to update an order status by ID
def update_order_status(order_id, status):
    result = orders_collection.update_one({"order_id": order_id}, {"$set": {"status": status}})
    return result.modified_count > 0


# Function to delete an order by ID
def delete_order(order_id):
    result = orders_collection.delete_one({"order_id": order_id})
    return result.deleted_count > 0


# Function to list all orders
def list_orders():
    return list(orders_collection.find())