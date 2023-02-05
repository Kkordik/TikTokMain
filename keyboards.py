from aiogram import types
from texts import text
from main_interface.main_classes import Product


def start_keyboard(language: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text[language]["start_but1"]),
                 types.KeyboardButton(text[language]["start_but2"]))
    return keyboard


def shop_keyboard(language: str, product_list: list[Product], current_id: int):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    if (len(product_list)-1 > current_id) and (current_id > 0):
        keyboard.add(types.InlineKeyboardButton(text=text[language]["shop_but_l"],
                                                callback_data="shop_move.{}".format(current_id-1)),
                     types.InlineKeyboardButton(text=text[language]["shop_but_r"],
                                                callback_data="shop_move.{}".format(current_id+1)))
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(current_id)))

    elif len(product_list)-1 > current_id:
        keyboard.add(types.InlineKeyboardButton(text=text[language]["shop_but_r"],
                                                callback_data="shop_move.{}".format(current_id+1)))
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(current_id)))

    elif current_id > 0:
        keyboard.add(types.InlineKeyboardButton(text=text[language]["shop_but_l"],
                                                callback_data="shop_move.{}".format(current_id-1)))
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(current_id)))

    else:
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(current_id)))

    return keyboard
