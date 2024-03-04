import asyncio
import os
from dotenv import find_dotenv, load_dotenv

from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать в нашу пиццерию, рады Вас видеть!!!")


@dp.message()
async def start(message: types.Message):
    await message.answer(message.text)




async def main():
    await bot.delete_webhook(drop_pending_updates=True) # Удалять все входящие сообщения, пока бот не в сети
    await dp.start_polling(bot)


asyncio.run(main())
"""
Запуск
"""