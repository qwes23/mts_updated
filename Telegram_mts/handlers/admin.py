from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from create_bot import dp, bot
from keyboards import kb_reg

user_id = None


class FSMregistration(StatesGroup):
    name = State()
    surname = State()
    email = State()
    phone = State()


async def registration_command(message: types.Message):
    global user_id
    user_id = message.from_user.id
    is_registred = sqlite_db.is_registred(user_id)
    if is_registred != '':
        await bot.send_message(is_registred)
    else:
        await bot.send_message('Кажется, вы еще не зарегистрированны! Хотите?', reply_markup=kb_reg)


# Начинаем диалог регистрации
async def cm_start(message: types.Message):
    await FSMregistration.name.set()
    await message.reply('Напишите свое Имя')


# Ловим первый ответ и пишем в словарь
async def getting_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['name'] = message.text

    await FSMregistration.next()
    await message.reply('Теперь напишите свою Фамилию')


# Ловим второй ответ
async def getting_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMregistration.next()
    await message.reply('Введите ваш email')


# Ловим третий ответ
# @dp.message_handler(state =FSMadmin.description)
async def getting_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Введите ваш номер телефона")
    await FSMregistration.next()


async def getting_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        data['telegram_name'] = f'{message.from_user.first_name} {message.from_user.last_name}'
        await sqlite_db.sql_add_commend(state)
    await state.finish()


# @dp.message_handler(state="*", commands ='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(registration_command)
    dp.register_message_handler(cm_start, commands=['Регистрация'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(getting_name, state=FSMregistration.name)
    dp.register_message_handler(getting_surname, state=FSMregistration.surname)
    dp.register_message_handler(getting_email, state=FSMregistration.email)
