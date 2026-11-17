import json
import socketserver
from crypto_utils import encrypt_message, decrypt_message
from database import initialize_database, save_order
from payment_server import process_payment
from network_monitor import record_event

HOST = "127.0.0.1"
PORT = 5050

class EcommerceHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_ip, client_port = self.client_address
        server_ip, server_port = self.request.getsockname()
        try:
            encrypted_request = self.request.recv(65536)
            if not encrypted_request:
                return

            record_event("CLIENT -> SERVER", client_ip, server_ip,
                         client_port, server_port, len(encrypted_request))
            print(f"\nEncrypted data received: {len(encrypted_request)} bytes")

            # Decrypt the incoming transaction.
            request_text = decrypt_message(encrypted_request).decode("utf-8")
            order = json.loads(request_text)
            print("Decrypted transaction:", order)

            customer = str(order["customer"]).strip()
            product = str(order["product"]).strip()
            quantity = int(order["quantity"])
            unit_price = float(order["unit_price"])

            if not customer or not product or quantity < 1 or unit_price <= 0:
                raise ValueError("Please enter valid order details.")

            amount = round(quantity * unit_price, 2)
            payment_status = process_payment(amount)
            order_id = save_order(customer, product, quantity, amount, payment_status)

            response = {
                "success": True,
                "message": "Order processed successfully",
                "order_id": order_id,
                "total_amount": amount,
                "payment_status": payment_status
            }
        except Exception as error:
            response = {"success": False, "message": str(error)}

        encrypted_response = encrypt_message(
            json.dumps(response).encode("utf-8")
        )
        self.request.sendall(encrypted_response)
        record_event("SERVER -> CLIENT", server_ip, client_ip,
                     server_port, client_port, len(encrypted_response))
        print("Encrypted response sent to customer.")

class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    initialize_database()
    print("=" * 55)
    print(" SECURE E-COMMERCE APPLICATION SERVER")
    print(f" Listening on {HOST}:{PORT}")
    print(" Waiting for customer transactions...")
    print(" Press CTRL+C to stop.")
    print("=" * 55)
    with ThreadedTCPServer((HOST, PORT), EcommerceHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
