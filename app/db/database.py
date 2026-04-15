import sqlite3
import os
import pandas as pd

# 🔹 Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../data/coding.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# =========================
# 🔥 CONNECTION
# =========================
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# 🔥 INIT DB (FIXED)
# =========================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 🔥 FORCE NEW STRUCTURE SAFELY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        problem_id TEXT,
        problem_name TEXT,
        difficulty TEXT,
        accuracy REAL,
        correct INTEGER,
        time_taken INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # 🔥 MIGRATION FIX (CRITICAL)
    cursor.execute("PRAGMA table_info(submissions)")
    columns = [row["name"] for row in cursor.fetchall()]

    # Add missing columns safely
    if "id" not in columns:
        cursor.execute("ALTER TABLE submissions ADD COLUMN id INTEGER")

    if "problem_name" not in columns:
        cursor.execute("ALTER TABLE submissions ADD COLUMN problem_name TEXT")

    if "accuracy" not in columns:
        cursor.execute("ALTER TABLE submissions ADD COLUMN accuracy REAL")

    if "correct" not in columns:
        cursor.execute("ALTER TABLE submissions ADD COLUMN correct INTEGER")

    if "time_taken" not in columns:
        cursor.execute("ALTER TABLE submissions ADD COLUMN time_taken INTEGER")

    # 🔥 FIX NULL DATA
    cursor.execute("""
        UPDATE submissions
        SET problem_name = problem_id
        WHERE problem_name IS NULL
    """)

    cursor.execute("""
        UPDATE submissions
        SET accuracy = CAST(correct AS REAL)
        WHERE accuracy IS NULL AND correct IS NOT NULL
    """)

    conn.commit()
    conn.close()


# =========================
# 🔥 INSERT
# =========================
def insert_submission(user_id, problem_id, problem_name, difficulty, accuracy, correct, time_taken):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions (
            user_id, problem_id, problem_name, difficulty, accuracy, correct, time_taken
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, problem_id, problem_name, difficulty, accuracy, correct, time_taken))

    conn.commit()
    conn.close()


# =========================
# 🔥 USER DATA
# =========================
def load_user_data(user_id):
    conn = get_connection()

    query = """
        SELECT problem_name, difficulty, accuracy, correct, time_taken
        FROM submissions
        WHERE user_id = ?
    """

    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    return df


# =========================
# 🔥 ALL DATA
# =========================
def load_all_data():
    conn = get_connection()

    query = """
        SELECT user_id, problem_name, difficulty, accuracy, correct
        FROM submissions
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


# =========================
# 🔥 LEADERBOARD (FIXED)
# =========================
def get_leaderboard():
    conn = get_connection()

    query = """
    SELECT users.username,
           AVG(submissions.accuracy) as accuracy
    FROM submissions
    JOIN users ON users.id = submissions.user_id
    WHERE submissions.accuracy IS NOT NULL
    GROUP BY submissions.user_id
    ORDER BY accuracy DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.to_dict(orient="records")


# =========================
# 🔥 USER STATS (FIXED)
# =========================
def get_user_stats(user_id):
    conn = get_connection()

    query = """
    SELECT problem_name,
           difficulty,
           accuracy,
           time_taken
    FROM submissions
    WHERE user_id = ?
      AND accuracy IS NOT NULL
    """

    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    return df.to_dict(orient="records")


# =========================
# 🔥 DEBUG
# =========================
def print_all_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM submissions", conn)
    conn.close()
    print(df)


# =========================
# 🔥 RUN INIT
# =========================
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized at:", DB_PATH)