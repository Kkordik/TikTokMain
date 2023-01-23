from aiogram import Dispatcher, types
from main_interface.main_classes import Product
from database.run_main_db import prod_tb
from texts import text


async def shop_msg(message: types.Message):
    product = Product(prod_tb)
    all_products = await product.get_all_products()
    await message.answer("rgfsdf")


def register_main_shop_msg(dp: Dispatcher):
    dp.register_message_handler(shop_msg, lambda message: message.text in [val["start_but1"] for val in text.values()])