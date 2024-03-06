from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder




def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона"
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)



"""                                         Простое создание клавиатур

start_kbrd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),                   # Делаем два списка в клавиатуре, для отображения в 2 ряда(каждый список - новый ряд)
            KeyboardButton(text="О магазине"),
        ],
        [
            KeyboardButton(text="Варианты оплаты"),
            KeyboardButton(text="Варианты доставки"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что Вас интересует?"
)

____________________________________________________________________________________________________________

# Удаляем клавиатуру, после нажатия

delete_kbrd = ReplyKeyboardRemove()

____________________________________________________________________________________________________________

# Второй вариант создания клавиатуры

start_kb_2 = ReplyKeyboardBuilder()
start_kb_2.add(
    KeyboardButton(text="Меню"),
             KeyboardButton(text="О магазине"),
             KeyboardButton(text="Варианты доставки"),
             KeyboardButton(text="Варианты оплаты"),
)
start_kb_2.adjust(2, 2)                                     # явно указываем размер клавиатуры

____________________________________________________________________________________________________________


                                          Добавление к существующей клавиатуре дополнительные кнопки

start_kb_3 = ReplyKeyboardBuilder()
start_kb_3.attach(start_kb_2)
start_kb_3.add(KeyboardButton(text="Оставить отзыв"))
start_kb_3.adjust(2, 2, 1)

____________________________________________________________________________________________________________

                                   Или добавлени кнопки методом row, который новую кнопку автоматически добавляет в новый ряд

start_kb_3 = ReplyKeyboardBuilder()
start_kb_3.attach(start_kb_2)
start_kb_3.row(KeyboardButton(text="Оставить отзыв"))

____________________________________________________________________________________________________________

                                               Тестовая клавиатура для отправки контакта и локации

test_kbrd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать опрос", request_poll=KeyboardButtonPollType())
        ],
        [
            KeyboardButton(text="Отпраавить номер ☎", request_contact=True),
            KeyboardButton(text="Отпраавить локацию 🚩", request_location=True)
        ]
    ],
    resize_keyboard=True
)
"""


