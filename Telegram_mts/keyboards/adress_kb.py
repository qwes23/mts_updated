from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Назначить')
b2 = KeyboardButton('/Меню')
b4 = KeyboardButton('/Помощь')

kb_adress = ReplyKeyboardMarkup(resize_keyboard=True)

kb_adress.add(b1).add(b2).add(b4)