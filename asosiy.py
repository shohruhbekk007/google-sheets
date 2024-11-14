import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Bot tokeningizni kiriting
API_TOKEN = '7720505731:AAE2ZgyIYS310DnvILdhKRwQ8y65xMTiY3g'

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Foydalanuvchi ma'lumotlari uchun State klassi
class Form(StatesGroup):
    fullname = State()  # Ism va familiya
    age = State()  # Yosh
    interests = State()  # Qiziqishlar
    photo = State()  # Rasm


# Boshlash tugmasi
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")]
    ],
    resize_keyboard=True
)


# /start buyrug'ini qayta ishlash
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Iltimos, ism va familiyangizni kiriting:", reply_markup=start_kb)
    await state.set_state(Form.fullname)


# Ism va familiya olish
@dp.message(Form.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(fullname=fullname)
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(Form.age)


# Yosh olish
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    await message.answer("Qiziqishlaringizni kiriting:")
    await state.set_state(Form.interests)


# Qiziqishlar olish
@dp.message(Form.interests)
async def process_interests(message: types.Message, state: FSMContext):
    interests = message.text
    await state.update_data(interests=interests)
    await message.answer("Rasm yuboring:")
    await state.set_state(Form.photo)


# Rasm olish
@dp.message(Form.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id  # Eng yuqori sifatli rasmni olish
    await state.update_data(photo=photo)

    # Foydalanuvchidan olingan ma'lumotlarni ko'rsatish
    user_data = await state.get_data()
    fullname = user_data.get("fullname")
    age = user_data.get("age")
    interests = user_data.get("interests")

    await message.answer(f"Ism: {fullname}\nYosh: {age}\nQiziqishlar: {interests}")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

    # Shartlarni tugatish
    await state.clear()


# Rasm o'rniga boshqa kontent yuborilgan holatda xatolik xabarini yuborish
@dp.message(Form.photo)
async def process_invalid_photo(message: types.Message):
    await message.answer("Faqat rasm yuboring.")


# Botni ishga tushirish
if __name__ == "__main__":
    import asyncio


    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
