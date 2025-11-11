# backend/drone_sim.py
import threading, time, math
import random

# simple haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R=6371 # km
    phi1,phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2-lat1); dlambda = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.asin(math.sqrt(a))

class Drone:
    def __init__(self, id, lat, lng, battery=100):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.battery = battery
        self.available = True
        self.current_order = None

    def as_dict(self):
        return {
            "id": self.id, "lat": self.lat, "lng": self.lng,
            "battery": self.battery, "available": self.available,
            "current_order": self.current_order
        }

class DroneFleet:
    def __init__(self):
        # initialize a few drones around a dark-store location (example: Hyderabad)
        self.drones = [
            Drone("drone-1", 17.412, 78.45, battery=95),
            Drone("drone-2", 17.414, 78.448, battery=80),
            Drone("drone-3", 17.409, 78.455, battery=60),
        ]
        # callback holder for updating orders: import ORDERS in caller or use direct reference
        from backend import app, app as _app  # silent import to satisfy module path when run as package

    def assign_drone(self, lat, lng):
        # choose nearest available drone with enough battery (>30)
        candidates = [d for d in self.drones if d.available and d.battery > 30]
        if not candidates:
            return None
        candidates.sort(key=lambda d: haversine(lat, lng, d.lat, d.lng))
        chosen = candidates[0]
        chosen.available = False
        return chosen

    def start_delivery(self, drone_id, order):
        # run delivery in a thread
        t = threading.Thread(target=self._simulate_delivery, args=(drone_id, order))
        t.start()

    def _simulate_delivery(self, drone_id, order):
        # find drone
        drone = next((d for d in self.drones if d.id==drone_id), None)
        if not drone:
            return
        # update order -> in_transit
        from backend.app import ORDERS
        ORDERS[order['id']]['status'] = f'in_transit:{drone.id}'
        # compute distance and time (simulate)
        dark_store_lat, dark_store_lng = 17.412, 78.45
        dist_to_customer = haversine(dark_store_lat, dark_store_lng, order['lat'], order['lng']) # km
        # assume drone speed 40 km/h -> time in seconds
        speed_kmh = 40
        flight_time_sec = max(5, int((dist_to_customer / speed_kmh) * 3600))
        # simulate takeoff
        for i in range(3):
            time.sleep(0.4)
        # in-flight simulate
        elapsed = 0
        while elapsed < flight_time_sec:
            time.sleep(1)
            elapsed += 1
        # delivered
        ORDERS[order['id']]['status'] = 'delivered'
        drone.available = True
        drone.battery -= int(10 + dist_to_customer)  # rough battery usage
        if drone.battery < 0:
            drone.battery = 0
