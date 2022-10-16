from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Заполнить_анкету')
b2 = KeyboardButton('/Снять_себя_с_проверки')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('/Помощь')

kb_list = ReplyKeyboardMarkup(resize_keyboard=True)

kb_list.add(b1).add(b2).row(b3, b4)