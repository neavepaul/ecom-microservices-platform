import pytest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from database import users_collection

# Before each test, ensure the test database is clean
@pytest.fixture(autouse=True)
def clear_db():
    users_collection.delete_many({})  # Clear the users collection

def test_register_user(client):
    # Test user registration
    response = client.post('/register', json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully!"

    # Verify user in the database
    user = users_collection.find_one({"username": "testuser"})
    assert user is not None
    assert user["username"] == "testuser"

def test_login_user(client):
    # Pre-insert a user for login test
    users_collection.insert_one({"username": "testuser", "password": "testpassword"})

    # Test successful login
    response = client.post('/login', json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful!"

    # Test failed login
    response = client.post('/login', json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid username or password!"
