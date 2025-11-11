# ⚡ Flash Commerce — AI Quick Commerce with Drone Delivery

**Flash Commerce** is a futuristic prototype that demonstrates how AI and drones can automate the quick commerce ecosystem.  
It simulates a system where:
- Orders are managed by an AI backend,
- Inventory is tracked automatically,
- Drones are dispatched to deliver items instantly — no human delivery needed 🚁

---

## 🧠 Project Overview

**Goal:** Replicate the concept of ultra-fast delivery (like Blinkit / Zepto) but fully automated — AI-managed dark stores and drone-based deliveries.

### ⚙️ Features
✅ Real-time inventory simulation  
✅ AI-style drone selection (nearest available drone)  
✅ Order tracking (received → scheduled → in-transit → delivered)  
✅ Simple front-end UI (HTML + JS)  
✅ Flask backend simulating AI dispatch & drone fleet management  

---

## 🧩 Architecture Overview

User → Order → AI Dispatcher → Drone Assignment → Simulated Delivery
↓
Inventory Update


- **Frontend:** HTML, JS  
- **Backend:** Flask (Python)  
- **Database:** JSON-based (mock inventory)  
- **Drone Simulation:** Python threading + distance calculation (Haversine formula)

---

## 🚀 Demo (How It Works)

1️⃣ Start the backend:  
```bash
cd backend
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python app.py

2️⃣ Open the front-end:
Open frontend/index.html in your browser.

3️⃣ Place an order:

Choose items like “milk”, “eggs”, “bread”.

Enter your (lat, lng).

Click “Place Order”.

4️⃣ Watch the magic ✨

Backend assigns a drone.

Status updates live:
received → scheduling → drone_assigned → in_transit → delivered.




