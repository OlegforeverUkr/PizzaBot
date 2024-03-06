from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F
from filters.chat_types import ChatTypeFilter
from keyboards.reply_kbrd import get_keyboard
from aiogram.utils.formatting import as_list, as_marked_section, Bold


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))



@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(                             #Добавляем клавиатуру сделанной функцией
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        )
    )





@user_private_router.message(or_f(Command("menu"), F.text.lower().contains('меню')))   # Добавляем условия срабатывания хендлера(или команда меню или текст, содержащий слово меню
async def menu_command(message: types.Message):
    await message.answer("<b>Вот наше меню:</b>")




@user_private_router.message(or_f(Command("about"), F.text.lower().contains("магазин")))
async def menu_command(message: types.Message):
    await message.answer("O нас - ")





@user_private_router.message(or_f(Command("payment"), F.text.lower().contains("оплат")))
async def menu_command(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении (карта/кеш)",
        "В заведении",
        marker="💲"
    )
    await message.answer(text.as_html())                    # Создаем промаркерованный и передаем в ответ, как html обязательно





@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def menu_command(message: types.Message):
    text = as_list(                                        # Создаем список отправляемого юзеру, разделяя его -------
        as_marked_section(
            Bold("Варианты доставки заказа:"),
            "Курьером",
            "Самовывоз",
            "Покушаю в заведении",
            marker="✅"
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Укрпочта",
            "Новая Почта",
            "Голуби",
            marker="❌"
        ),
        sep="\n----------------------------------------\n"
    )
    await message.answer(text.as_html())






@user_private_router.message(F.location)
async def menu_command(message: types.Message):
    await message.answer("Локация получена")
    await message.answer(str(message.location))


@user_private_router.message(F.contact)
async def menu_command(message: types.Message):
    await message.answer("Локация получена")
    await message.answer(str(message.contact))
