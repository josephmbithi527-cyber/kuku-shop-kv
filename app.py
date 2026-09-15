from flask import Flask, render_template, request, jsonify
import datetime
import os
import json

app = Flask(__name__)
ORDERS_FILE = 'orders.json'
COUNTER_FILE = 'order_counter.json'
POCHI = "0746810403"

def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f)

def get_next_order_number():
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
    return f"{counter:03d}"

orders = load_orders()

@app.route('/')
def customer():
    return render_template('customer.html')

@app.route('/vendor')
def vendor():
    return render_template('vendor.html')

@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.json
    phone = data.get('phone')
    place = data.get('placeOfDelivery')
    cart = data.get('cart')
    subtotal = data.get('subtotal')
    total = data.get('total')
    mpesa_code = data.get('mpesaCode')
    order_num = get_next_order_number()
    new_order = {
        'orderNumber': order_num,
        'phone': phone,
        'placeOfDelivery': place,
        'cart': cart,
        'subtotal': subtotal,
        'deliveryFee': 50,
        'total': total,
        'mpesaCode': mpesa_code,
        'status': 'paid',
        'time': datetime.datetime.now().strftime('%H:%M:%S')
    }
    orders.append(new_order)
    save_orders(orders)
    try:
        print(f"NEW ORDER #{order_num} KES {total} from {phone}", flush=True)
        import requests
        msg = f"NEW KUKU ORDER #{order_num} KES {total} Customer {phone} Place {place} Code {mpesa_code}"
        requests.get(f"https://api.callmebot.com/whatsapp.php?phone=254746810403&text={msg}&apikey=123456", timeout=10)
    except:
        pass
    return jsonify({'order': new_order})

@app.route('/api/orders')
def get_orders():
    return jsonify(load_orders())

@app.route('/api/confirm/<int:order_number>', methods=['POST'])
def confirm_order(order_number):
    all_orders = load_orders()
    for o in all_orders:
        if int(o['orderNumber']) == order_number:
            o['status'] = 'confirmed'
    save_orders(all_orders)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
