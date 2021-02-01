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

def get_name(member_id):
    """Возвращает имя по ID """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT name FROM members WHERE id LIKE {member_id}')

    return cursor.fetchone()



def add_memder(data):
    """Добавляет пользователя"""
    db.insert('members',{
        'id':data['member_id'],
        'name':data['member_name']
    })



# def update_role(role,member_id):
#     db.update('member_group',{'headman':role},member_id)




def member_list():
    """Возвращает list() c ID пользователей """
    cursor = db.get_cursor()
    cursor.execute(f'SELECT id FROM members')
    result = [x[0] for x in cursor.fetchall()]
    
    return result



# def conect(chat_id):
#     pass

    # return chat_id
    

