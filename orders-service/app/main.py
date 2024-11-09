# File: orders-service/app/main.py
from flask import Flask, request, jsonify
from bson import ObjectId
from database import create_order, get_order, update_order_status, delete_order, list_orders
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def serialize_order(order):
    order["_id"] = str(order["_id"])
    return order


# Route to create a new order
@app.route('/orders', methods=['POST'])
def create_order_route():
    order_data = request.get_json()
    create_order(order_data)
    return jsonify({"message": "Order created successfully!"}), 201


# Route to get an order by ID
@app.route('/orders/<order_id>', methods=['GET'])
def get_order_route(order_id):
    order = get_order(order_id)
    if not order:
        return jsonify({"message": "Order not found!"}), 404
    return jsonify(serialize_order(order)), 200


# Route to update an order status by ID
@app.route('/orders/<order_id>', methods=['PUT'])
def update_order_status_route(order_id):
    order_data = request.get_json()
    updated = update_order_status(order_id, order_data.get('status'))
    if not updated:
        return jsonify({"message": "Order not found!"}), 404
    return jsonify({"message": "Order status updated successfully!"}), 200


# Route to delete an order by ID
@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order_route(order_id):
    deleted = delete_order(order_id)
    if not deleted:
        return jsonify({"message": "Order not found!"}), 404
    return jsonify({"message": "Order deleted successfully!"}), 200


# Route to list all orders
@app.route('/orders', methods=['GET'])
def list_orders_route():
    orders = list_orders()
    serialized_orders = [serialize_order(order) for order in orders]
    return jsonify(serialized_orders), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
