import os
import stripe
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

stripe.api_key = os.environ['STRIPE_SECRET_KEY']
stripe_publishable_key = os.environ['STRIPE_PUBLISHABLE_KEY']


@app.route('/')
def index():
    return render_template('index.html', stripe_publishable_key=stripe_publishable_key)


@app.route('/charge', methods=['POST'])
def charge():
    try:
        amount = 500  # $5.00

        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )

        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Sample Charge'
        )

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
