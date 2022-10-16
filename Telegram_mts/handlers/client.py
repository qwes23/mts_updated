from datetime import datetime
from pydoc import describe
import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import  dp, bot

from data_base import sqlite_db

from keyboards import kb_client
from keyboards import kb_adress
from keyboards import kb_reg, kb_list
from keyboards import kb_answer


async def command_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветсвуем вас в боте Profpoint_mts!', reply_markup=kb_client)
    
async def helper(message: types.Message):
    user_id = message.from_user.id
    registration_data = sqlite_db.help(user_id)
    admin_id = 708697982
    await bot.send_message(message.from_user.id, f'Мы спешим на помощь! Скоро с вами свяжется наш менеджер, по оставленной вами почте {registration_data}.', reply_markup=kb_client)
    await bot.send_message(admin_id, f'Пользователю {user_id} нужна ваша помощь! Свяжитесь с ним по почте {registration_data} как можно скорее.')
    
async def oplata(message: types.Message):
    await bot.send_message(message.from_user.id, '''
    Оплата за все проверки прошлого месяца суммируется и начисляется к 15-му числу текущего месяца. Например, за все работы, которые вы выполнили в октябре, оплата будет начислена к 15-му ноября.

15-го числа каждого месяца Вам на почту приходит письмо, в котором указана заработанная сумма за прошлый месяц.

Оплата будет осуществляться трем категориям получателей:

«Самозанятый» на Qugo - дополнительный налог 6% уплачивается самостоятельно,

«Физическое лицо» на Solar Staff - оплата начисляется за вычетом 7%

ИП на Solar Staff – налог выплачивается самостоятельно в зависимости от системы налогооблажения ИП
                           
                           ''', reply_markup=kb_client)
    
async def command_info(message: types.Message):
    await bot.send_message(message.from_user.id, '''
    Приветствуем вас в боте Profpoint_салоны связи! Бот позволяет найти ближайшие свободные проверки и самостоятельно назначить себя на их выполнение.

Для того, что бы бот работал корректно, используйте предлагаемые им варианты ответов или команды: /start (для возврата к началу), /мои_проверки (чтобы увидеть Ваши проверки) и т.д. Все команды указаны внизу, в меню. Если во время ответов на вопросы анкеты вы понимаете, что ответили некорректно, напишите команду Отмена - заполнение анкеты обнулится.

Рекомендуем использовать смартфон или планшет, для того, что бы бот мог предлагать вам ближайшие к вам адреса.
После того, как вы выберите проверки, которые планируете выполнить - они будут закреплены за вами на 48 часов.
Вы можете снять с себя проверку, но не более 3х раз. Если вы не выполните проверки в течении 48 часов и не отмените их до истечения этого времени - вы будете заблокированы и не сможете более выполнять проверки.
После выполнения закрепленной за вами проверки - вам необходимо ответить на несколько вопросов прямо в боте. Если вы делаете это со смартфона - убедитесь, что записи с диктофона сохранены как файл.

Если у вас остались вопросы по работе бота - свяжитесь с нами по команде /Поддержка.
                           
Спасибо! И желаем Удачи.
    ''', reply_markup=kb_client)
    await message.reply_document('BQACAgIAAxkBAAMPYzFu5Fn_4xmpxTW3rKZz1HaP4BQAAuYbAAJwy4lJ86nafYyu6mMpBA')
    await message.reply_video('BAACAgIAAxkBAAMIYzFsurjC6SuMPtpctTv16_uCSagAAtYbAAJwy4lJE85GYGBz9hopBA')
    #await message.reply_document('BQACAgIAAxkBAAIGh2MkNgpLF9ARx_JUR_-P4NUgXnW0AALFIAACWvUpScOeJyNT06GOKQQ')
    
    
async def location_request(message: types.Message):
    await bot.send_message(message.from_user.id, 'reply')
    
async def location_give(message: types.Message):
    global reply
    lat = message.location.latitude
    lon = message.location.longitude
    lat1 = lat-3
    lat2 = lat+3
    lon1 = lon-3
    lon2 = lon+3
    reply = sqlite_db.get_info(lat1, lat2, lon1, lon2)
    for i in reply:
        await bot.send_message(message.from_user.id, f'Салон {i} : адрес - {reply[i][0]}, оплата: {reply[i][1]}', reply_markup=kb_adress)
        
class FSMassignation(StatesGroup):
    number_state = State()

async def take_one(message: types.Message):
    await FSMassignation.number_state.set()
    await message.reply('Напишите номер проверки:')
    
#Ловим первый ответ и пишем в словарь
async def number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    number = int(message.text)
        
    result =  sqlite_db.sql_add_number(user_id, number)
    if result == 'Вы уже назначены на 3 или более проверок. Назначение новых станет доступно после их выполнения.':
        await message.reply(result, reply_markup=kb_client)
    else:
        await message.reply(result, reply_markup=kb_client)
        await message.reply('Вот инструкция! Прочитайте ее, перед тем как выполнять проверку!')
        await message.reply_document('BQACAgIAAxkBAAMPYzFu5Fn_4xmpxTW3rKZz1HaP4BQAAuYbAAJwy4lJ86nafYyu6mMpBA') 
       
    await state.finish()


async def test(message: types.Message):
    global user_id
    user_id = message.from_user.id
    # print(user_id)
    reply1 = sqlite_db.get_mylist(user_id)
    # print(reply1)
    if len(reply1) == 0:
        await bot.send_message(message.from_user.id, 'Вы не назначены ни на одну проверку', reply_markup=kb_client)
    else:    
        await bot.send_message(message.from_user.id, 'Вы назначены на следующие проверки: ', reply_markup=kb_list)
        for i in reply1:
            await bot.send_message(message.from_user.id, f'Салон номер {i} : адрес - {reply1[i][0]}, режим работы - {reply1[i][1]}')
        await message.reply_document('BQACAgIAAxkBAAMPYzFu5Fn_4xmpxTW3rKZz1HaP4BQAAuYbAAJwy4lJ86nafYyu6mMpBA')

class FSMremove(StatesGroup):
    number_state = State()

async def remove(message: types.Message):
    await FSMremove.number_state.set()
    await message.reply('Напишите номер проверки, от которой хотите отказаться:')
    
    
#Ловим ответ и удаляем проверку у пользователя
async def remove_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    number = int(message.text)
        
    result =  sqlite_db.sql_remove_number(user_id, number)    
    await message.reply(result, reply_markup=kb_client)    
    await state.finish()




#####################################################РЕГИСТРАЦИЯ#########################################################

user_id = None

class FSMregistration(StatesGroup):
    name = State()
    surname = State()
    email = State()

async def command_start(message: types.Message):
    global user_id 
    user_id = message.from_user.id
    is_registred = sqlite_db.is_registred(user_id)
    if is_registred != '':
        await bot.send_message(message.from_user.id, f'Добрый день, {is_registred}!', reply_markup=kb_client)
    else:
        await bot.send_message(message.from_user.id, '''
        Приветствуем вас в боте Profpoint_салоны связи! Бот позволяет найти ближайшие свободные проверки и самостоятельно назначить себя на их выполнение.

Для того, что бы бот работал корректно, используйте предлагаемые им варианты ответов или команды: /start (для возврата к началу), /мои_проверки (чтобы увидеть Ваши проверки) и т.д. Все команды указаны внизу, в меню. Если во время ответов на вопросы анкеты вы понимаете, что ответили некорректно, напишите команду Отмена - заполнение анкеты обнулится.

Рекомендуем использовать смартфон или планшет, для того, что бы бот мог предлагать вам ближайшие к вам адреса.
После того, как вы выберите проверки, которые планируете выполнить - они будут закреплены за вами на 48 часов.
Вы можете снять с себя проверку, но не более 3х раз. Если вы не выполните проверки в течении 48 часов и не отмените их до истечения этого времени - вы будете заблокированы и не сможете более выполнять проверки.
После выполнения закрепленной за вами проверки - вам необходимо ответить на несколько вопросов прямо в боте. Если вы делаете это со смартфона - убедитесь, что записи с диктофона сохранены как файл.

Если у вас остались вопросы по работе бота - свяжитесь с нами по команде /Поддержка.
                           
Спасибо! И желаем Удачи.

Кажется, вы еще не зарегистрированы! Хотите?''', reply_markup=kb_reg)
        await message.reply_video('BAACAgIAAxkBAAMIYzFsurjC6SuMPtpctTv16_uCSagAAtYbAAJwy4lJE85GYGBz9hopBA')
         

#Начинаем диалог регистрации
async def cm_start(message : types.Message):
    await FSMregistration.name.set()
    await message.reply('Напишите свое Имя')
    
#Ловим первый ответ и пишем в словарь
async def getting_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['name'] = message.text
        
    await FSMregistration.next()
    await message.reply('Теперь напишите свою Фамилию')

#Ловим второй ответ
async def getting_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMregistration.next()
    await message.reply('Введите ваш email')

#Ловим третий ответ 
async def getting_email(message: types.Message, state: FSMContext):    
    async with state.proxy() as data:
        data['email'] = message.text
        
    await sqlite_db.sql_add_commend(state)    
    await message.reply('Спасибо! Теперь вы зарегистрированы', reply_markup=kb_client)  
    await state.finish()

#@dp.message_handler(state="*", commands ='отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')    


#####################################################ЗАПОЛНЕНИЕ_АНКЕТЫ#########################################################

class FSMfilling(StatesGroup):
    number = State()
    date = State()
    time_start = State()
    # time_end = State()
    # clients_operator = State()
    rezgim = State()
    number_workers = State()
    number_clients = State()
    name_worker = State()
    # dolzhnost_worker = State()
    describe_worker = State()
    # workers_look = State()
    # bad_worker_FIO = State()
    # sale_office = State()
    # bad_sale_office = State()
    resume = State()
    audio = State()
    photo1 = State()
    photo2 = State()

async def command_fill(message: types.Message):
    await FSMfilling.number.set()
    await message.reply('Напишите номер проверки:')
         
#Ловим первый ответ и пишем в словарь
async def getting_number(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['user_id'] = message.from_user.id
        data_check['number'] = int(message.text)
        data_check['date_time'] = datetime.now()
        
    await FSMfilling.next()
    await message.reply('Дата проверки. Формат 12.12.2022')

#Ловим второй ответ
async def getting_date(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['date'] = message.text
    await FSMfilling.next()
    await message.reply('Время начала проверки. Формат 17:20')
    
#Ловим четвертый ответ
async def getting_time_start(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['time_start'] = message.text
#     await FSMfilling.next()
#     await message.reply('Время окончания проверки. Формат 17:30')

# #Ловим пятый ответ
# async def getting_time_end(message: types.Message, state: FSMfilling):
#     async with state.proxy() as data_check:
#         data_check['time_end'] = message.text    
#     await FSMfilling.next()
#     await message.reply('Напишите название оператора, услугами которого вы пользуетесь.')

# async def clients_operator(message: types.Message, state: FSMfilling):
#     async with state.proxy() as data_check:
#         data_check['clients_operator'] = message.text    
    await FSMfilling.next()
    await message.reply('Салон работал согласно режиму работы?', reply_markup=kb_answer)
 
async def getting_rezgim(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['rezgim'] = message.text    
    await FSMfilling.next()
    await message.reply('Пришлите количество сотрудников, присутсвовавших во время визита')
    
async def getting_number_workers(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['number_workers'] = int(message.text)    
    await FSMfilling.next()
    await message.reply('Пришлите количество клиентов, присутсвовавших во время визита')
    
async def getting_number_clients(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['number_clients'] = int(message.text)    
    await FSMfilling.next()
    await message.reply('Пришлите Имя и Должность сотрудника, который проводил консультацию. Если не помните - напишите: не помню. Формат: Иванов Иван Иванович, консультант')
    
async def getting_name_worker(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['name_worker'] = message.text    
    await FSMfilling.next()
    await message.reply('Коротко опишите внешний вид сотрудника.')
    
# async def getting_describe_worker(message: types.Message, state: FSMfilling):
#     async with state.proxy() as data_check:
#         data_check['describe_worker'] = message.text    
#     await FSMfilling.next()
#  await message.reply('Если внешний вид сотрудника не соответствовал требованиям, укажите, что было не так. Если вид сотрудника соответствовал требованиям - напишите :ок.')
    
# async def getting_workers_look(message: types.Message, state: FSMfilling):
#     async with state.proxy() as data_check:
#         data_check['workers_look'] = message.text    
#     await FSMfilling.next()
#     await message.reply('Пришлите Имя сотрудника, который не соответствовал требованиям. Если не помните - напишите: не помню. Формат: Иванов Иван Иванович')
    
async def getting_describe_worker(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['describe_worker'] = message.text      
#     await FSMfilling.next()
#     await message.reply('Опишите внешний вид офиса продаж, чистоту, порядок, работоспособность оборудования')
    
# async def getting_sale_office(message: types.Message, state: FSMfilling):
#     async with state.proxy() as data_check:
#         data_check['sale_office'] = message.text    
#     await FSMfilling.next()
#     await message.reply('Если внешний вида офиса продаж не соответствовал требованиям, укажите, что было не так. Если ОП соответствовал требованиям - напишите :ок.')
    
# async def getting_bad_sale_office(message: types.Message, state: FSMfilling):
#     async with state.proxy() as data_check:
#         data_check['bad_sale_office'] = message.text    
    await FSMfilling.next()
    await message.reply('Напишите короткое резюме визита. Добавьте комментарии по желанию.')    
            
async def getting_resume(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['resume'] = message.text    
    await FSMfilling.next()
    await message.reply('Пришилите аудиозапись визита.')            

#Ловим шестой ответ
async def getting_audio(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['audio'] = message.audio.file_id
    await FSMfilling.next()
    await message.reply('Прикрепите фото фасада с первого ракурса.')
    
#Ловим седьмой ответ 
async def getting_photo1(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['photo1'] = message.photo[0].file_id
    await FSMfilling.next()
    await message.reply('Прикрепите фото фасада со второго ракурса.')
    
async def photo_loop(message: types.Message, state: FSMfilling):
    message_id = (await message.answer("Неверный формат сообщения.\n\nПожалуйста, пришлите фото")).message_id
    await asyncio

async def getting_photo2(message: types.Message, state: FSMfilling):
    admin_id = 708697982
    user_id = message.from_user.id
    async with state.proxy() as data_check:
        data_check['photo2'] = message.photo[0].file_id
    await sqlite_db.sql_add_check(state)    
    await message.reply(f'Спасибо! Анкета {data_check["number"]} -- заполнена!', reply_markup=kb_client)    
    await bot.send_message(admin_id, f'Пользователь {user_id}, заполнил анкету {data_check["number"]}')
    await state.finish()

#@dp.message_handler(state="*", commands ='отмена')
async def cancel_handler(message: types.Message, state: FSMfilling):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK') 
    
# async def scan_message(message: types.Message):
#     document_id = message.document.file_id
#     file_info = await bot.get_file(document_id)
#     print(f'file_id: {file_info.file_id}')
#     print(f'file_path: {file_info.file_path}')
#     print(f'file_size: {file_info.file_size}')
#     print(f'file_unique_id: {file_info.file_unique_id}')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(command_menu, commands = ['Меню'])
    # dp.register_message_handler(scan_message, content_types=['document'])
    dp.register_message_handler(test, commands = ['Мои_проверки'])
    dp.register_message_handler(command_info, commands = ['Инструкция'])
    dp.register_message_handler(location_request, commands=['Проверки рядом со мной'])
    dp.register_message_handler(location_give, content_types=["location"])
    
    dp.register_message_handler(take_one, commands=['Назначить'], state = None)
    dp.register_message_handler(number, state = FSMassignation.number_state)
    dp.register_message_handler(remove, commands=['Снять_себя_с_проверки'], state = None)
    dp.register_message_handler(remove_number, state = FSMremove.number_state)
    
    dp.register_message_handler(command_fill, commands = ['Заполнить_анкету'], state = None)
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(getting_number, state = FSMfilling.number)
    dp.register_message_handler(getting_date, state = FSMfilling.date)
    dp.register_message_handler(getting_time_start, state = FSMfilling.time_start)
    # dp.register_message_handler(getting_time_end, state = FSMfilling.time_end)
    # dp.register_message_handler(clients_operator, state = FSMfilling.clients_operator)
    dp.register_message_handler(getting_rezgim, state = FSMfilling.rezgim)
    dp.register_message_handler(getting_number_workers, state = FSMfilling.number_workers)
    dp.register_message_handler(getting_number_clients, state = FSMfilling.number_clients)
    dp.register_message_handler(getting_name_worker, state = FSMfilling.name_worker)
    # dp.register_message_handler(getting_dolzhnost_worker, state = FSMfilling.dolzhnost_worker)
    dp.register_message_handler(getting_describe_worker, state = FSMfilling.describe_worker)
    # dp.register_message_handler(getting_workers_look, state = FSMfilling.workers_look)
    # dp.register_message_handler(getting_bad_worker_FIO, state = FSMfilling.bad_worker_FIO)
    # dp.register_message_handler(getting_sale_office, state = FSMfilling.sale_office)
    # dp.register_message_handler(getting_bad_sale_office, state = FSMfilling.bad_sale_office)
    dp.register_message_handler(getting_resume, state = FSMfilling.resume)
    dp.register_message_handler(getting_audio, content_types=['audio'], state = FSMfilling.audio)
    dp.register_message_handler(getting_photo1, content_types=['photo'], state = FSMfilling.photo1)
    dp.register_message_handler(getting_photo2, content_types=['photo'], state = FSMfilling.photo2)
    
def register_handlers_registration(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands = ['Регистрация'], state = None)
    dp.register_message_handler(helper, commands = ['Помощь'])
    dp.register_message_handler(oplata, commands = ['Оплата'])
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(getting_name, state = FSMregistration.name)
    dp.register_message_handler(getting_surname, state = FSMregistration.surname)
    dp.register_message_handler(getting_email, state = FSMregistration.email)