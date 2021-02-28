from loader import dp, types, bot
from states import Stater
from config import MY_ID
import MW
import exceptions


@dp.message_handler(commands=['admin'])
async def send_last_homework(message: types.Message):
    await message.answer('admin')


def abuad(func):
    """ Декоратор не позволяющий использовать функции всем кроме меня """
    async def wrapper(message):
        if message.chat.id != MY_ID:
            return await message.answer('Ты не админ, ты питух - твое место у параши')
        return await func(message)
    return wrapper



@dp.message_handler(state='*', commands=['mailing'])
@abuad
async def mailing(message: types.Message):
    """ Рассылает сообщение всем пользователям """
    answer_message = message.text[8:]
    for member_id in MW.member_list():
        await bot.send_message(member_id, answer_message)

