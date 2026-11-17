from database import initialize_database, get_orders

initialize_database()
orders = get_orders()

print("\n============== STORED E-COMMERCE ORDERS ==============")
if not orders:
    print("No orders found. Run client.py to create a transaction.")
else:
    for order in orders:
        order_id, customer, product, quantity, amount, status, created = order
        print(f"\nOrder ID: {order_id}")
        print(f"Customer: {customer}")
        print(f"Product: {product}")
        print(f"Quantity: {quantity}")
        print(f"Amount: Rs. {amount:.2f}")
        print(f"Payment: {status}")
        print(f"Created: {created}")
