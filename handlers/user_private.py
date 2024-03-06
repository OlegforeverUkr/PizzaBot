from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F
from filters.chat_types import ChatTypeFilter
from keyboards import reply_kbrd
from aiogram.enums import ParseMode


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))



@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в нашу пиццерию, рады Вас видеть!!!",
        reply_markup=reply_kbrd.test_kbrd)                                        #Добавляем клавиатуру для отправки



@user_private_router.message(or_f(Command("menu"), F.text.lower().contains('меню')))   # Добавляем условия срабатывания хендлера(или команда меню или текст, содержащий слово меню
async def menu_command(message: types.Message):
    await message.answer(
        "<b>Вот наше меню:</b>",
        parse_mode=ParseMode.HTML)                                                 # Выбираем парс мод  для каждого хендлера для обработки текста в ответах (жирный, курсив ...)



@user_private_router.message(or_f(Command("about"), F.text.lower().contains("магазин")))
async def menu_command(message: types.Message):
    await message.answer("O нас - ")




@user_private_router.message(or_f(Command("payment"), F.text.lower().contains("оплат")))
async def menu_command(message: types.Message):
    await message.answer("Варианты оплаты - ")




@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def menu_command(message: types.Message):
    await message.answer("Варианты доставки - ")





@user_private_router.message(F.location)
async def menu_command(message: types.Message):
    await message.answer("Локация получена")
    await message.answer(str(message.location))

@user_private_router.message(F.contact)
async def menu_command(message: types.Message):
    await message.answer("Локация получена")
    await message.answer(str(message.contact))
