import os
import sqlite3
import pandas as pd
from typing import Optional
from app.core.config import Config


# -------------------------------
# 🔌 Connection Handler
# -------------------------------

def get_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "data", "coding.db")

    print("DB PATH:", db_path)  # debug

    return sqlite3.connect(db_path)


# -------------------------------
# 📥 Load Full Dataset (Training)
# -------------------------------

def load_data() -> pd.DataFrame:
    """
    Load entire dataset from database
    Used for model training
    """
    conn = get_connection()

    try:
        query = "SELECT * FROM submissions"
        df = pd.read_sql(query, conn)

        if df.empty:
            raise ValueError("⚠️ Database is empty. Cannot train model.")

        return df

    except Exception as e:
        raise RuntimeError(f"❌ Failed to load data: {str(e)}")

    finally:
        conn.close()


# -------------------------------
# 👤 Load User Data (Prediction)
# -------------------------------

def load_user_data(user_id: int) -> pd.DataFrame:
    """
    Load data for a specific user
    Used for prediction/recommendation
    """
    conn = get_connection()

    try:
        query = "SELECT * FROM submissions WHERE user_id = ?"
        df = pd.read_sql(query, conn, params=(user_id,))

        return df

    except Exception as e:
        raise RuntimeError(f"❌ Failed to load user data: {str(e)}")

    finally:
        conn.close()


# -------------------------------
# 🧪 Health Check (Optional)
# -------------------------------

def check_db_connection() -> bool:
    """
    Simple DB health check
    """
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False