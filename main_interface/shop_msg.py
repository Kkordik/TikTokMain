from aiogram import Dispatcher, types
from main_interface.main_classes import Product, User
from main_interface.run_main_bot import bot
from database.run_main_db import prod_tb, user_tb
from texts import text
from keyboards import shop_keyboard


def del_unfilled(prod_dict: {Product}):
    for prod_id, product in prod_dict.items():
        if not product.check_full_filling():
            del prod_dict[prod_id]
            print(Warning(f"Product object is not filled fully: {product.__dict__}"))


async def shop_msg(message: types.Message):
    user = User(user_tb, message.from_user.id)
    prod_dict = await Product(prod_tb).get_all_products()
    del_unfilled(prod_dict)
    if len(prod_dict) == 0:
        raise Exception(f"No product objects in prod_list: {prod_dict}")
    product_key = next(iter(prod_dict.keys()))
    keyboard = shop_keyboard(user.language(), product_dict=prod_dict, current_key=product_key)

    await bot.send_photo(user.user_id, photo=prod_dict[product_key].prod_photo_id, caption=prod_dict[product_key].description,
                         reply_markup=keyboard)


async def shop_move_callback(call: types.CallbackQuery):
    call_prod_key = int(call.data.split(".")[1])
    user = User(user_tb, call.from_user.id)
    prod_dict = await Product(prod_tb).get_all_products()
    del_unfilled(prod_dict)
    if call_prod_key not in prod_dict:
        await call.answer(text=text[user.language()]["no_prod_found"])
        raise Exception(f"No product object in list with id {call_prod_key} : {prod_dict}")
    keyboard = shop_keyboard(user.language(), product_dict=prod_dict, current_key=call_prod_key)
    await call.message.edit_media(types.InputMediaPhoto(media=prod_dict[call_prod_key].prod_photo_id,
                                                        caption=prod_dict[call_prod_key].description),
                                  reply_markup=keyboard)
    await call.answer()


async def shop_buy_callback(call: types.CallbackQuery):
    await call.answer(text="sdfsdvrebtgvr6en7trnb")


def register_main_shop_msg(dp: Dispatcher):
    dp.register_message_handler(shop_msg, lambda message: message.text in [val["start_but1"] for val in text.values()])
    dp.register_callback_query_handler(shop_move_callback, lambda call: call.data.split(".")[0] == "shop_move")
    dp.register_callback_query_handler(shop_buy_callback, lambda call: call.data.split(".")[0] == "shop_buy")
