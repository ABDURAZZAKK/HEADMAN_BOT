import os 
from settings import *



from aiogram import Bot, Dispatcher, executor, types
import auth


bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['start'])
""" Для не авториз. пользователя """
async def send_welcome(massage: types.Message):
    # Отправляет приветственное сообщение и помощь по боту
    await massage.answer(
        'Бот для удобного хранения ДЗ\n\n'
        'Присоеденится к группе: \conect\n'
     
    )

@dp.message_handler(commands=['conect'])
async def registration(massage: types.Message):
    
await massage.answer(
        auth.conect()
    )





# @dp.message_handler(commands=['help'])
# async def send_commands(massage: types.Message):
""" Вывод команд  """
#     # Отправляет приветственное сообщение и помощь по боту
#     await massage.answer(
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
