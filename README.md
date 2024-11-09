# E-commerce Microservices Platform
=====================================

## Overview

This is a microservices-based e-commerce platform built using Flask, MongoDB, and Docker. The platform consists of four services:

*   **Users Service**: Handles user registration, login, and authentication.
*   **Products Service**: Manages product information, including creation, retrieval, update, and deletion.
*   **Orders Service**: Handles order creation, retrieval, update, and deletion.
*   **Inventory Service**: Manages inventory levels for products.

## Services

### Users Service

*   **Endpoints**:
    *   `POST /register`: Register a new user.
    *   `POST /login`: Login an existing user.
*   **Database**: Uses a MongoDB collection named "users" to store user data.

### Products Service

*   **Endpoints**:
    *   `POST /products`: Create a new product.
    *   `GET /products`: Retrieve all products.
    *   `GET /products/<product_id>`: Retrieve a product by ID.
    *   `PUT /products/<product_id>`: Update a product by ID.
    *   `DELETE /products/<product_id>`: Delete a product by ID.
*   **Database**: Uses a MongoDB collection named "products" to store product data.

### Orders Service

*   **Endpoints**:
    *   `POST /orders`: Create a new order.
    *   `GET /orders`: Retrieve all orders.
    *   `GET /orders/<order_id>`: Retrieve an order by ID.
    *   `PUT /orders/<order_id>`: Update an order status by ID.
    *   `DELETE /orders/<order_id>`: Delete an order by ID.
*   **Database**: Uses a MongoDB collection named "orders" to store order data.

### Inventory Service

*   **Endpoints**:
    *   `POST /inventory`: Add inventory for a product.
    *   `GET /inventory`: Retrieve all inventory levels.
    *   `GET /inventory/<product_id>`: Retrieve inventory level for a product by ID.
    *   `PUT /inventory/<product_id>`: Update inventory level for a product by ID.
    *   `DELETE /inventory/<product_id>`: Delete inventory level for a product by ID.
*   **Database**: Uses a MongoDB collection named "inventory" to store inventory data.

## Running the Application

1.  Clone the repository.
2.  Build the Docker images using `docker-compose build`.
3.  Start the containers using `docker-compose up`.
4.  Access the services using the exposed ports (e.g., `http://localhost:5001` for the Users Service).

## Testing

Each service has its own set of tests in the `tests` directory. To run the tests, use the `pytest` command.

## Environment Variables

The following environment variables are used:

*   `MONGO_URI`: The MongoDB connection string.

## Dependencies

The following dependencies are used:

*   `Flask`
*   `MongoDB`
*   `Docker`
*   `pytest`
*   `mongomock`
