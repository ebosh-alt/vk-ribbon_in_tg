from asyncio import run

from config import *
from telethon import TelegramClient


async def F():
    data = load_object()
    print(data.data)
    client = TelegramClient("assahit", api_id, api_hash)
    await client.start(phone=phone_number)
    count = -1
    for i in data.data:
        count += 1
        channel = data.get_elem(i)
        if len(channel.list_object) != 0:
            for obj in channel.list_object:
                print(obj)

                await client.download_media(message=obj, file=f'./rec/{count}')

    await client.disconnect()

# MessageMediaPhoto(photo=Photo(id=5307569079881678029, access_hash=497137054372013160, file_reference=b'\x02n\x12\xf6\xd7\x00\x00\x00>c?J\xc7s\xf6!\x19\x82\xba$\x0e\x9fLL\x00s\xad\xdc}', date=datetime.datetime(2022, 9, 28, 22, 59, 5, tzinfo=datetime.timezone.utc), sizes=[PhotoStrippedSize(type='i', bytes=b'\x01\x17(\xc5\xa2\x8a(\x00\xa2\xa5a\x16\xd1\xb7y8\xe78\x00\x1a\x8e\x80\x12\x8a(\xa0\x02\x8a(\xa0\x02\x8a(\xa0\x02\x8a(\xa0\x0f'), PhotoSize(type='m', w=320, h=180, size=1638), PhotoSize(type='x', w=800, h=450, size=5807), PhotoSizeProgressive(type='y', w=1280, h=720, sizes=[3286, 7687, 7783])], dc_id=2, has_stickers=False, video_sizes=[]), ttl_seconds=None)

if __name__ == '__main__':
    run(F())
