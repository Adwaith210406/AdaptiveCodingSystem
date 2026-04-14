import sqlite3
import os

base_path = r"C:\Users\adduv\OneDrive\Documents\AdaptiveCoding System\data"
os.makedirs(base_path, exist_ok=True)

db_path = os.path.join(base_path, "coding.db")

conn = sqlite3.connect(db_path)

conn.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    user_id INTEGER,
    problem_id INTEGER,
    difficulty TEXT,
    correct INTEGER,
    time_taken INTEGER
)
""")

conn.commit()
conn.close()


print("✅ DB CREATED AT:", db_path)