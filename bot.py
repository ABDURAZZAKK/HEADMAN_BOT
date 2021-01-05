import os 
from config import *



from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import HW

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Stater(StatesGroup):
    make_group = State()
    connecting = State()
    
    headman = State()
    student = State()



@dp.message_handler(state='*',commands=['start'])
async def send_welcome(message: types.Message):
# """ Для не авториз. пользователя """
    # Отправляет приветственное сообщение и помощь по боту
    await message.answer(
        'Бот для удобного хранения ДЗ\n\n'
        'Создать группу (вы станете ее старостой): /make_group\n\n'
        'Присоеденится к группе: /connect\n'
     
    )

@dp.message_handler(commands=['make_group','connect'])
async def state_purpose(message: types.Message):
    await message.answer(
        'Название группы:'
    )
    if message.text == '/make_group':
        await Stater.make_group.set()
    if message.text == '/connect':
        await Stater.connecting.set()
    
    


@dp.message_handler(state=Stater.make_group)
async def make_group(message: types.Message, state: FSMContext):

    await message.answer('кажется работает :)')

    state.update_data({
        'group_name':message.text,
        'member_id':message.chat.id,
        'headman':True,
        })

  




# @dp.message_handler(commands=['help'])
# async def send_commands(message: types.Message):
""" Вывод команд  """
#     # Отправляет приветственное сообщение и помощь по боту
#     await message.answer(
#         'Бот для удобного хранения ДЗ\n\n'
#         'Расписание на завтра: /tmr'
#         'Расписание на сегодня: /now'
#         'Список предметов: /subjects\n'
#         'Актуальное дз: Философия\n'
#         'Дз по посленим 3 парам: \n/3ls Философия\n'
#         'Дз за все время: /all Философия\n'
#         'Книга жалоб и предложений: \n/devlop_pituh\n'
#     )



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
