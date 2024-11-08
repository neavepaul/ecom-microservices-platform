from flask import Flask, request, jsonify
from database import insert_user, find_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# Route to create a new user (simple example)
@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    if find_user(user_data['username']):
        return jsonify({"message": "User already exists!"}), 400
    hashed_password = generate_password_hash(user_data['password'])
    user_data['password'] = hashed_password
    insert_user(user_data)
    return jsonify({"message": "User registered successfully!"}), 201

# Route for user login (simplified authentication)
@app.route('/login', methods=['POST'])
def login_user():
    user_data = request.get_json()
    user = find_user(user_data['username'])
    if user and check_password_hash(user['password'], user_data['password']):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid username or password!"}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)