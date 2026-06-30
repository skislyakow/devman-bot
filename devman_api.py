import json
import requests

TOKEN = "d109bb7fef85d77beffa5832020d9401d4c6bb21"
BASE_URL = "https://dvmn.org/api/"


def get_reviews(page=1):
    headers = {"Authorization": f"Token {TOKEN}"}
    params = {"page": page}
    response = requests.get(
        f"{BASE_URL}user_reviews/", headers=headers, params=params
    )
    response.raise_for_status()
    return response.json()


def wait_for_review(timestamp=None):
    headers = {"Authorization": f"Token {TOKEN}"}
    params = {}
    if timestamp:
        params["timestamp"] = timestamp
    response = requests.get(
        f"{BASE_URL}long_polling/", headers=headers, params=params, timeout=100
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    timestamp = None
    while True:
        result = wait_for_review(timestamp=timestamp)
        if result["status"] == "found":
            for attempt in result["new_attempts"]:
                status = "✅" if not attempt["is_negative"] else "❌"
                print(
                    f"{status} {attempt['lesson_title']} - {attempt['submitted_at']}"
                )
            timestamp = result["last_attempt_timestamp"]
        elif result["status"] == "timeout":
            timestamp = result["timestamp_to_request"]

"""
    data = get_reviews()
    for review in data["results"]:
        status = "✅" if not review["is_negative"] else "❌"
        print(f"{status} {review['lesson_title']} - {review['submitted_at']}")

    print(json.dumps(data, indent=2, ensure_ascii=False))

    if data["results"]:
        last_ts = data["results"][0]["timestamp"]
        print(f"Ждем новых ревью после {last_ts} ...")
        result = wait_for_review(timestamp=last_ts)
        print(result)
"""
