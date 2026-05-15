from aiogram import Bot, Dispatcher, types
import asyncio
import os
import json
from aiogram.types import InputMediaPhoto, InputMediaVideo

BOT_TOKEN = os.getenv("BOT_TOKEN")

SOURCE_CHANNEL = -1003343428375

TARGET_CHANNELS = {
    -1002007912243: "https://t.me/+YuRtOBCZZQY0YWUy",
    -1002637320521: "https://t.me/+v9NPiv2Sx-EyNzAy",
    -1003177014187: "https://t.me/+TgXcSwoA9yxhOGQy",
    -1002614469635: "https://t.me/+wnRqhxjUj5xjYTZi",
    -1002824356985: "https://t.me/+-eR78TOS49JmZjAy",
    -1003493579355: "https://t.me/+dcX5tYMPtcA1YzU6",
    -1003623837970: "https://t.me/+VgV55NSNKw80ODli",
    -1003886419785: "https://t.me/+s01-u71_XogxZWU6",
    -1003414227082: "https://t.me/+0w3ahgPDehAzNjYy",
    -1003368706043: "https://t.me/+AgDci7pLEY9mZTky",
    -1003780415472: "https://t.me/+uHY32407zQU3NTAy",
    -1003643301934: "https://t.me/+JZga3RuScM84OGZi",
    -1003842841166: "https://t.me/+NwYyKwkAK94wZDUy",
    -1003982964898: "https://t.me/+A0SirOh2eTxlZWUy",
    -1003997267876: "https://t.me/+oK2Z35wEFKhjNTQ6",
    -1003937855384: "https://t.me/+gfvTDkZO3_tkZGYy",
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

queue_lock = asyncio.Lock()
albums = {}
message_map = {}

MAP_FILE = "message_map.json"


def load_map():
    global message_map
    try:
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            message_map = json.load(f)
    except:
        message_map = {}


def save_map():
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(message_map, f, ensure_ascii=False, indent=2)


async def send_single(message: types.Message):
    text = message.caption or message.text or ""
    source_id = str(message.message_id)
    message_map[source_id] = []

    for channel_id, link in TARGET_CHANNELS.items():
        final_text = f"{text}\n\n📢 Kanalga o'tish:\n{link}"

        try:
            sent = None

            if message.text:
                sent = await bot.send_message(channel_id, final_text)

            elif message.photo:
                sent = await bot.send_photo(
                    chat_id=channel_id,
                    photo=message.photo[-1].file_id,
                    caption=final_text
                )

            elif message.video:
                sent = await bot.send_video(
                    chat_id=channel_id,
                    video=message.video.file_id,
                    caption=final_text
                )

            elif message.document:
                sent = await bot.send_document(
                    chat_id=channel_id,
                    document=message.document.file_id,
                    caption=final_text
                )

            if sent:
                message_map[source_id].append({
                    "chat_id": channel_id,
                    "message_id": sent.message_id
                })

            await asyncio.sleep(1)

        except Exception as e:
            print(f"XATO: {channel_id} -> {e}", flush=True)

    save_map()


async def send_album(media_group_id):
    await asyncio.sleep(1.5)

    messages = albums.pop(media_group_id, [])
    messages.sort(key=lambda m: m.message_id)

    if not messages:
        return

    first = messages[0]
    text = first.caption or ""
    source_id = str(first.message_id)
    message_map[source_id] = []

    for channel_id, link in TARGET_CHANNELS.items():
        media = []

        for index, msg in enumerate(messages):
            caption = ""

            if index == 0:
                caption = f"{text}\n\n📢 Kanalga o'tish:\n{link}"

            if msg.photo:
                media.append(InputMediaPhoto(
                    media=msg.photo[-1].file_id,
                    caption=caption
                ))

            elif msg.video:
                media.append(InputMediaVideo(
                    media=msg.video.file_id,
                    caption=caption
                ))

        try:
            sent_messages = await bot.send_media_group(
                chat_id=channel_id,
                media=media
            )

            for sent in sent_messages:
                message_map[source_id].append({
                    "chat_id": channel_id,
                    "message_id": sent.message_id
                })

            await asyncio.sleep(1)

        except Exception as e:
            print(f"ALBUM XATO: {channel_id} -> {e}", flush=True)

    save_map()


@dp.channel_post()
async def autopost(message: types.Message):
    if message.chat.id != SOURCE_CHANNEL:
        return

    async with queue_lock:
        if message.media_group_id:
            group_id = message.media_group_id

            if group_id not in albums:
                albums[group_id] = []
                asyncio.create_task(send_album(group_id))

            albums[group_id].append(message)

        else:
            await send_single(message)


@dp.message()
async def delete_command(message: types.Message):
    if not message.text:
        return

    if not message.text.startswith("/del"):
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Format: /del POST_ID")
        return

    source_id = parts[1]

    if source_id not in message_map:
        await message.answer("Bu POST_ID topilmadi")
        return

    for item in message_map[source_id]:
        try:
            await bot.delete_message(
                chat_id=item["chat_id"],
                message_id=item["message_id"]
            )
        except Exception as e:
            print(f"DELETE XATO: {e}", flush=True)

    del message_map[source_id]
    save_map()

    await message.answer("O'chirildi ✅")


async def main():
    load_map()
    print("BOT IS STARTED", flush=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
