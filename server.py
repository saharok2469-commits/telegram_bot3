import os
from flask import Flask, request
from bot import dp, bot
import asyncio
from aiogram import types

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # твой URL будет в переменной


@app.route("/")
def home():
    return "Bot is running via webhook!"


# --- Telegram webhook handler ---
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook_handler():
    update_data = request.get_json()

    if update_data is None:
        return "no update"

    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return "ok"


# --- Установка webhook при старте ---
@app.before_first_request
def set_webhook():
    asyncio.get_event_loop().create_task(
        bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
