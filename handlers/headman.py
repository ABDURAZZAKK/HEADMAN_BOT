from loader import dp, types, bot, FSMContext
from states import Stater
import MW
import exceptions
from keyboards.choise_buttons import add_file, state_back_butt, stop_button
import logging
import logging.config


logging.config.fileConfig('logs\logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)



    # """ ОБРАБОТЧИКИ ДЛЯ АДМИНА """


@dp.message_handler(state=Stater.member, commands=['add_subjects', 'add_hw', 'timetable'])
async def give_permission(message: types.Message):
    """ Проверяет является ли участник старостой прежде чем выполнить команду """
    chat_id = message.chat.id
    if MW.get_role(chat_id):
        
        if message.text == '/add_subjects':
            await Stater.add_subjects.set()
            await message.answer("Ведите полное название предмета, "
                                 "а затем через запятую его "
                                 "сокращенные названия,\n например:\n "
                                 "Математический анализ,математика,матан,матеша", reply_markup=state_back_butt)

        if message.text == '/add_hw':
            await Stater.add_hw.set()
            await message.answer('Введите название предмета(полное либо сокращенное)\n затем "::"'
                                 'и текст задания\n например:\n '
                                 'инглиш:: выучить слова на странице Х упражнение Е', reply_markup=state_back_butt)

        if message.text == '/timetable':
            await Stater.change_schedule.set()
            await message.answer('Введите "+", если хотите изменить расписание для текущей недели "-" если'
                                    ' для следущей, затем введите "::", '
                                    'день недели от 1 до 7, затем "::" и '
                                    'расписание разделяя строки ";" '
                                    '\nнапример расписание на четверг для текущей недели:\n'
                            '+::4:: 1)инт.программирование 2п/г к. 2.11;\n'
                            '2)физ.культура;\n'
                            '3)ин.яз 1п/г к. 4.17;', reply_markup=state_back_butt
                            )

    else: 
        logger.info('%s was given to understand who the cock is', message.chat.id)
        await message.answer('Ты не староста, ты питух - твое место у параши')


@dp.message_handler(state=Stater.add_subjects)
async def add_subjects(message: types.Message):
    """ добавляет новый предмет(категорию) """
    text = message.text
    category = text.split(',')[0]
    aliases = ', '.join(text.split(',')[1:])
    data = {
        'category_name': category,
        "aliases": aliases,
        "group_name": MW.get_active_group(message.chat.id)
    }
    MW.add_category(data)
    await Stater.member.set()
    logger.info('%s created a new subject')
    await message.answer('Предмет добавлен')


@dp.message_handler(state=Stater.add_hw)
async def add_hw(message: types.Message, state: FSMContext):
    """ Добавляет новое ДЗ """
    await state.update_data(text=message.text, mem_id=message.chat.id, file_path='')
    await message.answer(text='Хотите добавить файл?', reply_markup=add_file)
    # try:
    #     MW.add_hw(message.chat.id, message.text)
    # except exceptions.CategoryNotFound as e:
    #     return await message.answer(str(e))
    # await Stater.member.set()
    # await message.answer(text='Задание добавлено.')


@dp.message_handler(state=Stater.change_schedule)
async def change_schedule(message: types.Message):
    try:
        day = MW.change_schedule(message.chat.id, message.text)
        await message.answer(f"Расписание на {day} изменено.")
    except exceptions.ValidationError as e:
        return await message.answer(str(e))
    except ValueError:
        return await message.answer('Не верный формат сообщения. Попробуйте еще.')
    await Stater.member.set()


@dp.callback_query_handler(state='*' ,text='state_back')
async def state_back(call: types.CallbackQuery):
    await Stater.member.set()
    await call.message.edit_reply_markup()


@dp.callback_query_handler(state=Stater.add_hw ,text='skip')
async def skip_add_file(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    try:
        MW.add_hw(data.get('mem_id'), data.get('text'), data.get('file_path'))
    except exceptions.CategoryNotFound as e:
        return await call.message.answer(str(e))
    await state.finish()
    await Stater.member.set()
    logger.info('%s created a new homework without files', call.message.chat.id)
    await call.message.answer(text='Задание добавлено.')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(state=Stater.add_hw ,text='add_file')
async def send_add_file(call: types.CallbackQuery, state=FSMContext):
    await Stater.file_handler.set()
    photo = open('help_photo\help_for_add_file.jpg','rb')
    await bot.send_photo(call.message.chat.id, photo)
    photo.close()
    await call.message.answer('Отправте файлы из раздела "Файл":',reply_markup=stop_button('Отмена'))


@dp.message_handler(state=Stater.file_handler, content_types=['document'])
async def hand_file(message: types.Message, state=FSMContext):
    file_id = message.document.file_id
    data = await state.get_data()
    await state.update_data(file_path=data.get('file_path')+file_id+'()')
    await message.answer('файл добавлен.', reply_markup=stop_button('Стоп'))


@dp.callback_query_handler(state=Stater.file_handler ,text='stop')
async def send_add_file(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    try:
        MW.add_hw(data.get('mem_id'), data.get('text'), data.get('file_path'))
    except exceptions.CategoryNotFound as e:
        return await call.message.answer(str(e))
    await state.finish()
    await Stater.member.set()
    logger.info('%s created a new homework with files', call.message.chat.id)
    await call.message.answer(text='Задание добавлено.')
    await call.message.edit_reply_markup()


@dp.message_handler(state=Stater.file_handler)
async def send_error(message: types.Message):
    logger.info('%s is dumb')
    await message.answer("это не документ.",reply_markup=stop_button('Отмена'))