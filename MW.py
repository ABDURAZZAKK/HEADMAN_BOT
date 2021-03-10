import datetime

import pytz

from db import db
import exceptions
from typing import List, NamedTuple, Optional



class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    category_id: int
    exercise: str



def add_group(member_id, group_name):
    """Добавляет группу в бд и связывает админа с группой."""
    try:
        db.insert('groups',{'name':group_name})
    except:
        raise exceptions.NameAlreadyExists('Это имя занято, попробуйте другое.')
    db.insert('member_group',{
        'member_id':member_id,
        'group_name':group_name,
        'headman':1
    })


def add_memder(data):
    """Добавляет пользователя"""
    db.insert('members',{
        'id':data['member_id'],
        'name':data['member_name']
    })

def connect(member_id, group_name):
    """ Добавляет участника в группу """
    try:
        get_role(member_id, group_name)
    except:
        db.insert('member_group',{
            'member_id':member_id,
            'group_name':group_name,
            'headman':0
        })

    


def add_category(data):
    """ Добавляет новый предмет(категорию) """
    db.insert('category',{
        'name':data['category_name'],
        'aliases':data['aliases'],
        'group_name':data['group_name']
    })


def add_hw(member_id: int, raw: str, file_path: str):
    """ Добавляет новое ДЗ """
    parsed_message = _parse_exercise(member_id, raw)
    db.insert(
        'homework',{
            'exercise':parsed_message.exercise,
            'category':parsed_message.category_id,
            'file_path':file_path,
            'created_date': _get_now_formatted()
        }
    )


def leave_group(member_id, group_name):
    """ Удаляет участника из группы """
    db.delete_many_to_many('member_group', member_id, group_name)


def delete(table, row_id):
    db.delete(table, row_id)


def update_active_group(member_id, group_name):
    'Обновляет активную группу(группу с которой можно взаимод.) пользователя'
    db.update_active_group('members', member_id, {'active_group':group_name})


def get_name(member_id):
    """Возвращает имя по ID """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name FROM members WHERE id LIKE {member_id}')
    return cursor.fetchone()[0]


def get_role(member_id):
    "Проверяет является ли member_id админом возвращает 1 или 0"
    group_name = get_active_group(member_id)
    cursor = db.get_cursor()
    cursor.execute(f'SELECT headman FROM member_group WHERE member_id LIKE {member_id}'
                   f' AND group_name LIKE "{group_name}"')
    return cursor.fetchone()[0]


def get_active_group(member_id):
    """ Возвращает активную группу участника """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT active_group FROM members WHERE id LIKE {member_id}')
    return cursor.fetchone()[0]


def group_list():
    "Возвращает list() с именами всех групп"
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name FROM groups')
    result = [x[0] for x in cursor.fetchall()]
    return result


def get_schedule(member_id, day, week_day):
    group_name = get_active_group(member_id)
       
    cursor = db.get_cursor()
    cursor.execute(f'SELECT id, day_w, {week_day} FROM schedule WHERE group_name LIKE "{group_name}" AND day_w LIKE {day}')
     
    return cursor.fetchall()


def personal_groups(member_id):
    """ Возвращает для участника все его группы и статус в них """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT group_name, headman FROM member_group WHERE member_id LIKE {member_id}')
    result = cursor.fetchall()
    return result



def member_list():
    """Возвращает list() c ID пользователей """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT id FROM members')
    result = [x[0] for x in cursor.fetchall()]
    return result


def category_list(group_name):
    """ Возвращает все категории конкретной группы """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name, aliases, id FROM category WHERE group_name LIKE "{group_name}"')
    result = cursor.fetchall()
    return result


def last_hw(member_id, category_name, limit=1):
    """Возвращает N-ное количество заданий """ 
    category_id = _get_category_id(member_id, category_name)
    cursor = db.get_cursor()
    cursor.execute(f"""SELECT id, exercise,  created_date, file_path FROM homework 
                    WHERE category={category_id} order by created_date desc limit {limit}""")
    return cursor.fetchall()


    
def change_schedule(member_id, raw):
    group_name = get_active_group(member_id)
    mess = _parse_schedule(raw)
    sh = get_schedule(member_id, mess['day_w'], mess['parity'])
    if len(sh) == 0:
        db.insert(
            "schedule",{
                "day_w":mess['day_w'],
                mess['parity']:mess['sh'],
                "group_name":group_name
            })
    else:
        db.update_schedule('schedule',mess['parity'],mess['sh'],sh[0][0])

    return mess['strday']


def _parse_schedule(raw):
    now_week = get_week()
    mess = raw.split('::')
    week_days = [
        "понедельник",
        "вторник",
        "среду",
        "четверг",
        "пятницу",
        "субботу",
        "воскресенье"
    ]
    if len(mess) != 3:
        raise exceptions.ValidationError('Неверный формат сообщения. Попробуйте еще')
    if int(mess[1]) > 7 or int(mess[1]) < 1:
        raise exceptions.ValidationError('Ввеидите день недели от 1 до 7\n '
                                        '1 - Понедельник\n 7 - Воскресенье')
    s = ''
    if  mess[0].lstrip().rstrip() == '+' :
        s = 'odd_week' if now_week[1]%2 else 'even_week'
    elif mess[0].lstrip().rstrip() == '-':
        s = 'even_week' if now_week[1]%2 else 'odd_week'
    
    if s == '':
        raise exceptions.ValidationError('Неверный формат сообщения. Попробуйте еще')

    
    return {'day_w':int(mess[1]),'parity':s, 'sh':mess[2], 'strday':week_days[int(mess[1])-1]}


def _parse_exercise(member_id, raw):
    """Парсит задание возвращает ID категории и текст задания"""
    category_id = _get_category_id(member_id, raw.split('::')[0] )
    exercise = raw.split('::')[1]
    return Message(category_id=category_id, exercise=exercise)
    
    
def _get_category_id(member_id, category_name):
    """Возвращает ID категории """ 
    categories = category_list(get_active_group(member_id))
    for i in categories:
        if category_name.lower() in list(map(lambda s: s.lstrip().rstrip().lower(),', '.join([i[0],i[1]]).split(', '))):
            return i[2]
    raise exceptions.CategoryNotFound("Такого предмета нет, попробуйте еще.")



def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now
   

def get_week():
    """ Возвращает кортеж (год, номер недели, день недели) пример (2021, 11, 7) """
    return _get_now_datetime().isocalendar()
    