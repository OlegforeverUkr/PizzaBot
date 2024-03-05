from aiogram.filters import CommandStart, Command
from aiogram import types, Router

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать в нашу пиццерию, рады Вас видеть!!!")


@user_private_router.message(Command("menu"))
async def menu_command(message: types.Message):
    await message.answer("Вот наше меню:")
