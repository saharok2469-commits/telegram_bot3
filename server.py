import os
import asyncio
from flask import Flask, request
from aiogram import types
from bot import bot, dp

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # пример: https://telegram-bot2-7lj8.onrender.com
WEBHOOK_PATH = "/webhook"


@app.route("/")
def home():
    return "Bot is running!"


# --- Webhook принимает обновления синхронно, но вызывает async внутри ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook_handler():
    update_data = request.get_json()

    if update_data is None:
        return "no update"

    update = types.Update(**update_data)

    # Запускаем async обработку
    asyncio.run(dp.feed_update(bot, update))

    return "ok"


# --- Установка webhook ---
@app.before_first_request
def setup_webhook():
    async def set_hook():
        await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

    asyncio.run(set_hook())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
