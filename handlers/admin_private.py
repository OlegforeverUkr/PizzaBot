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



#_____________________________________Код ниже для машины состояний______________________________________________


class AddProduct(StatesGroup):               # Создаем класс, наследуясь от StatesGroup и прописываем все состояния
    name = State()
    description = State()
    price = State()
    image = State()

    text = {
        'AddProduct:name': "Введите название заново",
        'AddProduct:description': "Введите описание заново",
        'AddProduct:price': "Введите цену заново",
        'AddProduct:image': "Этот шаг последний, поэтому ...",
    }



#_____________________________________Хендлеры отмена и команды назад_______________________________________


@admin_router.message(StateFilter('*'), Command("назад"))              # Добавляем проверку состояния, и выбираем любое состояние
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()                            # Получаем текущее состояние юзера

    if current_state == AddProduct.name:
        await message.answer('Предидущего шага нет, или введите название товара или введите "отмена"')
        return

    previous = None                                                    # Вводим переменную для получения стейта
    for step in AddProduct.__all_states__:                             # Проходим циклом по всем стейтам
        if step.state == current_state:                                # Находим соответствующий нашему состоянию стейт
            await state.set_state(previous)                            # Меняем текущее состояние на предудыщее(так как в переменной еще не поменян стейт на текущий)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{AddProduct.text[previous.state]}")
            return
        previous = step                                                # Если наш стейт не равен текущеми, то записываем в переменную стейт из цикла




@admin_router.message(StateFilter("*"), Command("отмена"))              # Добавляем проверку состояния, и выбираем любое состояние
@admin_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = state.get_state()                                   # Получаем текущее состояние юзера

    if current_state is None:                                           # Если его нет, просто продолжаем работу
        return

    await state.clear()                                                 # Если есть, то сбрасываем его и возвращаем админ клавиатуру
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)




#_____________________________________Хендлеры для ввода нового товара______________________________________


@admin_router.message(StateFilter(None), F.text == "Добавить товар")    # Добавляем StateFilter для проверки того, что у юзера сейчас нет активного состояния
async def add_product(message: types.Message, state: FSMContext):       # Добавляем  state: FSMContext для получения состояния юзера(aiogram прокидывает автоматом
    await message.answer("Введите название товара", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)                              # Ставим нашего юзера в состояние ввода названия товара




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

    try:                                                                # Добавляем проверку цены на валидный ввод числа
        float(message.text)
    except ValueError:
        await message.answer("Введите корректное значение цены")
        return

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
