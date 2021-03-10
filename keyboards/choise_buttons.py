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

stop_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Стоп', callback_data='stop')
        ]
    ]
)


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
