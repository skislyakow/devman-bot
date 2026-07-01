# Devman Bot

![Python](https://img.shields.io/badge/python-3.9+-blue)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-async-green)

Telegram-бот, который отслеживает проверки работ на [Devman](https://dvmn.org) через Long Polling API и присылает уведомления в Telegram.

Бот написан на **асинхронной версии python-telegram-bot (v22+)**, что позволяет параллельно обрабатывать сообщения от Telegram и Long Polling запросы к Devman без блокировок.

## Как это работает

```
Вы отправляете работу → Devman → Long Polling → Telegram → Уведомление
```

Бот в фоне опрашивает API Девмана. Как только преподаватель проверяет работу — бот мгновенно пишет в Telegram: название урока, результат (принята/отклонена) и ссылку.

## Требования

- Python 3.9+
- Telegram-аккаунт

## Установка

```bash
git clone https://github.com/ваш-username/devman-bot.git
cd devman-bot
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` в корне проекта:

```ini
DEVMAN_TOKEN=ваш_токен_с_dvmn.org
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_telegram_id
```

**Где взять:**

| Переменная | Где получить |
|---|---|
| `DEVMAN_TOKEN` | В профиле на dvmn.org (раздел API) |
| `TELEGRAM_BOT_TOKEN` | Создать бота через [@BotFather](https://t.me/botfather) |
| `TELEGRAM_CHAT_ID` | Узнать через [@userinfobot](https://t.me/userinfobot) (опционально) |

`TELEGRAM_CHAT_ID` можно не указывать — достаточно после запуска написать боту `/start`, и он сам запомнит ваш чат.

## Запуск

```bash
python bot.py
```

После запуска напишите боту `/start`, чтобы подписаться на уведомления.

## Пример уведомления

```
Преподаватель проверил работу!
«Отправляем уведомления о проверке работ» — отклонена ❌
https://dvmn.org/modules/chat-bots/lesson/devman-bot/
```

## Файлы проекта

| Файл | Назначение |
|---|---|
| `bot.py` | Основной скрипт бота |
| `.env` | Переменные окружения (токены) — не коммитить! |
| `.gitignore` | Исключения для git |
| `requirements.txt` | Зависимости проекта |

## Зависимости

- `requests` — HTTP-запросы к API Девмана
- `python-telegram-bot` — асинхронный фреймворк для Telegram Bot API (v22+)
- `python-dotenv` — загрузка переменных из `.env`
