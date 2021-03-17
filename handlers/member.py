from loader import dp, types, bot
from states import Stater
import MW
from config import MY_ID
import exceptions
from .utils import *
from keyboards.choise_buttons import delete_hw, delete_sub, leave_button
    # """ ОБРАБОТЧИКИ ДЛЯ ВСЕХ """
import logging
import logging.config


logging.config.fileConfig('logs/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)




@dp.message_handler(state=Stater.member, commands=['help'])
async def send_commands(message: types.Message):
    """ Вывод доступных команд  """
    chat_id = message.chat.id
    logger.info('%s used the command /help', chat_id)
    await message.answer(get_help(chat_id))


@dp.message_handler(state=Stater.member, commands=['group_name'])
async def send_group_name(message: types.Message):
    """ Отправляет участнику группу в которой он находится """
    logger.info('%s used the command /group_name',message.chat.id) 
    await message.answer(MW.get_active_group(message.chat.id))


@dp.message_handler(state=Stater.member, commands=['leave_group'])
async def leave_group(message: types.Message):
    """ Команда  чтобы покинуть группу """
    group_name = MW.get_active_group(message.chat.id)
    await message.answer(f'Вы действительно хотите покинуть группу: {group_name} ?', reply_markup=leave_button)


@dp.callback_query_handler(state=Stater.member ,text='leave')
async def send_leave(call: types.CallbackQuery):
    group_name = MW.get_active_group(call.message.chat.id)
    logger.info('%s leave_group: %s',call.message.chat.id, group_name)
    MW.leave_group(call.message.chat.id, group_name)
    MW.update_active_group(call.message.chat.id, 0)
    await call.message.edit_reply_markup()
    await Stater.any_state.set()
    await call.message.answer(f'Вы покинули группу: {group_name} \nПрисоеденитесь к группе: '
                            '/connect \nИли создайте новую: /make_group')


@dp.callback_query_handler(state=Stater.member ,text='no_leave')
async def send_no_leave(call: types.CallbackQuery):
    await call.message.edit_reply_markup()


@dp.message_handler(state=Stater.member, commands=['now','tmr','day'])
async def send_timetable(message: types.Message):
    week_days = [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье"
    ]
    try:
        now_week = MW.get_week()
        if message.text == '/now':
            s = 'odd_week' if now_week[1]%2 else 'even_week'
            sh = MW.get_schedule(message.chat.id,now_week[2],s)
        elif message.text == '/tmr':
            s = 'odd_week' if (now_week[1]+1 if (now_week[2]+1)==8 else now_week[1])%2 else 'even_week'
            sh = MW.get_schedule(message.chat.id,int((now_week[2]+1)%7),s)
        # elif '/day' in message.text:
        #     day = int(message.text[4:])
        #     if day > 7 or day < 1:
        #         return await message.answer('Нет такого дня недели')
        #     s = 'odd_week' if day%2 else 'even_week'
        #     sh = MW.get_schedule(message.chat.id,day,s)
        sh = sh[0]
        await message.answer(week_days[sh[1]-1] +'\n' +'\n'.join(str(sh[2]).split(';')))
        logger.info('%s found out the schedule',message.chat.id)
    except ValueError:
        await message.answer('N должно быть числом')
    except IndexError:
        await message.answer('Нет расписания на этот день :(')


@dp.message_handler(state=Stater.member, commands=['subjects'])
async def send_category_list(message: types.Message):
    """ Отправляет сообщение список предметов участника """
    logger.info('%s used the command /subjects',message.chat.id)
    role = MW.get_role(message.chat.id)
    if role:
        category = MW.category_list(MW.get_active_group(message.chat.id))
        await message.answer('Список предметов:')
        for c in category: 
            await message.answer(c[0]+' ('+c[1]+')', reply_markup=delete_sub(c[2]))

    else:
        category = MW.category_list(MW.get_active_group(message.chat.id))
        answer_message = "Список предметов:\n\n* " +\
            "\n* ".join([c[0]+' ('+c[1]+')' for c in category])
        await message.answer(answer_message)

@dp.callback_query_handler(state=Stater.member, text_contains="del_sub")
async def del_hw(call: types.CallbackQuery):
    sub_id = call.values['data'].split(':')[-1]
    logger.info('%s deleted subject',call.message.chat.id)
    hws = MW.there_is_hw(sub_id)
    if not hws:
        MW.delete('category', sub_id)
    else:
        for x in hws:
            MW.delete('homework', x[0])
        MW.delete('category', sub_id)
    await call.message.delete_reply_markup()
    await call.message.answer('Предмет удален.')

# @dp.message_handler(state=Stater.member, commands=['devlop_pituh'])
# async def state_for_latter(message: types.Message):
#     """ переводит в состояние для отправки сообщения разработчику """
#     await message.answer('Сообщение разработчику:')
#     await Stater.letter_to_developer.set()


# @dp.message_handler(state=Stater.letter_to_developer)
# async def send_letter_to_developer(message: types.Message):
#     """ отправляет сообщение разработчику """
#     await bot.send_message(MY_ID, f'{message.text} \n\nот '
#                            f'{MW.get_name(message.chat.id), message.chat.id}'
#                            f'\nиз группы: {MW.get_active_group( message.chat.id)}')
#     await Stater.member.set()
#     await message.answer('Спасибо за отзыв')


@dp.message_handler(state=Stater.member)
async def send_last_homework(message: types.Message):
    """ Возвращает N-ное колличство ДЗ по конкретному предмету  """
    ml = message.text.split('..')
    role = MW.get_role(message.chat.id)
    
    try:
        if len(ml) == 2:
            hw = MW.last_hw(message.chat.id, ml[1], int(ml[0]))
            logger.info('%s learned homework',message.chat.id)
        else:
            hw = MW.last_hw(message.chat.id, message.text)
            logger.info('%s learned homework',message.chat.id)
        if not hw:
            return await message.answer("Пока ДЗ нет :)")
        for h in list(reversed(hw)):
            if role:
                await message.answer(f"""{h[1]} \n\n дата публикации:{h[2][:10]} """,reply_markup=delete_hw(h[0]))
            else:
                await message.answer(f"""{h[1]} \n\n дата публикации:{h[2][:10]} """)
            if '()' in str(h[3]):
                for i in h[3].rstrip('()').split('()'):
                    await bot.send_document(message.chat.id, i)
    except exceptions.CategoryNotFound as e:
        await message.answer(str(e))
    except ValueError:
         await message.answer("Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n10..английский")

@dp.callback_query_handler(state=Stater.member, text_contains="del_hw")
async def del_hw(call: types.CallbackQuery):
    logger.info('%s deleted homework',call.message.chat.id) 
    MW.delete('homework', call.values['data'].split(':')[-1])
    await call.message.delete_reply_markup()
    await call.message.answer('ДЗ удалено.')


@dp.message_handler(state='*')
async def send_last_mail(message: types.Message):
    await message.answer('/make_group\n\n/connect\n\n/group_list')








# @dp.message_handler(commands = ['f'])
# async def ork(message: types.Message):
#     # await Stater.test.set()
#     # await message.answer('кидай файл')
#     await bot.send_document(message.chat.id, 'BQACAgIAAxkBAAIMCGA2ikq9KgTihC9Btj1oZ0Qe4EFrAALGDAACo-C4SUKCngoGNYEdHgQ')



# @dp.message_handler(state=Stater.test, content_types=['document'])
# async def save_file(message: types.Message):
#     file_id = message.document.file_id
   

# await bot.send_document(m_id, 'BQACAgIAAxkBAAIMCGA2ikq9KgTihC9Btj1oZ0Qe4EFrAALGDAACo-C4SUKCngoGNYEdHgQ')
# @dp.message_handler(state=Stater.test, content_types=['document'])
# async def save_file(message: types.Message):
#     await message.answer('ща гляну')
#     file_id = message.document.file_id
#     fil = await bot.get_file(file_id)

#     fname, file_ex = os.path.splitext(fil.file_path)
#     p = f'files/{message.chat.id}'
#     fil.file_path = p + '/' + fname.split("/")[-1]+file_ex
#     await fil.download()
#     shutil.make_archive(p,'zip',p)
#     shutil.rmtree(p)


