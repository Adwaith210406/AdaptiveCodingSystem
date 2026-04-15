import sqlite3
import os
import pandas as pd


# 🔹 Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../data/coding.db")

# 🔹 Ensure data folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# =========================
# 🔥 CONNECTION FUNCTION
# =========================
def get_connection():
    return sqlite3.connect(DB_PATH)


# =========================
# 🔥 CREATE TABLE (RUN ONCE)
# =========================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 🔹 submissions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        problem_id TEXT,
        difficulty TEXT,
        correct INTEGER,
        time_taken INTEGER
    )
    """)

    # 🔹 users table (for login system)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()
# =========================
# 🔥 INSERT SUBMISSION
# =========================
def insert_submission(user_id, problem_id, difficulty, correct, time_taken):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions (user_id, problem_id, difficulty, correct, time_taken)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, problem_id, difficulty, correct, time_taken))

    conn.commit()
    conn.close()


# =========================
# 🔥 LOAD USER DATA
# =========================
def load_user_data(user_id):
    conn = get_connection()

    query = """
        SELECT user_id, problem_id, difficulty, correct, time_taken
        FROM submissions
        WHERE user_id = ?
    """

    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    return df


# =========================
# 🔥 OPTIONAL: CLEAR DATA
# =========================
def clear_user_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM submissions WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# =========================
# 🔥 DEBUG FUNCTION
# =========================
def print_all_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM submissions", conn)
    conn.close()

    print(df)
    
def load_all_data():
    conn = get_connection()

    query = """
        SELECT user_id, problem_id, difficulty, correct, time_taken
        FROM submissions
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

def get_leaderboard():
    conn = get_connection()

    query = """
    SELECT users.username,
           COUNT(submissions.id) as attempts,
           SUM(submissions.correct) * 1.0 / COUNT(submissions.id) as accuracy
    FROM submissions
    JOIN users ON users.id = submissions.user_id
    GROUP BY submissions.user_id
    HAVING COUNT(submissions.id) > 0
    ORDER BY accuracy DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # 🔥 Convert to proper JSON format
    leaderboard = []

    for _, row in df.iterrows():
        leaderboard.append({
            "username": row["username"],
            "accuracy": float(row["accuracy"])
        })

    return leaderboard

# =========================
# 🔥 RUN INIT WHEN FILE RUN
# =========================
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized at:", DB_PATH)