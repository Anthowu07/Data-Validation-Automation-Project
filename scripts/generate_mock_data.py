import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/qa_project.db")

# Ensure the database folder exists
os.makedirs("../db", exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop tables if they exist
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS transactions")

# Create tables
cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE transactions (
    txn_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

# Insert mock users
users = [
    (1, "Alice", "alice@example.com"),         # Valid
    (2, "Bob", None),                          # ❌ Null email
    (3, "Charlie", "charlie@example.com")      # Valid
]
cursor.executemany("INSERT INTO users (user_id, name, email) VALUES (?, ?, ?)", users)

# Insert mock transactions
transactions = [
    (1, 1, 50.0, "success"),                   # Valid
    (2, 2, 75.0, "invalid_status"),            # ❌ Invalid status
    (3, 4, 100.0, "pending"),                  # ❌ Unknown user (user_id 4 doesn't exist)
    (4, 3, 200.0, "failed")                    # Valid
]
cursor.executemany("INSERT INTO transactions (txn_id, user_id, amount, status) VALUES (?, ?, ?, ?)", transactions)

# Commit and close
conn.commit()
conn.close()

print("Mock data generated in db/qa_project.db ✅")
