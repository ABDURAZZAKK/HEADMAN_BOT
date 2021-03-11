from loader import dp, types, bot
from states import Stater
import MW
import exceptions
import logging
from .utils import *
   #  """АВТОРИЗАЦИЯ И СОЗДАНИЕ ГРУППЫ"""



@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    """Проверяет авторезован ли пользователь и предлагает создать группу."""
    chat_id = message.chat.id
    if not chat_id in MW.member_list():
        await message.answer('Введите имя:')
        await Stater.auth.set()
    else:
        await message.answer(
            f'Здравствуйте, {MW.get_name(chat_id)}\n\n'
            'Создать группу: /make_group\n\n'
            'Присоеденится к группе: /connect\n\n'
            'Список групп: /group_list'
        )


@dp.message_handler(state='*', commands=['make_group', 'connect', 'group_list'])
async def attach_state(message: types.Message):
    """ Обрабатывает команды для создания либо присоединения к группе """
    if message.chat.id in MW.member_list():
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
    MW.add_memder(data)
    await message.answer(
        f'Здравствуйте, {data["member_name"]}\n\n'
        'Создать группу: /make_group\n\n'
        'Присоеденится к группе: /connect\n\n'
        'Список ваших групп: /group_list'
    )
    await Stater.any_state.set()


@dp.message_handler(state=Stater.connecting)
async def connecting(message: types.Message):
    """ Подключает участника к группе """
    if message.text in MW.group_list():
        MW.connect(message.chat.id, message.text)
        MW.update_active_group(message.chat.id, message.text)
        await Stater.member.set()
        await message.answer(f'Вы присоеденились к группе: {message.text}\n'
                             'Помощь: /help')
    else:
        await message.answer('Такой группы нет, попробуйте еще.')


@dp.message_handler(state=Stater.make_group)
async def make_group(message: types.Message):
    """ Создает новую группу и подключает к ней участника """
    chat_id = message.chat.id
    try:
        MW.add_group(chat_id, message.text)
    except exceptions.NameAlreadyExists as e:
        return await message.answer(str(e))
    MW.update_active_group(chat_id, message.text)
    await Stater.member.set()
    await message.answer(f'Теперь вы староста группы: {message.text}\n\n' +
                         get_help(chat_id)
                         )