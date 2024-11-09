import pytest
import mongomock
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import add_inventory, get_inventory, update_inventory, delete_inventory


@pytest.fixture
def client():
    # Mock MongoDB setup
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["ecom_platform"]
    mock_inventory_collection = mock_db["inventory"]

    # Patch the inventory collection in the app's database module
    with patch('app.database.inventory_collection', mock_inventory_collection):
        # Create a test client using Flask's test_client()
        with app.test_client() as test_client:
            yield test_client


def test_create_inventory_success(client):
    response = client.post('/inventory', json={
        'product_id': 'p1',
        'quantity': 50
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Inventory added successfully!'


def test_create_inventory_already_exists(client):
    # Insert an inventory record manually
    add_inventory({
        'product_id': 'p1',
        'quantity': 50
    })

    # Try to add inventory for the same product again
    response = client.post('/inventory', json={
        'product_id': 'p1',
        'quantity': 100
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Inventory for this product already exists!'


def test_get_inventory_success(client):
    # Insert an inventory record manually
    add_inventory({
        'product_id': 'p1',
        'quantity': 50
    })

    # Get the inventory for the product
    response = client.get('/inventory/p1')
    assert response.status_code == 200
    inventory = response.get_json()
    assert inventory['product_id'] == 'p1'
    assert inventory['quantity'] == 50


def test_get_inventory_not_found(client):
    response = client.get('/inventory/nonexistent')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Inventory not found!'


def test_update_inventory_success(client):
    # Insert an inventory record manually
    add_inventory({
        'product_id': 'p1',
        'quantity': 50
    })

    # Update the inventory
    response = client.put('/inventory/p1', json={
        'quantity': 100
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Inventory updated successfully!'


def test_update_inventory_not_found(client):
    response = client.put('/inventory/nonexistent', json={
        'quantity': 100
    })
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Inventory not found!'


def test_delete_inventory_success(client):
    # Insert an inventory record manually
    add_inventory({
        'product_id': 'p1',
        'quantity': 50
    })

    # Delete the inventory
    response = client.delete('/inventory/p1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Inventory deleted successfully!'


def test_delete_inventory_not_found(client):
    response = client.delete('/inventory/nonexistent')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Inventory not found!'


def test_list_inventory(client):
    # Insert inventory records manually
    add_inventory({
        'product_id': 'p1',
        'quantity': 50
    })
    add_inventory({
        'product_id': 'p2',
        'quantity': 30
    })

    # List all inventory
    response = client.get('/inventory')
    assert response.status_code == 200
    inventory = response.get_json()
    assert len(inventory) == 2
    assert inventory[0]['product_id'] == 'p1'
    assert inventory[1]['product_id'] == 'p2'
