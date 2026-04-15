from flask import Blueprint, request, jsonify
from app.db.database import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return jsonify({"message": "User created"})
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "user_id": user[0],
            "username": user[1]
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401