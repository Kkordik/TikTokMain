from aiogram import Dispatcher, types
from texts import text


async def shop_msg(message: types.Message):
    await message.answer("rgfsdf")


def register_main_shop_msg(dp: Dispatcher):
    dp.register_message_handler(shop_msg, lambda message: message.text in [val["start_but1"] for val in text.values()])