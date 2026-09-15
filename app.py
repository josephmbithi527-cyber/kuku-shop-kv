from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import json, os
from datetime import datetime

app = Flask(__name__)

@app.route('/googleb174ec1f7734b91b.html')
def google_verify():
    return 'google-site-verification: googleb174ec1f7734b91b.html'

@app.route('/robots.txt')
def robots():
    txt = "User-agent: *\nAllow: /\nSitemap: https://kuku-shop-kv.onrender.com/sitemap.xml"
    return Response(txt, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://kuku-shop-kv.onrender.com/</loc></url>
</urlset>"""
    return Response(xml, mimetype='application/xml')

ORDERS_FILE = 'orders.json'
ORDERS_FILE = 'orders.json'

def load_orders():
    if not os.path.exists(ORDERS_FILE): return []
    try:
        with open(ORDERS_FILE,'r') as f: return json.load(f)
    except: return []

def save_orders(orders):
    with open(ORDERS_FILE,'w') as f: json.dump(orders,f,indent=2)

def get_next_order_number():
    orders = load_orders()
    if not orders: return 1011
    return max(o.get('orderNumber',1010) for o in orders)+1

@app.route('/')
def customer(): return render_template('customer.html')

@app.route('/vendor')
def vendor(): return render_template('vendor.html')

@app.route('/api/mpesa_prompt', methods=['POST'])
def mpesa_prompt():
    data = request.json
    phone = data.get('phone','')
    total = data.get('total',0)
    # REAL STK Push will go to Till 0746810403 here
    return jsonify({'ok': True, 'message': f'M-Pesa prompt of KES {total} sent to {phone}. Pay to Till 0746810403'})

@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.json
    phone = data.get('phone','').strip()
    total = data.get('total',0)
    place = data.get('placeOfDelivery','').strip()
    cart = data.get('cart',[])
    mpesa_code = data.get('mpesaCode','').strip().upper()

    if not place:
        return jsonify({'error': 'Place of delivery must be filled!'}), 400
    if not mpesa_code or len(mpesa_code) < 4:
        return jsonify({'error': 'Enter M-Pesa Code after paying (e.g UIF7I6CCHT)'}), 400

    orders = load_orders()
    order_num = get_next_order_number()
    subtotal = total - 50

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
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    orders.append(new_order)
    save_orders(orders)
    return jsonify({'order': new_order})

@app.route('/api/orders')
def get_orders(): return jsonify(load_orders()[::-1])

@app.route('/api/confirm/<int:order_number>', methods=['POST'])
def confirm_order(order_number):
    orders = load_orders()
    for o in orders:
        if o['orderNumber']==order_number:
            o['status']='received'
            save_orders(orders)
            return jsonify({'ok': True})
    return jsonify({'error':'not found'}),404


@app.route('/manifest.json')
def manifest_file():
    return render_template('manifest.json')

@app.route('/sw.js')
def sw_file():
    return send_from_directory('static', 'sw.js')

@app.route('/robots.txt')
def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://kukushop-kv.onrender.com/sitemap.xml", 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://kukushop-kv.onrender.com/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>
</urlset>"""
    return xml, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
