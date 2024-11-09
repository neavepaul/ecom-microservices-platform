import pytest
import mongomock
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import create_order, get_order, update_order_status, delete_order


@pytest.fixture
def client():
    # Mock MongoDB setup
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["ecom_platform"]
    mock_orders_collection = mock_db["orders"]

    # Patch the orders collection in the app's database module
    with patch('app.database.orders_collection', mock_orders_collection):
        # Create a test client using Flask's test_client()
        with app.test_client() as test_client:
            yield test_client


def test_create_order_success(client):
    response = client.post('/orders', json={
        'order_id': 'o1',
        'product_id': 'p1',
        'quantity': 2,
        'status': 'pending'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Order created successfully!'


def test_get_order_success(client):
    # Insert an order manually
    create_order({
        'order_id': 'o1',
        'product_id': 'p1',
        'quantity': 2,
        'status': 'pending'
    })

    # Get the order
    response = client.get('/orders/o1')
    assert response.status_code == 200
    order = response.get_json()
    order['_id'] = str(order['_id'])  # Convert ObjectId to string for JSON serialization
    assert order['order_id'] == 'o1'
    assert order['status'] == 'pending'


def test_get_order_not_found(client):
    response = client.get('/orders/nonexistent')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Order not found!'


def test_update_order_status_success(client):
    # Insert an order manually
    create_order({
        'order_id': 'o1',
        'product_id': 'p1',
        'quantity': 2,
        'status': 'pending'
    })

    # Update the order status
    response = client.put('/orders/o1', json={
        'status': 'shipped'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Order status updated successfully!'


def test_update_order_status_not_found(client):
    response = client.put('/orders/nonexistent', json={
        'status': 'shipped'
    })
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Order not found!'


def test_delete_order_success(client):
    # Insert an order manually
    create_order({
        'order_id': 'o1',
        'product_id': 'p1',
        'quantity': 2,
        'status': 'pending'
    })

    # Delete the order
    response = client.delete('/orders/o1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Order deleted successfully!'


def test_delete_order_not_found(client):
    response = client.delete('/orders/nonexistent')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Order not found!'


def test_list_orders(client):
    # Insert orders manually
    create_order({
        'order_id': 'o1',
        'product_id': 'p1',
        'quantity': 2,
        'status': 'pending'
    })
    create_order({
        'order_id': 'o2',
        'product_id': 'p2',
        'quantity': 1,
        'status': 'shipped'
    })

    # List all orders
    response = client.get('/orders')
    assert response.status_code == 200
    orders = response.get_json()
    for order in orders:
        order['_id'] = str(order['_id'])  # Convert ObjectId to string for JSON serialization
    assert len(orders) == 2
    assert orders[0]['order_id'] == 'o1'
    assert orders[1]['order_id'] == 'o2'
