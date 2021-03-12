if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)

    """ 
      
    """

    headman_comds = ("Добавить предмет: /add_subjects\n"
                     "Добавить ДЗ: /add_hw\n"
                     "Изменить расписание: /timetable"
                     "\n\n"
                     )

    member_comds = ('Название группы: /group_name\n'
                    'Список ваших групп: /group_list\n'
                    'Покиунть группу:/leave_group\n\n'
                    'Расписание на завтра: /tmr\n'
                    'Расписание на сегодня: /now\n\n'
                    # 'Расписание на определенный день: /day N\n '
                    # 'где N - номер дня недели от 1 до 7\n\n'
                    'Список предметов: /subjects\n'
                    'Последнее дз: Философия\n'
                    'Дз по посленим N парам: \n N..Философия\n\n'
                    'Создать новую группу: /make_group\n'
                    'Присоеденится к группе: /connect\n\n'
                    'Книга жалоб и предложений: \n/devlop_pituh\n'
                    )