from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_reg = KeyboardButton('/Регистрация')

kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)

kb_reg.add(button_reg)