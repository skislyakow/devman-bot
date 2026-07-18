import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
import requests
import requests.exceptions

from telegram import Bot


BASE_URL = "https://dvmn.org/api/"


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: int):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord):
        if record.name.startswith(("httpx", "telegram", "urllib3")):
            return

        message = self.format(record)
        if len(message) > 4000:
            message = message[:4000] + "\n... (обрезано)"
        loop = asyncio.get_running_loop()
        loop.create_task(
            self.bot.send_message(chat_id=self.chat_id, text=message)
        )


def fetch_review(devman_token, timestamp=None):
    headers = {"Authorization": f"Token {devman_token}"}
    params = {}
    if timestamp:
        params["timestamp"] = timestamp

    response = requests.get(
        f"{BASE_URL}long_polling/",
        headers=headers,
        params=params,
        timeout=(5, 60),
    )
    response.raise_for_status()
    return response.json()


async def monitor_reviews(bot: Bot, devman_token: str, chat_id: int) -> None:
    timestamp = None
    while True:
        try:
            result = await asyncio.to_thread(fetch_review, devman_token, timestamp)
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
        ):
            continue
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
        elif result["status"] == "timeout":
            timestamp = result["timestamp_to_request"]


async def main() -> None:
    load_dotenv()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        stream=sys.stderr,
    )
    logger = logging.getLogger("bot")

    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    chat_id = int(os.environ["TELEGRAM_CHAT_ID"])
    devman_token = os.environ["DEVMAN_TOKEN"]

    telegram_handler = TelegramLogHandler(bot, chat_id)
    telegram_handler.setFormatter(
        logging.Formatter("%(levelname)s - %(message)s")
    )
    logger.addHandler(telegram_handler)

    logger.info("Бот запущен, начинаю мониторинг")

    async def run():
        while True:
            try:
                await monitor_reviews(bot, devman_token, chat_id)
            except Exception:
                logger.error("Бот упал, перезапускаю...", exc_info=True)
                await asyncio.sleep(1)

    await run()


if __name__ == "__main__":
    asyncio.run(main())
