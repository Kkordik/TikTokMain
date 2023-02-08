from aiogram import Dispatcher, types
from main_interface.main_classes import User, Text
from database.run_main_db import user_tb, text_tb
from texts import text
from keyboards import start_keyboard


async def start_cmd(message: types.Message):
    user = User(user_tb, message.from_user.id)
    await user.insert_user()
    keyboard = await start_keyboard(user.language())
    texts = Text(text_tb)
    start_text = await texts.get_texts(language=user.language(), text_name="start_txt")
    print(start_text)
    await message.answer(start_text, reply_markup=keyboard, parse_mode="HTML")


def register_main_start_cmd(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start")
