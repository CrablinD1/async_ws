import asyncio
from datetime import datetime

import aiofiles


async def wait_for_data():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5000)
    print(f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S")}] Установлено соединение')

    while True:
        try:
            data = await reader.readline()
            text = f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S")}] {data.decode()}'
            async with aiofiles.open("chat_logs.txt", "a+") as chat_file:
                await chat_file.write(text)
            print(text)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError) as exc:
            await asyncio.sleep(1)
            print(f'connection error {exc=}')
            continue

asyncio.run(wait_for_data())
