# File: users-service/tests/test_user.py
import pytest
import mongomock
import sys
import os
from unittest.mock import patch

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import insert_user, find_user
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    # Mock MongoDB setup
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["ecom_platform"]
    mock_users_collection = mock_db["users"]

    # Patch the database functions to use the mocked collection
    with patch('app.database.users_collection', mock_users_collection):
        with patch('app.database.insert_user', lambda user_data: mock_users_collection.insert_one(user_data)):
            with patch('app.database.find_user', lambda username: mock_users_collection.find_one({"username": username})):
                # Create a test client using Flask's test_client()
                with app.test_client() as test_client:
                    yield test_client


def test_register_user_success(client):
    # Test registering a new user
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully!'


def test_register_user_already_exists(client):
    # Insert a user manually
    insert_user({
        'username': 'existinguser',
        'password': generate_password_hash('password123')
    })

    # Try to register the same user again
    response = client.post('/register', json={
        'username': 'existinguser',
        'password': 'newpassword'
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User already exists!'


def test_login_user_success(client):
    # Insert a user manually
    insert_user({
        'username': 'testuser',
        'password': generate_password_hash('testpassword')
    })

    # Test logging in with correct credentials
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful!'


def test_login_user_invalid_credentials(client):
    # Insert a user manually
    insert_user({
        'username': 'testuser',
        'password': generate_password_hash('testpassword')
    })

    # Test logging in with incorrect password
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid username or password!'


def test_login_user_nonexistent(client):
    # Test logging in with a non-existent user
    response = client.post('/login', json={
        'username': 'nonexistentuser',
        'password': 'password'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid username or password!'
