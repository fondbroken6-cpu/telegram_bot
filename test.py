from aiogram import Bot, Dispatcher, types
import asyncio
import os

BOT_TOKEN = os.getenv("8725166562:AAEF5MWJ7Wh2QjkVgEBEu07OrZ-2rug2auY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.channel_post()
async def get_chat_id(message: types.Message):
    print("CHANNEL:", message.chat.title)
    print("ID:", message.chat.id)
    print("------")

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
