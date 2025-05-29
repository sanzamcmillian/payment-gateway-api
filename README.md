# payment-gateway-api

Develop a RESTful Payment Gateway API for Small Businesses.

# Objective

This is a basic RESTful API that allows small businesses to accept payments from customers using payment gateway PayPal, focusing on minimal customer information (name, email,
amount).
Implemententation with the use versioning, and automate testing and deployment through CI/CD.

# Features
- Initiate payments
- Retrieve transaction details
- Versioned API endpoints
- Deployed with Render


# Technologies Used

- Flask (Python)
- SQLite (Database)
- Paypal (Payment Processors)
- Gunicorn (Production WSGI Server)

# Installation

1. Clone the Repository
   ```bash
   git clone https://github.com/sanzamcmillian/payment_gateway-api.git
   cd payment-gateway-api

3. Create a Virtual Environment

   ```bash
    python -m venv venv
    source venv/bin/activate or
    venv\Scripts\activate //Windows

3. Install Dependencies

    ```bash
    pip install -r requirements.txt

4. Set Up the Database

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

5. Run the Application

    ```bash
    flask run

The app will be accessible at http://localhost:5000


# API Endpoints

1. Initiate a Payment
    ```plaintext
    POST /v1/payments

    Request Body:

    {
      "payment_id": "12345",
      "customer_name": "John Doe",
      "customer_email": "john@example.com",
      "amount": 100.00
    }

    Response:

    {
      "message": "Payment created successfully",
      "status": "pending",
      "payment_id": "12345"
    }
    ```

2. Get Payment Details

 GET /v1/payments/<payment_id>

Response:
 {
  "payment_id": "12345",
  "customer_name": "John Doe",
  "customer_email": "john@example.com"
  "amount": 100.00,
  "status": "completed"
 }


# Running tests

 pytest tests/


# Live Link

[(https://payment-gateway-api-foz9.onrender.com)]

# Contributors

- Sanele Skhosana (@sanzamcmillian)

# License

This project is licensed under MIT License.

