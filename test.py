from aiogram import Bot, Dispatcher, types
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Асосий канал
SOURCE_CHANNEL = -1003343428375

# 28 та канал намунаси
TARGET_CHANNELS = {
    -1002007912243: "https://t.me/+YuRtOBCZZQY0YWUy",
    -1002637320521: "https://t.me/+v9NPiv2Sx-EyNzAy",
    -1003177014187: "https://t.me/+TgXcSwoA9yxhOGQy",
    -1002614469635: "https://t.me/+wnRqhxjUj5xjYTZi",
    -1002824356985: "https://t.me/+-eR78TOS49JmZjAy",
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.channel_post()
async def autopost(message: types.Message):
    if message.chat.id != SOURCE_CHANNEL:
        return

    text = message.caption or message.text or ""

    for channel_id, link in TARGET_CHANNELS.items():
        final_text = f"{text}\n\n📢 Kanalga o'tish:\n{link}"

        try:
            if message.text:
                await bot.send_message(channel_id, final_text)

            elif message.photo:
                await bot.send_photo(
                    chat_id=channel_id,
                    photo=message.photo[-1].file_id,
                    caption=final_text
                )

            elif message.video:
                await bot.send_video(
                    chat_id=channel_id,
                    video=message.video.file_id,
                    caption=final_text
                )

            await asyncio.sleep(1)

        except Exception as e:
            print(f"XATO: {channel_id} -> {e}", flush=True)


async def main():
    print("BOT IS STARTED", flush=True)
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())
