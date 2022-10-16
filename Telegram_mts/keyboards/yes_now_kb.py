from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')
b4 = KeyboardButton('/Помощь')

kb_answer = ReplyKeyboardMarkup(resize_keyboard=True)

kb_answer.row(button_yes, button_no).add(b4)