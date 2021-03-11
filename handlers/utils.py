import MW



def get_help(chat_id):
    """ Вывод доступных команд  """
    headman_comds = ("Добавить предмет: /add_subjects\n"
                     "Добавить ДЗ: /add_hw\n"
                     "Изменить расписание: /timetable"
                     "\n\n"
                     )

    member_comds = ('Название группы: /group_name\n'
                    'Список ваших групп: /group_list\n'
                    'Покиунть группу:/leave_group\n\n'
                    'Расписание на завтра: /tmr\n'
                    'Расписание на сегодня: /now\n'
                    # 'Расписание на определенный день: /day N\n '
                    # 'где N - номер дня недели от 1 до 7\n\n'
                    'Список предметов: /subjects\n'
                    'Последнее дз: Философия\n'
                    'Дз по посленим N парам: \n N..Философия\n\n'
                    'Создать новую группу: /make_group\n'
                    'Присоеденится к группе: /connect\n\n'
                    'Книга жалоб и предложений: \n/devlop_pituh\n'
                    )

    if MW.get_role(chat_id):
        return str(headman_comds)+str(member_comds)
    else:
        return str(member_comds)


def get_personal_groups(member_id):
    """ Возврашает список групп участника """
    groups = MW.personal_groups(member_id)
    answer_message = "Список групп:\n\n* " +\
        "\n* ".join([c[0]+' - '+'староста.' if c[1] else 
                    c[0]+' - '+'участник.' for c in groups])
    return answer_message