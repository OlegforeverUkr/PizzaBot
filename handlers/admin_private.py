from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply_kbrd import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Я так, просто посмотреть зашел",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)



@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)



@admin_router.message(F.text == "Я так, просто посмотреть зашел")
async def starring_at_product(message: types.Message):
    await message.answer("ОК, вот список товаров")



@admin_router.message(F.text == "Изменить товар")
async def change_product(message: types.Message):
    await message.answer("ОК, вот список товаров")



@admin_router.message(F.text == "Удалить товар")
async def delete_product(message: types.Message):
    await message.answer("Выберите товар(ы) для удаления")





#Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):               # Создаем класс, наследуясь от StatesGroup и прописываем все состояния
    name = State()
    description = State()
    price = State()
    image = State()



@admin_router.message(StateFilter(None), F.text == "Добавить товар")    # Добавляем StateFilter для проверки того, что у юзера сейчас нет активного состояния
async def add_product(message: types.Message, state: FSMContext):       # Добавляем  state: FSMContext для получения состояния юзера(aiogram прокидывает автоматом
    await message.answer("Введите название товара", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)                              # Ставим нашего юзера в состояние ввода названия товара



@admin_router.message(Command("отмена"))
@admin_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)



@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"ок, вы вернулись к прошлому шагу")



@admin_router.message(StateFilter(AddProduct.name), F.text)             # Приверяем юзера на состояние ввода названия товара
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)                          # Берем из сообщения текст и вносим его в словарь с ключем name
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)                       # Меняем состояние юзера на следующее



@admin_router.message(StateFilter(AddProduct.description), F.text)      # Приверяем юзера на состояние ввода описания товара
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)                   # Берем из сообщения текст и вносим его в словарь с ключем description
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)                             # Меняем состояние юзера на следующее



@admin_router.message(StateFilter(AddProduct.price), F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)



@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)            # Берем отправленное фото и вносим его в имейдж(-1 значит берем последнее фото- самого высокого качества)
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()                                       # Получаем все данные в словарь
    await message.answer(str(data))                                     # Отправляем все полученные данные
    await state.clear()                                                 # Сбрасываем машину состояний