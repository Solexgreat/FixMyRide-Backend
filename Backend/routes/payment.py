from flask import Flask, redirect, request, jsonify
import stripe
# from torch import device
from . import payment_bp

app = Flask(__name__, static_url_path="", static_folder="public")
# Your_Domain =


@payment_bp.route('/checkout-session', methods=['POST'], strict_slashes=False)
def create_checkout_session():
    """
    """
    try:
        data = request.get_json()
        list_item = {
            'payment_method_types': ['card'],
            'line_items': [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': data['name'],
                        },
                        'unit_amount': data['amount'],
                    },
                    'quantity': 1,
                },
            ]
        }
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[list_item],
            mode='payment',
            success_url = 'http://localhost:3000/success',
            cancel_url = 'http://localhost:3000/cancel',
        )

        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e) }), 400

@payment_bp.route('/payout', methods=['POST'], strict_slashes=False)
def create_payment():
    """
    """
    try:
        data = request.get_json()
        stripe_acccount = data.get('stripe_account')
        amount = data.get('amount')

        # Create a PaymentIntent
        payout = stripe.Transfer.create(
            amount=amount,
            currency='usd',
            stripe_account=stripe_acccount,
        )

        return jsonify({'status': 'success', 'payout': payout}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400