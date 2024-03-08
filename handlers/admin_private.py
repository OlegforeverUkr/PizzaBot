from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_qwery import orm_add_product, orm_get_all_products

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply_kbrd import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)



@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)



@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):

    for product in await orm_get_all_products(session=session):               # Получаем все продукты из БД, предавая сессию
        await message.answer_photo(
            photo=product.image,                                              # Отвечаем юзеру фоткой из бд, передаем название, описание и цену
            caption=f"<strong>{product.name}</strong>\n"
                    f"{product.description}\n"
                    f"Стоимость - {round(product.price, 2)}"                  # Округляем стоимость до 2х знаков
        )




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


@admin_router.message(StateFilter(AddProduct.name))                     # После каждого хендлера делаем второй для проверки правильности ввода данных на предыдущем шаге
async def add_name(message: types.Message):
    await message.answer("Введите корректные данные описание товара")



@admin_router.message(StateFilter(AddProduct.description), F.text)      # Приверяем юзера на состояние ввода описания товара
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)                   # Берем из сообщения текст и вносим его в словарь с ключем description
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)                             # Меняем состояние юзера на следующее



@admin_router.message(StateFilter(AddProduct.description))
async def add_name(message: types.Message):
    await message.answer("Введите корректные данные описания товара")




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


@admin_router.message(StateFilter(AddProduct.price))
async def add_name(message: types.Message):
    await message.answer("Введите корректные данные значение цены товара")



@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    await state.update_data(image=message.photo[-1].file_id)            # Берем отправленное фото и вносим его в имейдж(-1 значит берем последнее фото- самого высокого качества)
    data = await state.get_data()                                       # Получаем все данные в словарь

    try:
        await orm_add_product(session=session, data=data)               # Передаем данные из машины состояний в функцию по добавлению данных в БД
        await message.answer("Данные внесены в БД",                # Отвечаем, что данные внесены
                             reply_markup=ADMIN_KB)
        await state.clear()                                             # Сбрасываем машину состояний
    except Exception as e:
        await message.answer(
            f"Произошла ошибка при добавлении товара в БД\n"
            f"{e}\n"
            f"Обратитесь за помощью к главному админу"
        )
        await state.clear()



@admin_router.message(StateFilter(AddProduct.image))
async def add_name(message: types.Message):
    await message.answer("Введите корректное изображение")