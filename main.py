import asyncio
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import aiofiles
from pydantic.main import BaseModel


class AppParams(BaseModel):
    history: Path
    port: int
    host: str


async def read_chat(app_config: AppParams):
    reader, writer = await asyncio.open_connection(app_config.host, app_config.port)
    print(f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S")}] Установлено соединение')

    while True:
        try:
            data = await reader.readline()
            text = f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S")}] {data.decode()}'
            async with aiofiles.open(app_config.history, "a+") as chat_file:
                await chat_file.write(text)
            print(text)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError) as exc:
            await asyncio.sleep(1)
            print(f'connection error {exc=}')
            continue


if __name__ == '__main__':
    parser = ArgumentParser(description='async ws')

    parser.add_argument('--host', type=str, default='minechat.dvmn.org', help='Host')
    parser.add_argument('--port', type=int, default=5000, help='Port')
    parser.add_argument(
        '--history',
        default='chat_history.txt',
        type=Path,
        help='Path to log file',
    )
    config = AppParams.parse_obj(parser.parse_args().__dict__)

    asyncio.run(read_chat(config))
