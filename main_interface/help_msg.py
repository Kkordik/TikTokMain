from aiogram import Dispatcher, types
from texts import text


async def shop_msg(message: types.Message):
    await message.answer("sdfsdfsdfgtryjtmyu ")


def register_main_help_msg(dp: Dispatcher):
    dp.register_message_handler(shop_msg, lambda message: message.text in [val["start_but2"] for val in text.values()])