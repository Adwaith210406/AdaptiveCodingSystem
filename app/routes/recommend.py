from flask import Blueprint, request, jsonify
import requests
import random

recommend_bp = Blueprint("recommend", __name__)


# 🔥 FETCH PROBLEMS FROM CODEFORCES API
def fetch_problems():
    url = "https://codeforces.com/api/problemset.problems"
    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return []

        data = response.json()

        if data["status"] != "OK":
            return []

        return data["result"]["problems"]

    except Exception as e:
        print("API ERROR:", e)
        return []


# 🔥 FILTER BASED ON DIFFICULTY
def filter_problems(problems, difficulty):
    if difficulty == "easy":
        return [p for p in problems if p.get("rating") and p["rating"] <= 1000]

    elif difficulty == "medium":
        return [p for p in problems if p.get("rating") and 1000 < p["rating"] <= 1600]

    else:
        return [p for p in problems if p.get("rating") and p["rating"] > 1600]


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        # 🔥 STEP 1: FETCH REAL PROBLEMS
        problems = fetch_problems()

        if not problems:
            return jsonify({"error": "Failed to fetch problems"}), 500

        # 🔥 STEP 2: DEFAULT DIFFICULTY (can upgrade later)
        difficulty = "easy"

        # 🔥 STEP 3: FILTER
        filtered = filter_problems(problems, difficulty)

        if not filtered:
            return jsonify({"error": "No problems found"}), 500

        # 🔥 STEP 4: PICK 5 RANDOM QUESTIONS
        selected = random.sample(filtered, min(5, len(filtered)))

        # 🔥 STEP 5: FORMAT FOR FRONTEND
        formatted = [
            {
                "name": p["name"],
                "rating": p.get("rating", "N/A"),
                "contestId": p["contestId"],
                "index": p["index"]
            }
            for p in selected
        ]

        return jsonify({
            "difficulty": difficulty,
            "problems": formatted
        })

    except Exception as e:
        print("RECOMMEND ERROR:", e)
        return jsonify({"error": "Server error"}), 500