from aiogram.types import InlineKeyboardMarkup , InlineKeyboardButton



add_file = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='ДА', callback_data='add_file'),
                InlineKeyboardButton(text='НЕТ', callback_data='skip')
            ]
    ]
)

state_back_butt = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='state_back')
        ]
    ]
)
def stop_button(text):
    stop_butto = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data='stop')
            ]
        ]
    )
    return stop_butto


def delete_hw(row_id):
    del_hw = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить', callback_data=f'del_hw:{row_id}')
            ]
        ]
    ) 
    return del_hw

def delete_sub(row_id):
    del_sub = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить', callback_data=f'del_sub:{row_id}')
            ]
        ]
    ) 
    return del_sub


def answer_the_mess(chat_id):
    answer = InlineKeyboardMarkup(
        inline_keyboard=[
                [
                    InlineKeyboardButton(text='Ответить', callback_data=f'answer:{chat_id}')
                ]
            ]
        ) 
    return answer

leave_button = InlineKeyboardMarkup(
        inline_keyboard=[
                [
                    InlineKeyboardButton(text='ДА', callback_data="leave"),
                    InlineKeyboardButton(text='НЕТ', callback_data="no_leave")
                ]
            ]
        )


def connect_button(group_list):
    connect_butt = InlineKeyboardMarkup(row_width=1)
    for g in group_list:
        text = g[0]+' - '+'Староста.' if g[1] else g[0]+' - '+'Участник.'
        button = InlineKeyboardButton(text=f'{text}', callback_data=f'connect:{g[0]}')
        connect_butt.insert(button)
    return connect_butt

