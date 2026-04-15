from flask import Blueprint, request, jsonify

analyze_bp = Blueprint("analyze", __name__)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze_code():
    data = request.get_json()
    code = data.get("code", "")

    feedback = []

    # 🔍 1. LENGTH CHECK
    if len(code) < 50:
        feedback.append(
            "⚠️ Your code is very short. Make sure you've fully implemented the solution and not just a partial snippet."
        )

    # 🔍 2. NESTED LOOPS
    if code.count("for") > 2:
        feedback.append(
            "⚠️ Multiple nested loops detected. This may increase time complexity (possibly O(n²) or worse). Try optimizing using better data structures like hash maps or prefix sums."
        )

    # 🔍 3. INPUT OPTIMIZATION (PYTHON)
    if "input()" in code:
        feedback.append(
            "⚡ Using input() can be slow for large inputs. Consider using sys.stdin.readline() for faster input handling in competitive programming."
        )

    # 🔍 4. DEBUG PRINTS
    if "print(" in code and "return" not in code:
        feedback.append(
            "🧪 Debug print statements detected. Ensure unnecessary prints are removed before final submission to avoid wrong answers."
        )

    # 🔍 5. NO FUNCTIONS
    if "def " not in code:
        feedback.append(
            "📦 Your code does not use functions. Structuring your code into functions improves readability and reusability."
        )

    # 🔍 6. HARD-CODED VALUES
    if "==" in code and any(num in code for num in ["10", "100", "1000"]):
        feedback.append(
            "⚠️ Possible hard-coded values detected. Ensure your solution works for all test cases, not just specific ones."
        )

    # 🔍 7. EDGE CASES
    if "if" not in code:
        feedback.append(
            "⚠️ No conditional checks detected. Make sure you are handling edge cases (like empty inputs or minimum values)."
        )

    # 🔍 8. DEFAULT GOOD FEEDBACK
    if not feedback:
        feedback.append(
            "✅ Your code structure looks good! Consider testing edge cases and optimizing further if needed."
        )

    return jsonify({"feedback": feedback})