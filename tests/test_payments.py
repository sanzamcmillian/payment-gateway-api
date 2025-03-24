import pytest
from app import app, db
from storage.models import Payments

@pytest.fixture
def client():
    """Set up a test client and initialize the database."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://:memory"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_payment(client):
    """Test payment creation endpoint."""
    response = client.post("/v1/payments", json={
        "customer_name": "Bill Doe",
        "customer_email": "bill@example.com",
        "amount": 50.00
    })
    assert response.status_code == 200
    data = response.get_json()
    assert  "message" in data
    assert data["message"] == "Payment successful" or "Payment created"


def test_create_payment_missing_fields(client):
    """Test error when missing fields."""
    response = client.post("/v1/payments", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data