from aiogram import types
from main_interface.main_classes import Text
from database.run_main_db import text_tb


async def start_keyboard(language: str):
    texts = Text(text_tb)
    but1_text = await texts.get_const_text(language=language, text_name="start_but1")
    but2_text = await texts.get_const_text(language=language, text_name="start_but2")
    print(but1_text, "\n", but2_text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(but1_text),
                 types.KeyboardButton(but2_text))
    return keyboard


async def shop_keyboard(language: str, product_dict: dict, current_key: int):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    prod_key_list = list(product_dict.keys())
    current_id = prod_key_list.index(current_key)

    texts = Text(text_tb)
    but_l_text = await texts.get_const_text(language=language, text_name="shop_but_l")
    but_r_text = await texts.get_const_text(language=language, text_name="shop_but_r")
    but_buy_text = await texts.get_const_text(language=language, text_name="buy")

    if (len(product_dict)-1 > current_id) and (current_id > 0):
        keyboard.add(types.InlineKeyboardButton(text=but_l_text,
                                                callback_data="shop_move.{}".format(prod_key_list[current_id-1])),
                     types.InlineKeyboardButton(text=but_r_text,
                                                callback_data="shop_move.{}".format(prod_key_list[current_id+1])))
        keyboard.add(types.InlineKeyboardButton(text=but_buy_text, callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    elif len(product_dict)-1 > current_id:
        keyboard.add(types.InlineKeyboardButton(text=but_r_text,
                                                callback_data="shop_move.{}".format(prod_key_list[current_id+1])))
        keyboard.add(types.InlineKeyboardButton(text=but_buy_text, callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    elif current_id > 0:
        keyboard.add(types.InlineKeyboardButton(text=but_l_text,
                                                callback_data="shop_move.{}".format(prod_key_list[current_id-1])))
        keyboard.add(types.InlineKeyboardButton(text=but_buy_text, callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    else:
        keyboard.add(types.InlineKeyboardButton(text=but_buy_text, callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    return keyboard


def admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="add product", callback_data="admin_add_prod"))
    return keyboard


def adm_cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="cancel", callback_data="admin_cancel"))
    return keyboard
