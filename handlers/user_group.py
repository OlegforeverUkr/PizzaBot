from string import punctuation
from aiogram import types, Router, Bot, F
from filters.chat_types import ChatTypeFilter
from filters.ban_words import read_bad_words


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))



"""
Создадим функцию, которая по тексту "1" проверит, является ли юзер админом, 
добаляя его в список админов, давая возможность использовать админку в личном чате с ботом
"""

@user_group_router.message(F.text == "1")
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.all_admin_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()




def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if read_bad_words().intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, соблюдайте порядок в чате!")
        await message.delete()
        # await message.chat.ban(user_id=message.from_user.id, until_date=datetime.datetime.now() + datetime.timedelta(days=1))