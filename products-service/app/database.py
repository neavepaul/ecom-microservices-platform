import os
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["ecom_platform"]
products_collection = db["products"]


def insert_product(product_data):
    products_collection.insert_one(product_data)


def find_product(product_id):
    return products_collection.find_one({"product_id": product_id})


def update_product(product_id, product_data):
    result = products_collection.update_one({"product_id": product_id}, {"$set": product_data})
    return result.modified_count > 0


def delete_product(product_id):
    result = products_collection.delete_one({"product_id": product_id})
    return result.deleted_count > 0


def list_all_products():
    return list(products_collection.find())