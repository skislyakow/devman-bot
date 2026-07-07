# Devman Bot

![Python](https://img.shields.io/badge/python-3.9+-blue)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-Bot-blueviolet)
![requests](https://img.shields.io/badge/requests-long--polling-orange)
![License](https://img.shields.io/badge/license-MIT-green)

Telegram-бот, который отслеживает проверки работ на [Devman](https://dvmn.org) через Long Polling API и присылает уведомления в Telegram.

Стек: `requests` (Long Polling API Девмана) + python-telegram-bot (отправка уведомлений в Telegram).

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
git clone https://github.com/skislyakow/devman-bot.git
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


## Запуск

```bash
python bot.py
```

## Пример уведомления

```
Преподаватель проверил работу!
«Отправляем уведомления о проверке работ» — отклонена ❌
https://dvmn.org/modules/chat-bots/lesson/devman-bot/
```

## Зависимости

- `requests` — HTTP-запросы к API Девмана
- `python-telegram-bot` — класс Bot для отправки сообщений Telegram Bot API
- `python-dotenv` — загрузка переменных из `.env`
