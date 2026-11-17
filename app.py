import json
import socket
from flask import Flask, render_template, request, flash, redirect, url_for
from crypto_utils import encrypt_message, decrypt_message
from database import get_orders

app = Flask(__name__)
app.secret_key = "change-this-demo-secret-key"
TCP_HOST = "127.0.0.1"
TCP_PORT = 5050

PRODUCTS = [
    {
        "name": "Aurora Headphones",
        "category": "Audio",
        "price": 1499,
        "symbol": "♫",
        "tone": "lavender",
        "image": "aurora-headphones.jpg"
    },
    {
        "name": "Cloud Sneakers",
        "category": "Footwear",
        "price": 2199,
        "symbol": "✳",
        "tone": "peach",
        "image": "cloud-sneakers.jpg"
    },
    {
        "name": "Solstice Sunglasses",
        "category": "Accessories",
        "price": 999,
        "symbol": "◎",
        "tone": "mint",
        "image": "solstice-sunglasses.jpg"
    },
    {
        "name": "Nova Smart Watch",
        "category": "Wearables",
        "price": 2799,
        "symbol": "◉",
        "tone": "blue",
        "image": "nova-smartwatch.jpg"
    }
]

def send_secure_order(order):
    """Encrypt order data, send it to the TCP application server, decrypt its reply."""
    encrypted_data = encrypt_message(json.dumps(order).encode("utf-8"))
    with socket.create_connection((TCP_HOST, TCP_PORT), timeout=8) as client:
        client.sendall(encrypted_data)
        encrypted_response = client.recv(65536)
    return json.loads(decrypt_message(encrypted_response).decode("utf-8"))

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)

@app.route("/place-order", methods=["POST"])
def place_order():
    customer = request.form.get("customer", "").strip()
    product = request.form.get("product", "").strip()
    try:
        quantity = int(request.form.get("quantity", "1"))
        selected = next((p for p in PRODUCTS if p["name"] == product), None)
        if not customer or not selected or quantity < 1 or quantity > 20:
            raise ValueError("Please enter a valid name, product and quantity (1–20).")
        order = {
            "customer": customer,
            "product": selected["name"],
            "quantity": quantity,
            "unit_price": float(selected["price"])
        }
        response = send_secure_order(order)
        if response.get("success"):
            flash(
                f"Order #{response['order_id']} confirmed · ₹{response['total_amount']:.2f} · Payment {response['payment_status']}",
                "success"
            )
        else:
            flash(response.get("message", "The order could not be processed."), "error")
    except ValueError as error:
        flash(str(error), "error")
    except (ConnectionRefusedError, OSError):
        flash("The Python TCP server is not running. Start server.py in Terminal 1, then try again.", "error")
    except Exception as error:
        flash(f"Something went wrong: {error}", "error")
    return redirect(url_for("home"))

@app.route("/orders")
def orders():
    return render_template("orders.html", orders=get_orders())

if __name__ == "__main__":
    print("Web store running at http://127.0.0.1:5000")
    print("Make sure server.py is running on TCP port 5050.")
    app.run(host="127.0.0.1", port=5000, debug=True)
