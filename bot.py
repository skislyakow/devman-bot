import asyncio
import os

from dotenv import load_dotenv
import requests
import requests.exceptions

from telegram import Bot


BASE_URL = "https://dvmn.org/api/"


def fetch_review(devman_token, timestamp=None):
    headers = {"Authorization": f"Token {devman_token}"}
    params = {}
    if timestamp:
        params["timestamp"] = timestamp
    try:
        response = requests.get(
            f"{BASE_URL}long_polling/",
            headers=headers,
            params=params,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
    except (
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError,
    ):
        return {"status": "error", "timestamp_to_request": timestamp}


async def monitor_reviews(bot: Bot, devman_token: str, chat_id: int) -> None:
    timestamp = None
    while True:
        result = await asyncio.to_thread(fetch_review, devman_token, timestamp)
        if result["status"] == "found":
            for attempt in result["new_attempts"]:
                emoji = "✅" if not attempt["is_negative"] else "❌"
                status = (
                    "принята" if not attempt["is_negative"] else "отклонена"
                )
                text = (
                    f"Преподаватель проверил работу!\n"
                    f"«{attempt['lesson_title']}» - {status} {emoji}\n"
                    f"{attempt['lesson_url']}"
                )
                await bot.send_message(chat_id=chat_id, text=text)
            timestamp = result["last_attempt_timestamp"]
        elif result["status"] in ("timeout", "error"):
            timestamp = result["timestamp_to_request"]


async def main() -> None:
    load_dotenv()

    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    chat_id = int(os.environ["TELEGRAM_CHAT_ID"])
    devman_token = os.environ["DEVMAN_TOKEN"]

    await monitor_reviews(bot, devman_token, chat_id)


if __name__ == "__main__":
    asyncio.run(main())
