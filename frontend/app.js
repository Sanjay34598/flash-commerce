// frontend/app.js
const API = 'http://localhost:5000';

async function loadInventory() {
  const res = await fetch(API + '/inventory');
  const inv = await res.json();
  const invDiv = document.getElementById('inventory');
  invDiv.innerHTML = '<strong>Inventory</strong><br/>';
  const itemsDiv = document.getElementById('items');
  itemsDiv.innerHTML = '';
  for (let k of Object.keys(inv)) {
    invDiv.innerHTML += `${k} - ₹${inv[k].price} (qty:${inv[k].qty})<br/>`;
    const cb = document.createElement('input');
    cb.type='checkbox'; cb.id='it-'+k; cb.value=k;
    const lbl = document.createElement('label');
    lbl.htmlFor = cb.id; lbl.innerText = ' ' + k + ' ';
    itemsDiv.appendChild(cb); itemsDiv.appendChild(lbl);
  }
}

async function loadFleet() {
  const res = await fetch(API + '/drones');
  const fleet = await res.json();
  const fdiv = document.getElementById('fleet');
  fdiv.innerHTML = '<strong>Drone Fleet</strong><br/>';
  fleet.forEach(d => {
    fdiv.innerHTML += `${d.id} — loc:${d.lat.toFixed(3)},${d.lng.toFixed(3)} — battery:${d.battery} — available:${d.available}<br/>`;
  });
}

async function placeOrder() {
  const customer = document.getElementById('customer').value;
  const lat = parseFloat(document.getElementById('lat').value);
  const lng = parseFloat(document.getElementById('lng').value);
  const items = [];
  document.querySelectorAll('#items input[type=checkbox]').forEach(cb => { if(cb.checked) items.push(cb.value); });
  if(items.length===0) { alert('choose an item'); return; }
  const res = await fetch(API + '/order', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body:JSON.stringify({customer, lat, lng, items})
  });
  const data = await res.json();
  if(res.ok) {
    document.getElementById('order-status').innerText = `Order placed: ${data.order_id}`;
    pollStatus(data.order_id);
  } else {
    alert(JSON.stringify(data));
  }
}

async function pollStatus(orderId) {
  const statusDiv = document.getElementById('order-status');
  const interval = setInterval(async () => {
    const res = await fetch(API + '/order/' + orderId);
    if(!res.ok) { statusDiv.innerText = 'Order not found'; clearInterval(interval); return; }
    const data = await res.json();
    statusDiv.innerText = `Order ${orderId} — status: ${data.status}`;
    if(data.status === 'delivered' || data.status==='queued_no_drone') {
      clearInterval(interval);
      loadInventory(); loadFleet();
    }
  }, 1500);
}

document.getElementById('place').addEventListener('click', placeOrder);
window.onload = () => { loadInventory(); loadFleet(); setInterval(loadFleet, 5000); };
