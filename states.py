from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    fullname = State()
    age = State()
    tel = State()
    photo = State()
    finish = State()