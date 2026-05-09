from aiogram import Bot, Dispatcher, types
import asyncio

BOT_TOKEN = "8725166562:AAEF5MWJ7Wh2QjkVgEBEu07OrZ-2rug2auY"
SOURCE_CHANNEL = -1003343428375

TARGET_CHANNELS = {
    "@testkanal1052": "https://t.me/testkanal1052"
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.channel_post()
async def autopost(message: types.Message):
    if message.chat.id != SOURCE_CHANNEL:
        return

    text = message.caption or message.text or ""

    for channel, link in TARGET_CHANNELS.items():
        final_text = f"{text}\n\n👉 Kanalga o'tish:\n{link}"

        if message.text:
            await bot.send_message(chat_id=channel, text=final_text)

        elif message.photo:
            await bot.send_photo(
                chat_id=channel,
                photo=message.photo[-1].file_id,
                caption=final_text
            )

        elif message.video:
            await bot.send_video(
                chat_id=channel,
                video=message.video.file_id,
                caption=final_text
            )

async def main():
    await dp.start_polling(bot)

asyncio.run(main())