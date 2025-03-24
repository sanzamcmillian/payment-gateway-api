from http.cookiejar import debug

from flask import Flask
from storage import db
from flask_migrate import Migrate
import paypalrestsdk
import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///payments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

paypalrestsdk.configure({
    "mode": config.PAYPAL_MODE,
    "client_id": config.PAYPAL_CLIENT_ID,
    "client_secret": config.PAYPAL_CLIENT_SECRET
})

from storage.models import Payments
from api.routes import payment_bp

with app.app_context():
    db.create_all()

app.register_blueprint(payment_bp)

@app.route("/")
def home():
    return {"message": "Welcome to the Payment Gateway API"}

if __name__ == "__main__":
    app.run(debug=True)