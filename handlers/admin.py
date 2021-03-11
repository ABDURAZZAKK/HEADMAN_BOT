from loader import dp, types, bot, FSMContext
from states import Stater
from config import MY_ID
import MW
import exceptions
from keyboards.choise_buttons import answer_the_mess


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


@dp.message_handler(state=Stater.member, commands=['devlop_pituh'])
async def state_for_latter(message: types.Message):
    """ переводит в состояние для отправки сообщения разработчику """
    await message.answer('Сообщение разработчику:')
    await Stater.letter_to_developer.set()


@dp.message_handler(state=Stater.letter_to_developer)
async def send_letter_to_developer(message: types.Message):
    """ отправляет сообщение разработчику """
    chat_id = message.chat.id
    await bot.send_message(MY_ID, f'{message.text} \n\nот '
                           f'{MW.get_name(chat_id), chat_id}'
                           f'\nиз группы: {MW.get_active_group(chat_id)}',reply_markup=answer_the_mess(chat_id))
    await Stater.member.set()
    await message.answer('Спасибо за отзыв')


@dp.callback_query_handler(state=Stater.member ,text_contains='answer')
async def reply_(call: types.CallbackQuery, state=FSMContext):
    await Stater.answer.set()
    await state.update_data(user_id=call.values['data'].split(':')[-1])
    await call.message.edit_reply_markup()
    await call.message.answer('Ваш ответ:')
    


@dp.message_handler(state=Stater.answer)
async def send_answer(message: types.Message,state=FSMContext):
    data = await state.get_data()
    await bot.send_message(data.get('user_id'), message.text)
    await message.answer('Сообщение отправленно.')
    await state.finish()
    await Stater.member.set()