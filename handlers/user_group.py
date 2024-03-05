from string import punctuation
from aiogram import types, Router
from filters.chat_types import ChatTypeFilter
from filters.ban_words import read_bad_words

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if read_bad_words().intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, соблюдайте порядок в чате!")
        await message.delete()
        # await message.chat.ban(user_id=message.from_user.id, until_date=datetime.datetime.now() + datetime.timedelta(days=1))