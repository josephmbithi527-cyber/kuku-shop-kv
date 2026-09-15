from flask import Flask, render_template, request, jsonify
import datetime
import os

app = Flask(__name__)
orders = []
POCHI = "0746810403"

@app.route('/')
def customer():
    return render_template('customer.html')

@app.route('/vendor')
def vendor():
    return render_template('vendor.html')

@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.json
    order = {
        "orderNumber": f"BS{datetime.datetime.now().strftime('%H:%M:%S')}",
        "phone": data.get('phone'),
        "pickupLocation": data.get('pickup'),
        "items": data.get('cart'),
        "totalPaid": data.get('total'),
        "mpesaCode": data.get('mpesaCode',''),
        "pochi": POCHI,
        "time": datetime.datetime.now().strftime('%H:%M:%S'),
        "status": "PAID"
    }
    orders.append(order)
    print(f"NEW ORDER to {POCHI}: {order}")
    return jsonify({"success": True, "order": order})

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
