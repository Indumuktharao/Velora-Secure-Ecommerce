import json
import socket
from crypto_utils import encrypt_message, decrypt_message

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050

def main():
    print("\n========== SECURE E-COMMERCE CUSTOMER ==========")
    customer = input("Enter customer name: ").strip()
    product = input("Enter product name: ").strip()

    try:
        quantity = int(input("Enter quantity: "))
        unit_price = float(input("Enter price per item (₹): "))
        if not customer or not product or quantity < 1 or unit_price <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Name/product cannot be empty; quantity and price must be positive.")
        return

    order = {
        "customer": customer,
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price
    }

    # Encrypt before sending over TCP.
    encrypted_data = encrypt_message(json.dumps(order).encode("utf-8"))
    print("\nOriginal transaction:", order)
    print("Encrypted transaction prepared.")

    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=10) as client:
            client_ip, client_port = client.getsockname()
            print(f"Client address: {client_ip}:{client_port}")
            print(f"Server address: {SERVER_HOST}:{SERVER_PORT}")
            client.sendall(encrypted_data)
            encrypted_response = client.recv(65536)

        response = json.loads(decrypt_message(encrypted_response).decode("utf-8"))
        print("\n========== SERVER RESPONSE ==========")
        if response["success"]:
            print("Status:", response["message"])
            print("Order ID:", response["order_id"])
            print(f"Total amount: ₹{response['total_amount']:.2f}")
            print("Payment:", response["payment_status"])
        else:
            print("Transaction failed:", response["message"])
    except ConnectionRefusedError:
        print("Cannot connect. Start server.py first, then run client.py.")
    except Exception as error:
        print("Communication error:", error)

if __name__ == "__main__":
    main()
