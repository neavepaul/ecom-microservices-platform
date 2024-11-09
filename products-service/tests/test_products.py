# File: products-service/tests/test_products.py
import pytest
import mongomock
import sys
import os
from unittest.mock import patch
from bson import ObjectId
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import insert_product, find_product, update_product, delete_product, products_collection


@pytest.fixture
def client():
    # Mock MongoDB setup
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["ecom_platform"]
    mock_products_collection = mock_db["products"]

    # Patch the products collection in the app's database module
    with patch('app.database.products_collection', mock_products_collection):
        # Create a test client using Flask's test_client()
        with app.test_client() as test_client:
            yield test_client


def test_create_product_success(client):
    response = client.post('/products', json={
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Product created successfully!'


def test_create_product_already_exists(client):
    # Insert a product manually
    insert_product({
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })

    # Try to create the same product again
    response = client.post('/products', json={
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Product already exists!'


def test_get_product_success(client):
    # Insert a product manually
    insert_product({
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })

    # Get the product
    response = client.get('/products/p1')
    assert response.status_code == 200
    product = response.get_json()
    product['_id'] = str(product['_id'])  # Convert ObjectId to string for JSON serialization
    assert product['product_id'] == 'p1'
    assert product['name'] == 'Product 1'


def test_get_product_not_found(client):
    response = client.get('/products/nonexistent')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Product not found!'


def test_update_product_success(client):
    # Insert a product manually
    insert_product({
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })

    # Update the product
    response = client.put('/products/p1', json={
        'name': 'Updated Product 1',
        'price': 150
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product updated successfully!'


def test_update_product_not_found(client):
    response = client.put('/products/nonexistent', json={
        'name': 'Updated Product'
    })
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Product not found!'


def test_delete_product_success(client):
    # Insert a product manually
    insert_product({
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })

    # Delete the product
    response = client.delete('/products/p1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product deleted successfully!'


def test_delete_product_not_found(client):
    response = client.delete('/products/nonexistent')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Product not found!'


def test_list_products(client):
    # Insert products manually
    insert_product({
        'product_id': 'p1',
        'name': 'Product 1',
        'price': 100,
        'quantity': 10
    })
    insert_product({
        'product_id': 'p2',
        'name': 'Product 2',
        'price': 200,
        'quantity': 5
    })

    # List all products
    response = client.get('/products')
    assert response.status_code == 200
    products = response.get_json()
    for product in products:
        product['_id'] = str(product['_id'])  # Convert ObjectId to string for JSON serialization
    assert len(products) == 2
    assert products[0]['product_id'] == 'p1'
    assert products[1]['product_id'] == 'p2'
