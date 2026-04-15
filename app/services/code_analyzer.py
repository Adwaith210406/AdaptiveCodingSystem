def analyze_code(code: str):
    feedback = []

    # 🔥 Simple heuristic checks

    # 1. Nested loops
    if "for" in code and code.count("for") > 1:
        feedback.append("⚠️ Nested loops detected — may lead to O(n²) complexity")

    # 2. No input handling
    if "input" not in code:
        feedback.append("⚠️ No input handling detected")

    # 3. No functions
    if "def " not in code:
        feedback.append("⚠️ Consider modularizing your code using functions")

    # 4. Long code
    if len(code) > 300:
        feedback.append("⚠️ Code is long — consider simplifying logic")

    # 5. Recursion hint
    if "recursion" in code.lower():
        feedback.append("💡 Ensure recursion has proper base case")

    if not feedback:
        feedback.append("✅ Code looks good! Consider optimizing further.")

    return feedback