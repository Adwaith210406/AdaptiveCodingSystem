import sqlite3
import random

db_path = r"C:\Users\adduv\OneDrive\Documents\AdaptiveCoding System\data\coding.db"

conn = sqlite3.connect(db_path)

for _ in range(100):
    conn.execute("""
    INSERT INTO submissions VALUES (?, ?, ?, ?, ?)
    """, (
        random.randint(1, 10),
        random.randint(1, 100),
        random.choice(["easy", "medium", "hard"]),
        random.randint(0, 1),
        random.randint(100, 1000)
    ))

conn.commit()
conn.close()

print("✅ DATA INSERTED at:", db_path)