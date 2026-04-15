from flask import Blueprint, request, jsonify

analyze_bp = Blueprint("analyze", __name__)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    code = data.get("code", "").strip()

    # 🔥 EMPTY CODE CHECK
    if not code:
        return jsonify({
            "error": "No code given. Please paste your code before analyzing."
        }), 400

    feedback = []
    issues = 0

    # 🔍 RULES
    if len(code) < 50:
        feedback.append("⚠️ Code is too short — may be incomplete.")
        issues += 1

    if code.count("for") > 2:
        feedback.append("⚠️ Too many loops → high time complexity.")
        issues += 1

    if "input()" in code:
        feedback.append("⚡ Use faster input methods (sys.stdin).")
        issues += 1

    if "print(" in code and "return" not in code:
        feedback.append("🧪 Remove debug prints.")
        issues += 1

    if "def " not in code:
        feedback.append("📦 Use functions for better structure.")
        issues += 1

    if "==" in code and any(num in code for num in ["10", "100", "1000"]):
        feedback.append("⚠️ Avoid hard-coded values.")
        issues += 1

    if "if" not in code:
        feedback.append("⚠️ Handle edge cases.")
        issues += 1

    # 🔥 ACCURACY
    total_rules = 7
    accuracy = max(0, (total_rules - issues) / total_rules)

    if issues == 0:
        feedback.append("✅ Code looks good!")

    return jsonify({
        "feedback": feedback,
        "accuracy": accuracy
    })