SECURE E-COMMERCE NETWORK - PYTHON PROJECT
==========================================

1. REQUIREMENTS
---------------
- Windows PC
- Python 3.10 or later
- VS Code
- Internet connection for installing the cryptography package (first time only)

2. OPEN THE PROJECT
-------------------
- Extract Secure_Ecommerce_Network.zip.
- Open VS Code.
- Select File -> Open Folder.
- Select the extracted Secure_Ecommerce_Network folder.
- Open Terminal -> New Terminal.

3. INSTALL THE REQUIRED PACKAGE
-------------------------------
Run:

    python -m pip install -r requirements.txt

If "python" does not work, try:

    py -m pip install -r requirements.txt

4. RUN THE PROJECT
------------------
IMPORTANT: Open TWO VS Code terminals.

TERMINAL 1 - Start the server:

    python server.py

Wait until you see:
    Listening on 127.0.0.1:5050
    Waiting for customer transactions...

TERMINAL 2 - Start the customer client:

    python client.py

Enter customer name, product name, quantity and price.
The client encrypts the order and sends it to the server.
The server decrypts it, processes a mock payment and stores the order.

5. VIEW DATABASE ORDERS
------------------------
Run in a terminal:

    python view_orders.py

Orders are stored in orders.db (created automatically).

6. VIEW NETWORK MONITOR LOG
---------------------------
Open network_activity.log after making a transaction.
It records timestamp, communication direction, source/destination IP,
ports and encrypted message size.

7. WIRESHARK DEMONSTRATION
--------------------------
- Start Wireshark.
- Select the loopback interface (often named Npcap Loopback Adapter on Windows).
- Use display filter: tcp.port == 5050
- Run a customer transaction in the second terminal.
- Stop capture and inspect the TCP packets.
- The transaction payload is encrypted. Packet metadata such as IP addresses,
  ports, packet lengths and timing remains observable.

8. NMAP DEMONSTRATION (OPTIONAL)
--------------------------------
Only scan your own computer / authorized lab systems.
After starting server.py, run:

    nmap -sT -p 5050 127.0.0.1

This checks whether the project's TCP server port is open.
Install Nmap separately if it is not already installed.

9. PROJECT CONCEPTS
-------------------
Client-Server: client.py sends a purchase request to server.py.
TCP/IP: socket communication uses TCP.
Encryption/Decryption: Fernet protects the transaction message.
IP Addressing: local client and server IP addresses are displayed.
Ports: server listens on TCP port 5050.
Network Monitoring: network_activity.log records connection metadata.
Database: SQLite stores processed orders.
Payment Server: payment_server.py simulates payment approval.

10. IMPORTANT SECURITY NOTE
---------------------------
This is an educational localhost demonstration, not a production payment
system. The encryption key is shared in secret.key so both local programs
can encrypt/decrypt. Do not use real card numbers, passwords or personal
payment information. For real deployment, use HTTPS/TLS, proper key
management, authentication, authorization and a certified payment provider.
The local monitor log records application-level message sizes; it is not
a replacement for Wireshark packet capture.
