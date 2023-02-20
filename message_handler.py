from aiogram import Dispatcher, types
from main_interface.main_classes import Product, User, Text
from main_interface.run_main_bot import bot
from database.run_main_db import prod_tb, user_tb, text_tb
from keyboards import shop_keyboard, admin_keyboard
from main_interface.shop_call import del_unfilled
from hashlib import sha256


async def is_button(message: str, button_name) -> bool:
    texts = await Text(text_tb).get_texts(text_name=button_name)
    for text in texts:
        if text.text == message:
            return True
    return False


async def message_handler(message: types.Message):
    user = User(user_tb, message.from_user.id)
    texts = Text(text_tb)
    hash_password = await texts.get_const_text(language="en", text_name="admin_pswd")

    # Shop message, from main keyboard
    if await is_button(message=message.text, button_name="start_but1"):
        prod_dict = await Product(prod_tb).get_all_products()
        del_unfilled(prod_dict)  # Clear unfilled product objects
        # Check if list is not empty
        if len(prod_dict) == 0:
            raise Exception(f"No product objects in prod_list: {prod_dict}")
        product_key = next(iter(prod_dict.keys()))

        text = await texts.get_const_text(language=user.language(), text_name="product")
        keyboard = await shop_keyboard(user.language(), product_dict=prod_dict, current_key=product_key)
        product = prod_dict[product_key]
        text = text.format(product.title, product.price, product.description, product.vid_amount)

        await bot.send_photo(user.user_id, photo=product.prod_photo_id, caption=text, reply_markup=keyboard,
                             parse_mode="HTML")
    elif sha256(message.text.encode('utf-8')).hexdigest() == hash_password:
        await message.answer(text="admin", reply_markup=admin_keyboard())
    else:
        text = await texts.get_const_text(language=user.language(), text_name="msg_not_found")
        await message.answer(text=text)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(message_handler, lambda message: True)
