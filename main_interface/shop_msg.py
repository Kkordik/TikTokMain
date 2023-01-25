from aiogram import Dispatcher, types, Bot
from main_interface.main_classes import Product, User
from main_interface.run_main_bot import bot
from database.run_main_db import prod_tb, user_tb
from texts import text
from keyboards import shop_keyboard


async def shop_msg(message: types.Message):
    user = User(user_tb, message.from_user.id)
    prod_list = await Product(prod_tb).get_all_products()
    product = prod_list[0]

    keyboard = shop_keyboard(user.language, product_list=prod_list, current_id=0)

    await bot.send_photo(user.user_id, photo=product.prod_photo_id, caption=product.description,
                         reply_markup=keyboard)


async def shop_callback(call: types.CallbackQuery):
    call_prod_id = int(call.data.split("_")[1])
    user = User(user_tb, call.from_user.id)
    prod_list = await Product(prod_tb).get_all_products()
    keyboard = shop_keyboard(user.language, product_list=prod_list, current_id=call_prod_id)
    await call.message.edit_media(types.InputMediaPhoto(media=prod_list[call_prod_id].prod_photo_id,
                                                        caption=prod_list[call_prod_id].description),
                                  reply_markup=keyboard)
    await call.answer()


def register_main_shop_msg(dp: Dispatcher):
    dp.register_message_handler(shop_msg, lambda message: message.text in [val["start_but1"] for val in text.values()])
    dp.register_callback_query_handler(shop_callback, lambda call: call.data.split("_")[0] == "shop")
