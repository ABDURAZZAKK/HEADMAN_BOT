from bot import *



def abuad(func):
    """ Декоратор не позволяющий использовать функции всем кроме меня """
    async def wrapper(message):
        if message.chat.id != 553818543:
            return await message.answer('Ты не админ, ты питух - твое место у параши')
        return await func(message)
    return wrapper



@dp.message_handler(state='*', commands=['mailing'])
@abuad
async def mailing(message: types.Message):
    """ Рассылает сообщение всем пользователям """
    answer_message = message.text[8:]
    for member_id in HW.member_list():
        await bot.send_message(member_id, answer_message)

""" Сделать возможным удалять ДЗ и категории """

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

