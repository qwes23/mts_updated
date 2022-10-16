from aiogram import Bot 
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage  = MemoryStorage()

bot = Bot(token = "5365166446:AAEe740Q5yPT2IlHdsFvKACr9xSH6ASN8xk")
dp  = Dispatcher(bot, storage=storage)