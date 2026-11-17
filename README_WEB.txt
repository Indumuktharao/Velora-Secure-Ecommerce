SECURE E-COMMERCE NETWORK – WEB INTERFACE
==========================================

WHAT THIS ADDS
--------------
This version adds an attractive browser-based storefront to the existing Python
TCP e-commerce project. The website is a Flask frontend. It does NOT replace
server.py: the Flask app sends an encrypted order to the existing TCP server.

HOW THE PARTS CONNECT
--------------------
Browser (Flask website on 127.0.0.1:5000)
    -> app.py encrypts order using crypto_utils.py
    -> TCP connection to server.py at 127.0.0.1:5050
    -> server.py decrypts, simulates payment, saves via database.py
    -> encrypted response returns to app.py
    -> browser displays confirmation
    -> /orders reads saved SQLite orders

REQUIREMENTS
------------
- Python installed
- VS Code
- Internet is only needed if you want the Google Fonts to load; the site still
  works with fallback fonts when offline.
- The existing Wireshark and Nmap tools can still be used for monitoring.

STEP-BY-STEP RUN IN VS CODE
---------------------------
1. Extract this ZIP file.
2. In VS Code choose File > Open Folder and open the extracted
   Secure_Ecommerce_Network_Web folder.
3. Open Terminal > New Terminal.
4. Install the Python packages:
       py -m pip install -r requirements.txt
5. TERMINAL 1 – start the TCP application server:
       py server.py
   Keep this terminal open. It should say it is listening on 127.0.0.1:5050.
6. TERMINAL 2 – start the website:
       py app.py
   Keep this terminal open. It should show:
       Web store running at http://127.0.0.1:5000
7. Open your browser and visit:
       http://127.0.0.1:5000
8. Enter a customer name, choose a product and quantity, then click
   "Place secure order".
9. Open "Order history" in the website or run in TERMINAL 3:
       py view_orders.py

IMPORTANT
---------
- Start server.py BEFORE app.py and before placing an order.
- Do not use VS Code Live Server for this Flask website. Flask serves the
  dynamic pages itself at port 5000.
- Your TCP application server still listens on port 5050.
- This is a local educational demo, not a production e-commerce service.
- Payment approval is simulated; no real money or card details are involved.
- Fernet encryption is used for the demo message. The app is not HTTPS/TLS.
- Keep secret.key private. Do not upload it to a public repository.
- The Flask secret key in app.py is a demo value and must be replaced before
  any real deployment.
