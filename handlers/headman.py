from loader import dp, types, bot
from states import Stater
import MW
import exceptions


    # """ ОБРАБОТЧИКИ ДЛЯ АДМИНА """


@dp.message_handler(state=Stater.member, commands=['add_subjects', 'add_hw', 'timetable'])
async def give_permission(message: types.Message):
    """ Проверяет является ли участник старостой прежде чем выполнить команду """
    chat_id = message.chat.id
    active_group = MW.get_active_group(chat_id)
    if MW.get_role(chat_id, active_group):
        
        if message.text == '/add_subjects':
            await Stater.add_subjects.set()
            await message.answer("Ведите полное название предмета, "
                                 "а затем через запятую его "
                                 "сокращенные названия,\n например:\n "
                                 "Математический анализ,математика,матан,матеша")

        if message.text == '/add_hw':
            await Stater.add_hw.set()
            await message.answer('Введите название предмета(полное либо сокращенное)\n затем "::"'
                                 'и текст задания\n например:\n '
                                 'инглиш:: выучить слова на странице Х упражнение Е')

        if message.text == '/timetable':
            await Stater.change_schedule.set()
            await message.answer('Введите "+", если хотите изменить расписание для текущей недели "-" если'
                                    ' для следущей, затем введите "::", '
                                    'день недели от 1 до 7, затем "::" и '
                                    'расписание разделяя строки ";" '
                                    '\nнапример расписание на четверг для текущей недели:\n'
                            '+::4:: 1)инт.программирование 2п/г к. 2.11;\n'
                            '2)физ.культура;\n'
                            '3)ин.яз 1п/г к. 4.17;'
                            )

    else: 
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
    await message.answer('Предмет добавлен')


@dp.message_handler(state=Stater.add_hw)
async def add_hw(message: types.Message):
    """ Добавляет новое ДЗ """
    try:
        MW.add_hw(message.chat.id, message.text)
    except exceptions.CategoryNotFound as e:
        return await message.answer(str(e))
    await Stater.member.set()
    await message.answer('Задание добавлено.')


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