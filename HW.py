import datetime

import pytz

import db
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
    try:
        get_role(member_id, group_name)
    except:
        db.insert('member_group',{
            'member_id':member_id,
            'group_name':group_name,
            'headman':0
        })

    


def add_category(data):
    db.insert('category',{
        'name':data['category_name'],
        'aliases':data['aliases'],
        'group_name':data['group_name']
    })


def add_hw(member_id: int, raw: str ):
    parsed_message = _parse_exercise(member_id, raw)
    db.insert(
        'homework',{
            'exercise':parsed_message.exercise,
            'category':parsed_message.category_id,
            'created_date': _get_now_formatted()
        }
    )


def leave_group(member_id, group_name):
    db.delete_many_to_many('member_group', member_id, group_name)


def update_active_group(member_id, group_name):
    'Обновляет активную группу(группу с которой можно взаимод.) пользователя'
    db.update_active_group('members', member_id, {'active_group':group_name})


def get_name(member_id):
    """Возвращает имя по ID """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name FROM members WHERE id LIKE {member_id}')
    return cursor.fetchone()[0]


def get_role(member_id, group_name):
    "Проверяет является ли member_id админом возвращает 1 или 0"
    cursor = db.get_cursor()
    cursor.execute(f'SELECT headman FROM member_group WHERE member_id LIKE {member_id}'
                   f' AND group_name LIKE "{group_name}"')
    return cursor.fetchone()[0]


def get_active_group(member_id):
    cursor = db.get_cursor()
    cursor.execute(f'SELECT active_group FROM members WHERE id LIKE {member_id}')
    return cursor.fetchone()[0]


def group_list():
    "Возвращает list() с именами групп"
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name FROM groups')
    result = [x[0] for x in cursor.fetchall()]
    return result


def personal_groups(member_id):
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
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name, aliases, id FROM category WHERE group_name LIKE "{group_name}"')
    result = cursor.fetchall()
    return result


def last_hw(member_id, category_name, limit=1):
    
    # categories = category_list(group_name)
    # for i in categories:
    #     if category_name.lower() in ', '.join([i[0],i[1]]).split(', '):
    #         category_id = i[2]

    category_id = _get_category_id(member_id, category_name)
    cursor = db.get_cursor()
    cursor.execute(f"""SELECT id, exercise, created_date FROM homework 
                    WHERE category={category_id} order by created_date desc limit {limit}""")
    return cursor.fetchall()
    # raise exceptions.CategoryNotFound("Предмет не найден.")
    

# def _parse_message()


def _parse_exercise(member_id, raw):
    category_id = _get_category_id(member_id, raw.split('::')[0] )
    exercise = raw.split('::')[1]
    return Message(category_id=category_id, exercise=exercise)
    
    
def _get_category_id(member_id, category_name):
    categories = category_list(get_active_group(member_id))
    for i in categories:
        if category_name.lower() in ', '.join([i[0],i[1]]).split(', '):
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
   







    

