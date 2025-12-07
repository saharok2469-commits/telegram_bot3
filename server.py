import os
import asyncio
from flask import Flask, request
from bot import dp, bot
from aiogram import types

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # https://your-name.onrender.com


@app.route("/")
def home():
    return "Bot running via webhook"


# ---------- ГЛАВНОЕ ИСПРАВЛЕНИЕ ----------
# вместо asyncio.run → запускаем ручной event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@app.post(WEBHOOK_PATH)
def webhook_handler():
    update_data = request.get_json()

    if not update_data:
        return "no update"

    update = types.Update(**update_data)

    # запускаем async внутри loop, НО БЕЗ asyncio.run !!!
    loop.create_task(dp.feed_update(bot, update))

    return "ok"
# ------------------------------------------


# ставим webhook ПРАВИЛЬНО
@app.before_request
def setup_webhook():
    if request.path == "/":  # выполняем только один раз
        loop.create_task(bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
