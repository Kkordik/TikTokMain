from aiogram import Dispatcher, types
from main_interface.main_classes import User
from database.run_main_db import user_tb
from texts import text
from keyboards import start_keyboard


async def start_cmd(message: types.Message):
    user = User(user_tb, message.from_user.id)
    await user.insert_user()
    await message.answer(text[user.language]["start_txt"], reply_markup=start_keyboard(user.language))


def register_main_start_cmd(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start")
