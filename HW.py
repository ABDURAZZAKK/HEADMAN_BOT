import db
import exceptions


# Все переписать 

def add_group(group_name,member_id):
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

def add_category(data):
    db.insert('category',{
        'name':data['category_name'],
        'aliases':data['aliases'],
        'group_name':data['group_name']
    })


def update_active_group(group_name,member_id):
    'Обновляет активную группу(группу с которой можно взаимод.) пользователя'
    db.update_active_group('members',{'active_group':group_name},member_id)


def get_name(member_id):
    """Возвращает имя по ID """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name FROM members WHERE id LIKE {member_id}')
    return cursor.fetchone()[0]


def get_role(member_id,group_name):
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


def member_list():
    """Возвращает list() c ID пользователей """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT id FROM members')
    result = [x[0] for x in cursor.fetchall()]
    return result


def category_list(group_name):
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name, aliases FROM category WHERE group_name LIKE "{group_name}"')
    result = cursor.fetchall()
    return result

    

