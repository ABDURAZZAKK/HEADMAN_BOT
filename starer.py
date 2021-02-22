from aiogram.dispatcher.filters.state import StatesGroup, State



class Stater(StatesGroup):
    any_state = State(state='*')
    
    auth = State()
    make_group = State()
    connecting = State()

    add_subjects = State()
    add_hw = State()
    change_schedule = State()
    letter_to_developer = State()

    member = State()
    