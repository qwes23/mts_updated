from aiogram import types, Dispatcher
from create_bot import dp

#@dp.message_handler()
async def location_send(message : types.Message):
    if message.text == 'Привет':
         
         await message.answer('Здравствуй!')

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(location_send, commands = ['hellowing'])