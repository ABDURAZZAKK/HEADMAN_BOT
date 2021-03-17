from loader import dp, types, bot
from states import Stater
import MW
import exceptions
from .utils import *
from keyboards.choise_buttons import connect_button
import logging
import logging.config

   #  """АВТОРИЗАЦИЯ И СОЗДАНИЕ ГРУППЫ"""


# logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logging.config.fileConfig('logs\logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)




@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    """Проверяет авторезован ли пользователь и предлагает создать группу."""
    chat_id = message.chat.id
    if not chat_id in MW.member_list():
        await message.answer('Введите имя:')
        await Stater.auth.set()
        logger.info("New member.")
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
            group_list = MW.personal_groups(message.chat.id)
            await message.answer("Список ваших групп:",reply_markup=connect_button(group_list))
            await message.answer('Название группы:')

        if message.text == '/group_list':
            await message.answer(get_personal_groups(message.chat.id))
            logger.info('%s used the command /group_list', message.chat.id)
            """ Отправляет участнику список его групп  """

    else:
        await message.answer('Введите команду: /start')


@dp.callback_query_handler(state=Stater.connecting ,text_contains='connect:')
async def call_connect(call: types.CallbackQuery):
    group_name = call.values['data'].split(':')[-1]
    MW.connect(call.message.chat.id, group_name)
    await Stater.member.set()
    await call.message.answer(f'Вы присоеденились к группе: {group_name}\n'
                             'Помощь: /help')
    await call.message.delete_reply_markup()


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
    logger.info('%s changed the group to: %s', message.chat.id, message.text)
    if message.text in MW.group_list():
        MW.connect(message.chat.id, message.text)
        await Stater.member.set()
        await message.answer(f'Вы присоеденились к группе: {message.text}\n'
                             'Помощь: /help')
    else:
        await message.answer('Такой группы нет, попробуйте еще.\n Или создайте ее /make_group')


@dp.message_handler(state=Stater.make_group)
async def make_group(message: types.Message):
    """ Создает новую группу и подключает к ней участника """
    chat_id = message.chat.id
    try:
        MW.add_group(chat_id, message.text)
    except exceptions.NameAlreadyExists as e:
        logger.error('%s tried to create an existing group')
        return await message.answer(str(e))
    logger.info('%s created a new group: %s', chat_id, message.text)
    MW.update_active_group(chat_id, message.text)
    await Stater.member.set()
    await message.answer(f'Теперь вы староста группы: {message.text}\n\n' +
                         get_help(chat_id)
                         )