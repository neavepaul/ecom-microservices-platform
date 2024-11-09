from flask import Flask, request, jsonify
from bson import ObjectId
from .database import add_inventory, get_inventory, update_inventory, delete_inventory, list_inventory

app = Flask(__name__)


def serialize_inventory(inventory):
    inventory["_id"] = str(inventory["_id"])
    return inventory


# Route to add inventory for a product
@app.route('/inventory', methods=['POST'])
def create_inventory():
    inventory_data = request.get_json()
    if get_inventory(inventory_data['product_id']):
        return jsonify({"message": "Inventory for this product already exists!"}), 400
    add_inventory(inventory_data)
    return jsonify({"message": "Inventory added successfully!"}), 201


# Route to get inventory by product ID
@app.route('/inventory/<product_id>', methods=['GET'])
def get_inventory_route(product_id):
    inventory = get_inventory(product_id)
    if not inventory:
        return jsonify({"message": "Inventory not found!"}), 404
    return jsonify(serialize_inventory(inventory)), 200


# Route to update inventory by product ID
@app.route('/inventory/<product_id>', methods=['PUT'])
def update_inventory_route(product_id):
    inventory_data = request.get_json()
    updated = update_inventory(product_id, inventory_data)
    if not updated:
        return jsonify({"message": "Inventory not found!"}), 404
    return jsonify({"message": "Inventory updated successfully!"}), 200


# Route to delete inventory by product ID
@app.route('/inventory/<product_id>', methods=['DELETE'])
def delete_inventory_route(product_id):
    deleted = delete_inventory(product_id)
    if not deleted:
        return jsonify({"message": "Inventory not found!"}), 404
    return jsonify({"message": "Inventory deleted successfully!"}), 200


# Route to list all inventory
@app.route('/inventory', methods=['GET'])
def list_inventory_route():
    inventory = list_inventory()
    serialized_inventory = [serialize_inventory(item) for item in inventory]
    return jsonify(serialized_inventory), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
