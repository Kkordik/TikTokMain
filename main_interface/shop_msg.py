from aiogram import Dispatcher, types
from main_interface.main_classes import Product, User, Text
from main_interface.run_main_bot import bot
from database.run_main_db import prod_tb, user_tb, text_tb
from keyboards import shop_keyboard
import asyncio


def del_unfilled(prod_dict: {Product}):
    for prod_id, product in prod_dict.items():
        if not product.check_full_filling():
            del prod_dict[prod_id]
            print(Warning(f"Product object is not filled fully: {product.__dict__}"))


async def is_button(message: str, button_name) -> bool:
    texts = await Text(text_tb).get_texts(text_name=button_name)
    for text in texts:
        if text.text == message:
            return True
    return False


async def shop_msg(message: types.Message):
    user = User(user_tb, message.from_user.id)

    if await is_button(message=message.text, button_name="start_but1"):
        prod_dict = await Product(prod_tb).get_all_products()
        del_unfilled(prod_dict)  # Clear unfilled product objects

        # Check if list is not empty
        if len(prod_dict) == 0:
            raise Exception(f"No product objects in prod_list: {prod_dict}")
        product_key = next(iter(prod_dict.keys()))

        texts = Text(text_tb)
        text = await texts.get_const_text(user.language(), "product")

        keyboard = await shop_keyboard(user.language(), product_dict=prod_dict, current_key=product_key)
        product = prod_dict[product_key]

        text = text.format(product.title, product.price, product.description, product.vid_amount)

        await bot.send_photo(user.user_id, photo=product.prod_photo_id, caption=text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer()


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
    text = await Text(text_tb).get_const_text(user.language(), "product")
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


def register_main_shop_msg(dp: Dispatcher):
    dp.register_message_handler(shop_msg, lambda message: True)
    dp.register_callback_query_handler(shop_move_callback, lambda call: call.data.split(".")[0] == "shop_move")
    dp.register_callback_query_handler(shop_buy_callback, lambda call: call.data.split(".")[0] == "shop_buy")
