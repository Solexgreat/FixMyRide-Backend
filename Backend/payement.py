from flask import Flask, redirect, request
import stripe
from torch import device

app = Flask(__name__, static_url_path="", static_folder="public")
# Your_Domain =


@app.route('/create-checkout-session', methods=['POST'], strict_slashes=False)
def create_checkout_session():
    """
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            list_item 
        )
    except Exception as e:
        return str(e)
