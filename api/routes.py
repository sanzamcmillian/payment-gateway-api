from flask import Blueprint, request, jsonify
import requests
from storage.models import db, Payments
import  paypalrestsdk
import uuid

payment_bp = Blueprint("payments", __name__)

@payment_bp.route("/v1/payments", methods=["POST"])
def create_payment():
    data = request.json

    required_fields = ["customer_name", "customer_email", "amount"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    payment_id = str(uuid.uuid4())

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": str(data["amount"]), "currency": "USD"},
            "description": f"Payment by {data['customer_name']}"
        }],
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/v1/payments/success",
            "cancel_url": "http://127.0.0.1:5000/v1/payments/cancel"
        }
    })

    if payment.create():
        approval_url = next(link["href"] for link in payment.links if link["rel"] == "approval_url")

        new_payment = Payments(payment_id=payment_id, amount=data["amount"], name=data["customer_name"], email=data["customer_email"])
        db.session.add(new_payment)
        db.session.commit()

    #payment_url = initiate_paypal_payment(payment_id, amount, name, email)
        return jsonify({"message": "Payment created", "payment_id": payment_id, "approval_url": approval_url}), 200
    else:
        return jsonify({"error": "Payment creation failed", "details": payment.error}), 400
    #return jsonify({"payment_id": payment_id, "status": "pending", "payment_url": payment_url})


@payment_bp.route("/v1/payments/success", methods=["GET"])
def payment_success():
    payment_id = request.args.get("payment_id")
    payer_id = request.args.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        transaction = Payments.query.filter_by(payment_id=payment_id).first()
        if transaction:
            db.session.commit()
        return jsonify({"message": "Payment successful", "payment_id": payment_id}), 200
    else:
        return jsonify({"error": "Payment execution failed"}), 400



@payment_bp.route("/v1/payments/<payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment = Payments.query.filter_by(payment_id=payment_id).first()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(payment.to_dict()), 200


@payment_bp.route("/v1/payments/cancel", methods=["GET"])
def payment_cancel():
    return jsonify({"message": "Payment cancelled"}), 200