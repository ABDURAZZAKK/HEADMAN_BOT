import os
from config import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import HW
import exceptions

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# dp = Dispatcher(bot)


class Stater(StatesGroup):
    auth = State()
    make_group = State()
    connecting = State()

    add_subjects = State()
    letter_to_developer = State()

    member = State()

    #  """АВТОРИЗАЦИЯ И СОЗДАНИЕ ГРУППЫ"""


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    """Проверяет авторезован ли пользователь и предлагает создать группу."""
    chat_id = message.chat.id
    active_group = HW.get_active_group(chat_id)
    if not chat_id in HW.member_list():
        await message.answer('Введите имя:')
        await Stater.auth.set()
    elif active_group != '0':
        await message.answer(f'группа: {active_group}')
        await Stater.member.set()
        print('/start = ',chat_id,active_group)
        await message.answer(get_help(chat_id,active_group))
    else:
        await message.answer(
            f'Здравствуйте, {HW.get_name(chat_id)}\n\n'
            'Создать группу: /make_group\n\n'
            'Присоеденится к группе: /connect\n'
        )


@dp.message_handler(state='*', commands=['make_group', 'connect'])
async def attach_state(message: types.Message):
    """ Обрабатывает команды для создания либо присоединения к группе """
    if message.text == '/make_group':
        await Stater.make_group.set()
    if message.text == '/connect':
        await Stater.connecting.set()

    await message.answer(
        'Название группы:'
    )


@dp.message_handler(state=Stater.auth)
async def auth(message: types.Message):
    """ Авторизует пользователя """
    data = {
        'member_id': message.chat.id,
        'member_name': message.text
    }
    HW.add_memder(data)
    await message.answer(
        f'Здравствуйте, {data["member_name"]}\n\n'
        'Создать группу: /make_group\n\n'
        'Присоеденится к группе: /connect\n'
    )


@dp.message_handler(state=Stater.connecting)
async def connecting(message: types.Message):
    if message.text in HW.group_list():
        HW.update_active_group(message.text, message.chat.id)
        await Stater.member.set()
        await message.answer(f'Вы присоеденились к группе: {message.text}\n'
                             'Помощь: /help')
    else:
        await message.answer('Такой группы нет, попробуйте еще.')


@dp.message_handler(state=Stater.make_group)
async def make_group(message: types.Message):
    chat_id = message.chat.id
    try:
        HW.add_group(message.text, chat_id)
    except exceptions.NameAlreadyExists as e:
        return await message.answer('Это имя занято, попробуйте еще.')
    HW.update_active_group(message.text, chat_id)
    await Stater.member.set()
    await message.answer(f'Теперь вы староста группы: {message.text}\n\n' +\
                            get_help(chat_id,HW.get_active_group(chat_id))
                         )
    # """ ОБРАБОТЧИКИ ДЛЯ АДМИНА """


@dp.message_handler(state=Stater.member, commands=['add_subjects', 'add_hw', 'timetable'])
async def give_permission(message: types.Message):
    chat_id = message.chat.id
    if HW.get_role(chat_id, HW.get_active_group(chat_id)):
        if message.text == '/add_subjects':
            await Stater.add_subjects.set()
            await message.answer("Ведите полное название предмета, "
                                 "а затем через запятую его "
                                 "сокращенные названия, например: "
                                 "Математический анализ, математика, матан, матеша")

        if message.text == '/add_hw':
            await message.answer('Этот функционал еще не реализован :(')

        if message.text == '/timetable':
            await message.answer('Этот функционал еще не реализован :(')

    else:
        await message.answer('Ты не староста, ты питух - твое место у параши')


@dp.message_handler(state=Stater.add_subjects)
async def add_subjects(message: types.Message):
    text = message.text.lower()
    category = text.split(',')[0]
    aliases = ', '.join(text.split(',')[1:])
    data = {
        'category_name':category,
        "aliases":aliases,
        "group_name":HW.get_active_group(message.chat.id)
    }
    HW.add_category(data)
    await Stater.member.set()
    await message.answer('Предмет добавлен')

    # """ ОБРАБОТЧИКИ ДЛЯ ВСЕХ """


@dp.message_handler(state=Stater.member, commands=['help'])
async def send_commands(message: types.Message):
    """ Вывод доступных команд  """
    chat_id = message.chat.id
    await message.answer(get_help(chat_id,HW.get_active_group(chat_id)))


@dp.message_handler(state=Stater.member, commands=['group_name'])
async def send_group_name(message: types.Message):
    await message.answer(HW.get_active_group(message.chat.id))


@dp.message_handler(state=Stater.member, commands=['subjects'])
async def send_category_list(message: types.Message):
    category = HW.category_list(HW.get_active_group(message.chat.id))
    answer_message = "Список предметов:\n\n* "+\
                        "\n* ".join([c[0]+'('+c[1]+')' for c in category])
    await message.answer(answer_message)


@dp.message_handler(state=Stater.member, commands=['devlop_pituh'])
async def state_for_latter(message: types.Message):
    await message.answer('Сообщение разработчику:')
    await Stater.letter_to_developer.set()


@dp.message_handler(state=Stater.letter_to_developer)
async def send_letter_to_developer(message: types.Message):
    await bot.send_message(553818543, f'{message.text} \n\nот '
                           f'{HW.get_name(message.chat.id), message.chat.id}'
                           f'\nиз группы: {HW.get_active_group( message.chat.id)}')
    await Stater.member.set()
    await message.answer('Спасибо за отзыв')


def get_help(chat_id,group_name):
    """ Вывод доступных команд  """
    headman_comds = ("Добавить предмет: /add_subjects\n"
                     "Добавить ДЗ: /add_hw\n"
                     "Изменить расписание: /timetable\n\n")

    member_comds = ('Название группы: /group_name\n'
                    'Расписание на завтра: /tmr\n'
                    'Расписание на сегодня: /now\n'
                    'Список предметов: /subjects\n'
                    'Актуальное дз: Философия\n'
                    'Дз по посленим 3 парам: \n/3ls Философия\n'
                    'Дз за все время: /all Философия\n\n'
                    'Создать новую группу: /make_group\n'
                    'Присоеденится к группе: /connect\n'
                    'Книга жалоб и предложений: \n/devlop_pituh\n')

    if HW.get_role(chat_id,group_name):
        return str(headman_comds)+str(member_comds)
    else:
        return str(member_comds)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
