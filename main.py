import asyncio
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv
from aiogram import Dispatcher, Bot, F

load_dotenv(find_dotenv())

from database.engine import session_maker                             # Импорт функций создания сессии
from middlewares.db import DataBaseSession                            # Импорт мидлвары, которая будет пробрасывать сессию во все события
from database.start_shutdown import on_startup, on_shutdown           # Импорт функций создания БД(по необходимости) и остановки БД

from handlers.user_private import user_private_router, \
    pre_check, succsess_pay  # Импортируем роутеры для общения с пользовательскими сообщениями

from handlers.user_group import user_group_router                     # Импортируем роутер для общения с пользователями в группе
from handlers.admin_private import admin_router                       # Импортируем роутер для общения с админом

from aiogram.enums import ParseMode, ContentType

# ALLOW_UPDATES = ["message", "edited_message"]   - Делаем список, добавляя методы, которые будет обрабатывать наш бот (await dp.start_polling(bot, allowed_updates=ALLOW_UPDATES))


bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Выбираем парс мод  для всего бота
bot.all_admin_list = []


dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)



async def main():
    dp.startup.register(on_startup)                                      # Запускаем создание базы данных
    dp.shutdown.register(on_shutdown)                                    # Останавливаем базу данных (опционально)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))    # Вешаем сессию на все обновления(можно отдельно на роутер админа, роутер привата и т д...)

    dp.pre_checkout_query.register(pre_check)
    dp.message.register(succsess_pay, F.content_type == ContentType.SUCCESSFUL_PAYMENT)


    await bot.delete_webhook(drop_pending_updates=True)                  # Удалять все входящие сообщения, пока бот не в сети

    # await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())   Добавляем к боту команды, а также выставляем зону их отображения
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())     # Указываем какие обновления будет обрабатывать наш ТГ бот (без данных будет обрабатывать все, а skip_events- для ограничения на обработку)


asyncio.run(main())
