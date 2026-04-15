from flask import Blueprint, request, jsonify
from app.db.database import insert_submission

submit_bp = Blueprint("submit", __name__)

@submit_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    user_id = data.get("user_id")
    problem_id = data.get("problem_id")
    difficulty = data.get("difficulty")
    correct = data.get("correct", 1)
    time_taken = data.get("time_taken", 100)

    insert_submission(user_id, problem_id, difficulty, correct, time_taken)

    return jsonify({"message": "Submission recorded"})