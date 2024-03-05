import asyncio
import os

from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv
from aiogram import Dispatcher, Bot

load_dotenv(find_dotenv())
from handlers.user_private import user_private_router                 # Импортируем роутеры для общения с пользовательскими сообщениями
from commands.bot_cmds_list import private


ALLOW_UPDATES = ["message", "edited_message"]




bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(user_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)                   # Удалять все входящие сообщения, пока бот не в сети
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())  # Добавляем к боту команды, а также выставляем зону их отображения
    await dp.start_polling(bot, allowed_updates=ALLOW_UPDATES)     # Указываем какие обновления будет обрабатывать наш ТГ бот


asyncio.run(main())
