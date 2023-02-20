from aiogram import Dispatcher, types
from main_interface.main_classes import Product, User, Text
from main_interface.run_main_bot import bot
from database.run_main_db import prod_tb, user_tb, text_tb
from keyboards import shop_keyboard


def del_unfilled(prod_dict: {Product}):
    for prod_id, product in prod_dict.items():
        if not product.check_full_filling():
            del prod_dict[prod_id]
            print(Warning(f"Product object is not filled fully: {product.__dict__}"))


async def shop_move_callback(call: types.CallbackQuery):
    call_prod_key = int(call.data.split(".")[1])
    user = User(user_tb, call.from_user.id)

    prod_dict = await Product(prod_tb).get_all_products()
    del_unfilled(prod_dict)  # Clear unfilled product objects

    # Check if required id of product is into product list
    if call_prod_key not in prod_dict:
        text = await Text(text_tb).get_const_text(user.language(), "no_prod_found")
        await call.answer(text=text)
        raise Exception(f"No product object in list with id {call_prod_key} : {prod_dict}")

    keyboard = await shop_keyboard(user.language(), product_dict=prod_dict, current_key=call_prod_key)
    product = prod_dict[call_prod_key]
    text = str(await Text(text_tb).get_const_text(user.language(), "product"))
    photo = types.InputMediaPhoto(media=product.prod_photo_id,
                                  caption=text.format(product.title, product.price, product.description,
                                                      product.vid_amount),
                                  parse_mode="HTML")
    await call.message.edit_media(photo, reply_markup=keyboard)
    await call.answer()


async def shop_buy_callback(call: types.CallbackQuery):
    call_prod_key = int(call.data.split(".")[1])
    user = User(user_tb, call.from_user.id)

    text = await Text(text_tb).get_const_text(user.language(), "choose_payment")

    photo = types.InputMediaPhoto(media="AgACAgIAAxkBAAIEQGPirOxF-hFpE8I3-nuOTMgbCHMuAAJCxzEb4FoQS_3Zb74n_0kOAQADAgADcwADLgQ",
                                  caption=text, parse_mode="HTML")
    await call.message.edit_media(media=photo, reply_markup=None)
    await call.answer()


def register_main_shop_call(dp: Dispatcher):
    dp.register_callback_query_handler(shop_move_callback, lambda call: call.data.split(".")[0] == "shop_move")
    dp.register_callback_query_handler(shop_buy_callback, lambda call: call.data.split(".")[0] == "shop_buy")
