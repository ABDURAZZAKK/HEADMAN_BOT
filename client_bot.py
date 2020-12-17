import os 
from settings import *



from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(massage: types.Message):
    # Отправляет приветственное сообщение и помощь по боту
    await massage.answer(
        'Бот для удобного хранения ДЗ\n\n'
        'Авторизоватся: /auth\n'
        'Список предметов: /subject_list\n'
        'Актуальное дз: Философия\n'
        'Дз по посленим 3 парам: /3ls Философия\n'
        'Дз за все время: /all Философия\n'
        'Книга жалоб и предложений: /admin_pituh'
    )



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
