import os

from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F, Bot
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_qwery import orm_get_all_products, orm_add_to_cart, orm_add_user, orm_get_user_carts, Paginator

from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from keyboards.inline_kbrd import get_callback_btns, MenuCallBack
from keyboards.reply_kbrd import get_keyboard
from aiogram.utils.formatting import as_list, as_marked_section, Bold



user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))



@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)



async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Товар добавлен в корзину.")




@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):

    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()



#___________________________________________Далее идет оплата_______________________________________

@user_private_router.callback_query(F.data == "order_button")
async def pay_for_product(callback: types.CallbackQuery, session: AsyncSession, bot):
    carts = await orm_get_user_carts(session=session, user_id=callback.from_user.id)

    total_price = round(sum(cart.quantity * cart.product.price for cart in carts), 2)
    product_in_cart = [i.product.name for i in carts]
    photo_pay = 'https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcSVhJ46pOBVylg5_ZnYilSr14xSgJwSZ386f8C6hRKrA0MRiCpn2ozG-Bfcxa3bSdJ-'

    if total_price >= 300:
        cost_delivery = 0
    else:
        cost_delivery = 50

    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Покупка через телеграмм",
        description="Пробная оплата через ТГ Бота",
        payload="Внутренняя инфа для статистики или тд...",
        provider_token=f"{os.getenv('PAY_TOKEN')}",
        currency="UAH",
        prices=[
            LabeledPrice(
                label="Стоимость заказа",
                amount=total_price*100
            ),
            LabeledPrice(
                label="Доставка",
                amount=cost_delivery
            )
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        provider_data=None,
        photo_url=photo_pay,
        photo_size=100,
        photo_width=417,
        photo_height=626,
        need_name=True,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,  # Меняется ли адрес доставки
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,  # Зависит ли конечгая цена от способа доставки
        disable_notification=True,  # Доставка сообщения без звука
        protect_content=False,
        reply_to_message_id=False,  # Ответить на сообщение
        allow_sending_without_reply=True,
        reply_markup=None,  # Отправить еще одну клавиатуру(1м должно быть ОПЛАТИТЬ)
        request_timeout=30
    )


async def pre_check(pre_check_qwery: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_check_qwery.id, ok=True)



async def succsess_pay(message: Message):
    answ = f"{message.from_user.first_name}, спасибо за оплату!"
    await message.answer(answ)




"""
_________________________________Ниже код до обновления бота под новый формат_________________________

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
async def menu_command(message: types.Message, session: AsyncSession):
    await message.answer("<b>Вот наше меню:</b>")
    for product in await orm_get_all_products(session=session):               # Получаем все продукты из БД, предавая сессию
        await message.answer_photo(
            photo=product.image,                                              # Отвечаем юзеру фоткой из бд, передаем название, описание и цену
            caption=f"<strong>{product.name}</strong>\n"
                    f"{product.description}\n"
                    f"Стоимость - {round(product.price, 2)}"                  # Округляем стоимость до 2х знаков
        )




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
"""