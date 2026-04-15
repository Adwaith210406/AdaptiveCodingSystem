import requests
import random


def fetch_problems(difficulty: str, limit=5):

    rating_map = {
        "easy": (800, 1200),
        "medium": (1200, 1800),
        "hard": (1800, 2600)
    }

    min_r, max_r = rating_map.get(difficulty, (800, 1200))

    try:
        url = "https://codeforces.com/api/problemset.problems"
        response = requests.get(url, timeout=5).json()

        problems = response["result"]["problems"]

        filtered = [
            p for p in problems
            if "rating" in p and min_r <= p["rating"] <= max_r
        ]

        selected = random.sample(filtered, min(limit, len(filtered)))

        return selected

    except Exception:
        return []
