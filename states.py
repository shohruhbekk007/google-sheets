from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    fullname = State()  # Ism va familiya
    age = State()  # Yosh
    interests = State()  # Qiziqishlar
    photo = State()  # Rasm