# backend/app.py
from flask import Flask, request, jsonify
from threading import Thread
import time, uuid, json, os
from drone_sim import DroneFleet

app = Flask(__name__)
DATA_DIR = os.path.dirname(__file__)
INV_FILE = os.path.join(DATA_DIR, 'inventory.json')
ORDERS = {}
DRONE_FLEET = DroneFleet()

def load_inventory():
    with open(INV_FILE, 'r') as f:
        return json.load(f)

@app.route('/inventory', methods=['GET'])
def inventory():
    return jsonify(load_inventory())

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    # expecting: { "customer": "Name", "lat": 17.412, "lng": 78.45, "items": ["milk","eggs"] }
    inv = load_inventory()
    # basic availability check
    for it in data.get('items', []):
        if it not in inv or inv[it]['qty'] <= 0:
            return jsonify({"error": f"{it} not available"}), 400

    # reserve items (simple decrement)
    for it in data['items']:
        inv[it]['qty'] -= 1
    with open(INV_FILE, 'w') as f:
        json.dump(inv, f, indent=2)

    order_id = str(uuid.uuid4())[:8]
    ORDERS[order_id] = {
        "id": order_id,
        "customer": data.get('customer'),
        "lat": data.get('lat'),
        "lng": data.get('lng'),
        "items": data.get('items', []),
        "status": "received"
    }

    # dispatch in background
    Thread(target=dispatch_order, args=(order_id,)).start()
    return jsonify({"order_id": order_id, "status": "received"})

def dispatch_order(order_id):
    ORDERS[order_id]['status'] = 'scheduling'
    # simple AI: pick nearest available drone
    drone = DRONE_FLEET.assign_drone(ORDERS[order_id]['lat'], ORDERS[order_id]['lng'])
    if not drone:
        ORDERS[order_id]['status'] = 'queued_no_drone'
        return
    ORDERS[order_id]['status'] = f'drone_assigned:{drone.id}'
    # simulate pickup + delivery
    DRONE_FLEET.start_delivery(drone.id, ORDERS[order_id])
    # the drone simulator updates order status via callback
    # poll for final status
    while ORDERS[order_id]['status'].startswith('drone_assigned') or ORDERS[order_id]['status'].startswith('in_transit'):
        time.sleep(0.5)
        # loop until delivery updates status

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error":"not_found"}), 404
    return jsonify(order)

@app.route('/drones', methods=['GET'])
def drones():
    return jsonify([d.as_dict() for d in DRONE_FLEET.drones])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
