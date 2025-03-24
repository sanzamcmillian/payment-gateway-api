from email.policy import default
from enum import unique
from datetime import datetime
from storage import db




class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default="USD")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.payment_id,
            "customer_name": self.name,
            "customer_email": self.email,
            "amount": self.amount,
            "currency": self.currency,
        }
