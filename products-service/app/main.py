# File: products-service/app/main.py
from flask import Flask, request, jsonify
from bson import ObjectId
from .database import insert_product, find_product, update_product, delete_product, list_all_products

app = Flask(__name__)


def serialize_product(product):
    product["_id"] = str(product["_id"])
    return product


# Route to create a new product
@app.route('/products', methods=['POST'])
def create_product():
    product_data = request.get_json()
    if find_product(product_data['product_id']):
        return jsonify({"message": "Product already exists!"}), 400
    insert_product(product_data)
    return jsonify({"message": "Product created successfully!"}), 201


# Route to get a product by ID
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = find_product(product_id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404
    return jsonify(serialize_product(product)), 200


# Route to update a product by ID
@app.route('/products/<product_id>', methods=['PUT'])
def update_product_route(product_id):
    product_data = request.get_json()
    updated = update_product(product_id, product_data)
    if not updated:
        return jsonify({"message": "Product not found!"}), 404
    return jsonify({"message": "Product updated successfully!"}), 200


# Route to delete a product by ID
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    deleted = delete_product(product_id)
    if not deleted:
        return jsonify({"message": "Product not found!"}), 404
    return jsonify({"message": "Product deleted successfully!"}), 200


# Route to list all products
@app.route('/products', methods=['GET'])
def list_products():
    products = list_all_products()
    serialized_products = [serialize_product(product) for product in products]
    return jsonify(serialized_products), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
