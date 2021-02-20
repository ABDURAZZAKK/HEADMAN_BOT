import os
from config import *

from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import HW
from starer import Stater
import exceptions

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# dp = Dispatcher(bot)

    #  """АВТОРИЗАЦИЯ И СОЗДАНИЕ ГРУППЫ"""

""" 
логирование, замеры скорости работы того как оно есть сейчас и переведенная целиком на запросы 
"""

@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    """Проверяет авторезован ли пользователь и предлагает создать группу."""
    chat_id = message.chat.id
    if not chat_id in HW.member_list():
        await message.answer('Введите имя:')
        await Stater.auth.set()
    else:
        await message.answer(
            f'Здравствуйте, {HW.get_name(chat_id)}\n\n'
            'Создать группу: /make_group\n\n'
            'Присоеденится к группе: /connect\n\n'
            'Список групп: /group_list'
        )


@dp.message_handler(state='*', commands=['make_group', 'connect', 'group_list'])
async def attach_state(message: types.Message):
    """ Обрабатывает команды для создания либо присоединения к группе """
    if message.chat.id in HW.member_list():
        if message.text == '/make_group':
            await Stater.make_group.set()
            await message.answer('Название группы:')

        if message.text == '/connect':
            await Stater.connecting.set()
            await message.answer('Название группы:')

        if message.text == '/group_list':
            await message.answer(get_personal_groups(message.chat.id))

    else:
        await message.answer('Введите команду: /start')


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
        'Присоеденится к группе: /connect\n\n'
        'Список ваших групп: /group_list'
    )
    await Stater.any_state.set()


@dp.message_handler(state=Stater.connecting)
async def connecting(message: types.Message):
    if message.text in HW.group_list():
        HW.connect(message.chat.id, message.text)
        HW.update_active_group(message.chat.id, message.text)
        await Stater.member.set()
        await message.answer(f'Вы присоеденились к группе: {message.text}\n'
                             'Помощь: /help')
    else:
        await message.answer('Такой группы нет, попробуйте еще.')


@dp.message_handler(state=Stater.make_group)
async def make_group(message: types.Message):
    chat_id = message.chat.id
    try:
        HW.add_group(chat_id, message.text)
    except exceptions.NameAlreadyExists as e:
        return await message.answer(str(e))
    HW.update_active_group(chat_id, message.text)
    await Stater.member.set()
    await message.answer(f'Теперь вы староста группы: {message.text}\n\n' +
                         get_help(chat_id, message.text)
                         )
    # """ ОБРАБОТЧИКИ ДЛЯ АДМИНА """


@dp.message_handler(state=Stater.member, commands=['add_subjects', 'add_hw', 'timetable'])
async def give_permission(message: types.Message):
    chat_id = message.chat.id
    active_group = HW.get_active_group(chat_id)
    if HW.get_role(chat_id, active_group):
        
        if message.text == '/add_subjects':
            await Stater.add_subjects.set()
            await message.answer("Ведите полное название предмета, "
                                 "а затем через запятую его "
                                 "сокращенные названия,\n например: "
                                 "Математический анализ,математика,матан,матеша")

        if message.text == '/add_hw':
            await Stater.add_hw.set()
            await message.answer('Введите название предмета(полное либо сокращенное)\n затем "::"'
                                 'и текст задания\n например: '
                                 'инглиш:: выучить слова на странице Х упражнение Е')

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
        'category_name': category,
        "aliases": aliases,
        "group_name": HW.get_active_group(message.chat.id)
    }
    HW.add_category(data)
    await Stater.member.set()
    await message.answer('Предмет добавлен')


@dp.message_handler(state=Stater.add_hw)
async def add_hw(message: types.Message):
    try:
        HW.add_hw(message.chat.id, message.text)
    except exceptions.CategoryNotFound as e:
        return await message.answer(str(e))
    await Stater.member.set()
    await message.answer('Задание добавлено.')

    # """ ОБРАБОТЧИКИ ДЛЯ ВСЕХ """


@dp.message_handler(state=Stater.member, commands=['help'])
async def send_commands(message: types.Message):
    """ Вывод доступных команд  """
    chat_id = message.chat.id
    await message.answer(get_help(chat_id, HW.get_active_group(chat_id)))


@dp.message_handler(state=Stater.member, commands=['group_name'])
async def send_group_name(message: types.Message):
    await message.answer(HW.get_active_group(message.chat.id))


@dp.message_handler(state=Stater.member, commands=['group_list'])
async def send_personal_groups(message: types.Message):
    await message.answer(get_personal_groups(message.chat.id))


@dp.message_handler(state=Stater.member, commands=['leave_group'])
async def leave_group(message: types.Message):
    group_name = HW.get_active_group(message.chat.id)
    HW.leave_group(message.chat.id, group_name)
    HW.update_active_group(message.chat.id, 0)
    await Stater.any_state.set()
    await message.answer(f'Вы покинули группу: {group_name}')

@dp.message_handler(state=Stater.member, commands=['subjects'])
async def send_category_list(message: types.Message):
    category = HW.category_list(HW.get_active_group(message.chat.id))
    answer_message = "Список предметов:\n\n* " +\
        "\n* ".join([c[0]+' ('+c[1]+')' for c in category])
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


@dp.message_handler(state=Stater.member)
async def send_last_homework(message: types.Message):
    ml = message.text.split('..')
    try:
        if len(ml) == 2:
            hw = HW.last_hw(message.chat.id, ml[1], int(ml[0]))
        else:
            hw = HW.last_hw(message.chat.id, message.text)
        for h in list(reversed(hw)):
            await message.answer(f"""{h[1]} \n\n дата публикации:{h[2][:10]} """)
    except exceptions.CategoryNotFound as e:
        await message.answer(str(e))
    except ValueError:
         await message.answer("Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n10..английский")



def get_help(chat_id, group_name):
    """ Вывод доступных команд  """
    headman_comds = ("Добавить предмет: /add_subjects\n"
                     "Добавить ДЗ: /add_hw\n"
                    #  "Изменить расписание: /timetable"
                     "\n\n"
                     )

    member_comds = ('Название группы: /group_name\n'
                    'Список ваших групп: /group_list\n'
                    'Покиунть группу:/leave_group\n'
                    # 'Расписание на завтра: /tmr\n'
                    # 'Расписание на сегодня: /now\n'
                    'Список предметов: /subjects\n'
                    'Последнее дз: Философия\n'
                    'Дз по посленим N парам: \n N..Философия\n'
                    'Создать новую группу: /make_group\n'
                    'Присоеденится к группе: /connect\n'
                    'Книга жалоб и предложений: \n/devlop_pituh\n'
                    )

    if HW.get_role(chat_id, group_name):
        return str(headman_comds)+str(member_comds)
    else:
        return str(member_comds)


def get_personal_groups(member_id):
    groups = HW.personal_groups(member_id)
    answer_message = "Список групп:\n\n* " +\
        "\n* ".join([c[0]+' - '+'староста.' if c[1] else 
                    c[0]+' - '+'участник.' for c in groups])
    return answer_message



