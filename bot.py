from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
import os

TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Webhook работает! 🚀")


@router.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")
