import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "orders.db"

def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_status TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_order(customer, product, quantity, amount, payment_status):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            """INSERT INTO orders
               (customer, product, quantity, amount, payment_status)
               VALUES (?, ?, ?, ?, ?)""",
            (customer, product, quantity, amount, payment_status)
        )
        return cursor.lastrowid

def get_orders():
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute(
            "SELECT id, customer, product, quantity, amount, payment_status, created_at FROM orders ORDER BY id DESC"
        ).fetchall()
