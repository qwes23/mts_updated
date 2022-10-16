from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Инструкция')
b2 = KeyboardButton('/Проверки рядом со мной', request_location=True)
b3 = KeyboardButton('/Мои_проверки')
b4 = KeyboardButton('/Помощь')
b5 = KeyboardButton('/Оплата')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b3, b1).add(b2).row(b4, b5)