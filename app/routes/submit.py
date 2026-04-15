from flask import Blueprint, request, jsonify
from app.db.database import insert_submission

submit_bp = Blueprint("submit", __name__)

@submit_bp.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()

        # 🔍 Extract fields safely
        user_id = data.get("user_id")
        problem_id = data.get("problem_id")
        problem_name = data.get("problem_name")
        difficulty = data.get("difficulty")
        accuracy = data.get("accuracy")

        # 🔒 Validation
        if user_id is None or problem_id is None or difficulty is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Normalize accuracy and keep a compatibility fallback for correctness.
        if accuracy is None:
            correct = data.get("correct", 0)
            accuracy = float(correct)
        else:
            accuracy = float(accuracy)
            correct = 1 if accuracy > 0.6 else 0

        # ⏱️ Placeholder time (can upgrade later)
        time_taken = data.get("time_taken", 100)

        # 💾 Store submission
        insert_submission(
            user_id=user_id,
            problem_id=problem_id,
            problem_name=problem_name,
            difficulty=difficulty,
            accuracy=accuracy,
            correct=correct,
            time_taken=time_taken
        )

        return jsonify({
            "message": "Submission recorded",
            "correct": correct,
            "accuracy_used": accuracy
        })
        print("SUBMIT DATA:", data)

    except Exception as e:
        print("ERROR in /submit:", e)
        return jsonify({"error": "Server error"}), 500
    

