from flask import Blueprint, request, jsonify
from app.services.recommender import predict_next_difficulty
from app.services.codeforces import fetch_problems


recommend_bp = Blueprint("recommend", __name__)


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    if not data or "user_id" not in data:
        return jsonify({"error": "user_id required"}), 400

    try:
        user_id = int(data["user_id"])

        difficulty = predict_next_difficulty(user_id)
        problems = fetch_problems(difficulty)

        return jsonify({
            "user_id": user_id,
            "difficulty": difficulty,
            "problems": problems
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500