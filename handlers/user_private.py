from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F
from filters.chat_types import ChatTypeFilter


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать в нашу пиццерию, рады Вас видеть!!!")


@user_private_router.message(or_f(Command("menu"), F.text.lower().contains('меню')))
async def menu_command(message: types.Message):
    await message.answer("Вот наше меню:")


@user_private_router.message(Command("about"))
async def menu_command(message: types.Message):
    await message.answer("O нас - ")


@user_private_router.message(Command("payment"))
async def menu_command(message: types.Message):
    await message.answer("Варианты оплаты - ")


@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def menu_command(message: types.Message):
    await message.answer("Варианты доставки - ")

