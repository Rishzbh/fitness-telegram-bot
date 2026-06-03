import sqlite3

conn = sqlite3.connect("fitness.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    task TEXT,
    status TEXT,
    reason TEXT
)
""")

conn.commit()
