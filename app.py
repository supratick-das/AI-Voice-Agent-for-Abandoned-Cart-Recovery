from flask import Flask, request, jsonify
from twilio_handler import initiate_call, voice_bp

app = Flask(__name__)
app.register_blueprint(voice_bp)

# Simulated cart abandonment trigger endpoint
@app.route('/trigger_cart_abandonment', methods=['POST'])
def trigger_cart_abandonment():
    data = request.json
    customer_phone = data['phone']
    customer_name = data['name']
    cart_items = data['cart_items']
    call_sid = initiate_call(customer_phone, customer_name, cart_items)
    return jsonify({'status': 'call_initiated', 'call_sid': call_sid})

if __name__ == '__main__':
    app.run(debug=True) 