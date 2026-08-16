from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from os import getenv
from dotenv import load_dotenv
from googletrans import Translator
from googletrans.models import Translated

import asyncio
import logging
import sys

load_dotenv()
TOKEN = getenv("TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN)
translator = Translator()

@dp.message(CommandStart())
async def handle_start(msg: Message) -> None:
    await bot.send_message(msg.chat.id, "🇷🇺 Привет! Извините, пока что этот бот не предназначен для использования в ЛС. Добавте его в канал, и он будет переводить сообщения на русский.\n🇺🇸 Hello! Sorry, but this bot is not supposed for DM use. Add it into your channel and it will translate your messages to russian.")

@dp.channel_post()
async def translate(msg: Message) -> None:
    txt = msg.text or msg.caption
    if not txt:
        return

    translated = await translator.translate(txt, dest = "ru")
    new_text = f"🇺🇸 {txt}\n\n🇷🇺 {translated.text}"

    if msg.text:
        await msg.edit_text(new_text)
    elif msg.caption:
        await msg.edit_caption(new_text)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
