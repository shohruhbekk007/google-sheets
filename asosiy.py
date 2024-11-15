import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from states import Form
from config import token
from buttons import get_text, get_confirm_keyboard, get_contact_keyboard, Til
from aiogram.types import ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(get_text('uz', 'greeting').format(name=message.from_user.full_name), reply_markup=Til)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.update_data(language=None)



@dp.callback_query(F.data.in_({"uz", "ru"}))
async def language_selection(call: types.CallbackQuery, state: FSMContext):
    language = call.data
    await state.update_data(language=language)
    await call.message.answer(get_text(language, 'enter_fullname'))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.set_state(Form.fullname)



@dp.message(Form.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    fullname = message.text
    await state.update_data(fullname=fullname)
    await message.answer(get_text(language, 'enter_age'))
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.set_state(Form.age)


@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    age = message.text
    if age.isdigit():
        await state.update_data(age=age)
        await message.answer(get_text(language, 'enter_phone'), reply_markup=get_contact_keyboard(language))
        await state.set_state(Form.tel)
    else:
        await message.answer(get_text(language, 'enter_age'))
        await state.set_state(Form.age)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



@dp.message(F.contact, Form.tel)
async def process_contact(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    tel = message.contact.phone_number
    await state.update_data(tel=tel)
    await message.answer(get_text(language, 'enter_photo'), reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.photo)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



@dp.message(F.photo, Form.photo)
async def process_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    fullname = data.get("fullname")
    age = data.get("age")
    tel = data.get("tel")

    await message.answer_photo(photo=photo,
                               caption=get_text(language, 'confirm').format(fullname=fullname, age=age, tel=tel),
                               reply_markup=get_confirm_keyboard(language))
    await state.set_state(Form.finish)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



@dp.message(Form.photo)
async def process_invalid_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    await message.answer(get_text(language, 'only_photo'))
    await state.set_state(Form.photo)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.callback_query(F.data.in_({"tasdiqlash", "bekor"}), Form.finish)
async def confirmation(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    if call.data == "tasdiqlash":
        await call.message.answer(get_text(language, 'approved'))
    else:
        await call.message.answer(get_text(language, 'retry'))

    await state.clear()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


if __name__ == "__main__":
    import asyncio


    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
