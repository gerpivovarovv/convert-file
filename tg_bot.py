from api_token import tg_token
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from converter import upload
import os


TOKEN = tg_token

dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")
    await message.answer("Пришли pdf файл а я сделаю из него odt")


@dp.message()
async def file_convert(message: Message) -> None:
    try:
        file_id = message.document.file_id
        print(file_id)
        await Bot.download(bot, file_id, "test.pdf", 120)
        await message.answer('Круто)')
        upload()
        os.remove('test.pdf')
        await message.answer_document(document=FSInputFile('my-converted-file.odt'))
        os.remove('my-converted-file.odt')

    except AttributeError:
        await message.answer("Пришли pdf файл")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())