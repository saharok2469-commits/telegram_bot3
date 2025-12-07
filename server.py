import os
import asyncio
from flask import Flask, request
from aiogram import types
from bot import bot, dp

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # https://telegram-bot3.onrender.com
WEBHOOK_PATH = "/webhook"


@app.route("/")
def home():
    return "Bot is running!"


# --- Webhook handler (Flask должен быть sync) ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook_handler():
    update_data = request.get_json()

    if update_data is None:
        return "no update"

    update = types.Update(**update_data)

    asyncio.run(dp.feed_update(bot, update))
    return "ok"


# --- Установка webhook при импорте модуля ---
async def setup_webhook():
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)


# Запускаем установку webhook ПРИ ЗАГРУЗКЕ серверного модуля
asyncio.get_event_loop().run_until_complete(setup_webhook())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
