from aiogram import Bot, Dispatcher, types
from config import *

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# dp = Dispatcher(bot)