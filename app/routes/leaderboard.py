from flask import Blueprint, jsonify
from app.db.database import get_connection

leaderboard_bp = Blueprint("leaderboard", __name__)

@leaderboard_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.username,
               stats.total_attempts,
               stats.correct_attempts
        FROM stats
        JOIN users ON users.id = stats.user_id
    """)

    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        username, total, correct = row

        accuracy = correct / total if total > 0 else 0

        result.append({
            "username": username,
            "accuracy": accuracy
        })

    # SORT BY ACCURACY
    result.sort(key=lambda x: x["accuracy"], reverse=True)

    return jsonify(result)