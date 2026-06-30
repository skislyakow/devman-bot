import asyncio
import os

from dotenv import load_dotenv
import requests
import requests.exceptions
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BASE_URL = "https://dvmn.org/api/"


def wait_for_review(devman_token, timestamp=None):
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
        return {"status": "timeout", "timestamp_to_request": timestamp}


chat_ids = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat:
        return
    chat_id = update.effective_chat.id
    chat_ids.add(chat_id)
    user = update.effective_user
    name = user.full_name if user else "Незнакомец"
    await update.message.reply_text(f"Hello, {name}. Бот включён!")


async def poll_devman(app: Application, devman_token: str):
    timestamp = None
    while True:
        result = await asyncio.to_thread(
            wait_for_review, devman_token, timestamp
        )
        if result["status"] == "found":
            for attempt in result["new_attempts"]:
                emoji = "✅" if not attempt["is_negative"] else "❌"
                text = f"Преподаватель проверил работу!\n{emoji} {attempt['lesson_title']}"
                for chat_id in chat_ids:
                    await app.bot.send_message(chat_id=chat_id, text=text)
            timestamp = result["last_attempt_timestamp"]
        elif result["status"] == "timeout":
            timestamp = result["timestamp_to_request"]


async def main():
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    devman_token = os.environ["DEVMAN_TOKEN"]

    app = Application.builder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))

    async with app:
        if app.updater:
            await app.updater.start_polling()
        await app.start()
        await poll_devman(app, devman_token)


if __name__ == "__main__":
    asyncio.run(main())
