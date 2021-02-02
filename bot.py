import os 
from config import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import HW, exceptions

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Stater(StatesGroup):
    auth = State()
    make_group = State()
    connecting = State()
    
    member = State()

                            #  """АВТОРИЗАЦИЯ И СОЗДАНИЕ ГРУППЫ"""

@dp.message_handler(state='*',commands=['start'])
async def send_welcome(message: types.Message):
    """Проверяет авторезован ли пользователь и предлагает создать группу."""
    if  not message.chat.id in HW.member_list():
        await message.answer('Введите имя:')
        await Stater.auth.set()
    else:
        await message.answer(
            f'Здравствуйте, {HW.get_name(message.chat.id)[0]}\n\n'
            'Создать группу (вы станете ее старостой): /make_group\n\n'
            'Присоеденится к группе: /connect\n'
            )
        



@dp.message_handler(state=Stater.auth)
async def auth(message: types.Message, state: FSMContext):
    """ Авторизует пользователя """
    await state.update_data({
        'member_id':message.chat.id,
        'member_name':message.text
        })
    data = await state.get_data()
    HW.add_memder(data)
    await message.answer(
        f'Здравствуйте, {message.text}\n\n'
        'Создать группу (вы станете ее старостой): /make_group\n\n'
        'Присоеденится к группе: /connect\n'
    )
    


@dp.message_handler(state='*',commands=['make_group','connect'])
async def attach_state(message: types.Message):
    """ Обрабатывает команды для создания либо присоединения к группе """ 
    if message.text == '/make_group':
        await Stater.make_group.set()
    if message.text == '/connect':
        await Stater.connecting.set()

    await message.answer(
        'Название группы:'
    )


@dp.message_handler(state=Stater.make_group)
async def make_group(message: types.Message, state: FSMContext):
    await state.update_data({
        'group_name':message.text,
        'headman':1,
        })
    data = await state.get_data()
    try:
        HW.add_group(data.get('group_name'),message.chat.id)
        # HW.update_role(data['headman'],message.chat.id)
    except exceptions.NameAlreadyExists as e:
        return await message.answer('Это имя занято, попробуйте еще.')

    await Stater.member.set()
    await message.answer(f'Теперь вы староста группы: {data["group_name"]}\n\n'
                          'Вы можете:\n'
                          "Добавить предмет: /add_subjects\n"
                          "Добавить ДЗ: /add_hw\n"
                          "Изменить расписание: /timetable\n\n"
                          'Узнать:\n'
                          'Расписание на завтра: /tmr\n'
                          'Расписание на сегодня: /now\n'
                          'Список предметов: /subjects\n'
                          'Актуальное дз: Философия\n'
                          'Дз по посленим 3 парам: \n/3ls Философия\n'
                          'Дз за все время: /all Философия\n'
                          'Книга жалоб и предложений: \n/devlop_pituh\n'
                          )


                            # """ ОБРАБОТЧИКИ ДЛЯ СТАРОСТЫ """

                            
# @dp.message_handler(state=Stater.member)
# async def test_h(message: types.Message, state: FSMContext):

    

@dp.message_handler(state=Stater.member,commands=['help'])
async def send_commands(message: types.Message):
    """ Вывод доступных команд  """    
    headman_comds = ("Добавить предмет: /add_subjects\n"
                    "Добавить ДЗ: /add_hw\n"
                    "Изменить расписание: /timetable\n\n"
                    )
                          
    member_comds = ('Расписание на завтра: /tmr\n'
                    'Расписание на сегодня: /now\n'
                    'Список предметов: /subjects\n'
                    'Актуальное дз: Философия\n'
                    'Дз по посленим 3 парам: \n/3ls Философия\n'
                    'Дз за все время: /all Философия\n\n'
                    'Создать группу новую группу: /make_group\n'
                    'Присоеденится к группе: /connect\n'
                    'Книга жалоб и предложений: \n/devlop_pituh\n'
                    )

    if HW.check_role(message.chat.id):
        await message.answer(str(headman_comds)+str(member_comds))
    else:
        await message.answer(str(member_comds))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
