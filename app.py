import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from aiogram import Dispatcher, Bot
load_dotenv(find_dotenv())
from handlers.user_private import user_private_router                 # Импортируем роутеры для общения с пользовательскими сообщениями


ALLOW_UPDATES = ["message", "edited_message"]


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(user_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)                   # Удалять все входящие сообщения, пока бот не в сети
    await dp.start_polling(bot, allowed_updates=ALLOW_UPDATES)     # Указываем какие обновления будет обрабатывать наш ТГ бот


asyncio.run(main())
