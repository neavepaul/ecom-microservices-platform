import os
import pytest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from main import app

# Set environment variable for testing
os.environ["TESTING"] = "true"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
