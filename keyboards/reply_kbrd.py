from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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



# Удаляем клавиатуру, после нажатия

delete_kbrd = ReplyKeyboardRemove()



# Второй вариант создания клавиатуры

start_kb_2 = ReplyKeyboardBuilder()
start_kb_2.add(
    KeyboardButton(text="Меню"),
             KeyboardButton(text="О магазине"),
             KeyboardButton(text="Варианты доставки"),
             KeyboardButton(text="Варианты оплаты"),
)
start_kb_2.adjust(2, 2)                                     # явно указываем размер клавиатуры


"""

                                          Добавление к существующей клавиатуре дополнительные кнопки

start_kb_3 = ReplyKeyboardBuilder()
start_kb_3.attach(start_kb_2)
start_kb_3.add(KeyboardButton(text="Оставить отзыв"))
start_kb_3.adjust(2, 2, 1)


                                   Или добавлени кнопки методом row, который новую кнопку автоматически добавляет в новый ряд

start_kb_3 = ReplyKeyboardBuilder()
start_kb_3.attach(start_kb_2)
start_kb_3.row(KeyboardButton(text="Оставить отзыв"))



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


