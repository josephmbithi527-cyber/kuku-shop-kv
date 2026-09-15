from flask import Flask, render_template, request, jsonify
import datetime
import os
import jsonapp = Flask(name)ORDERS_FILE = 'orders.json'
COUNTER_FILE = 'order_counter.json'
POCHI = "0746810403"def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f)def get_next_order_number():
    counter = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                counter = json.load(f).get('count', 0)
        except:
            counter = 0
    counter += 1
    with open(COUNTER_FILE, 'w') as f:
        json.dump({'count': counter}, f)
    return f"{counter:03d}"orders = load_orders()@app.route('/')
def customer():
    return render_template('customer.html')@app.route('/vendor')
def vendor():
    return render_template('vendor.html')@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.json
    phone = data.get('phone')
    place = data.get('placeOfDelivery')
    cart = data.get('cart')
    subtotal = data.get('subtotal')
    total = data.get('total')
    mpesa_code = data.get('mpesaCode')
