from aiogram import types
from texts import text


def start_keyboard(language: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text[language]["start_but1"]),
                 types.KeyboardButton(text[language]["start_but2"]))
    return keyboard


def shop_keyboard(language: str, product_dict: dict, current_key: int):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    prod_key_list = list(product_dict.keys())
    current_id = prod_key_list.index(current_key)
    if (len(product_dict)-1 > current_id) and (current_id > 0):
        keyboard.add(types.InlineKeyboardButton(text=text[language]["shop_but_l"],
                                                callback_data="shop_move.{}".format(prod_key_list[current_id-1])),
                     types.InlineKeyboardButton(text=text[language]["shop_but_r"],
                                                callback_data="shop_move.{}".format(prod_key_list[current_id+1])))
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    elif len(product_dict)-1 > current_id:
        keyboard.add(types.InlineKeyboardButton(text=text[language]["shop_but_r"],
                                                callback_data="shop_move.{}".format(prod_key_list[current_id+1])))
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    elif current_id > 0:
        keyboard.add(types.InlineKeyboardButton(text=text[language]["shop_but_l"],
                                                callback_data="shop_move.{}".format(prod_key_list[current_id-1])))
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    else:
        keyboard.add(types.InlineKeyboardButton(text="buy", callback_data="shop_buy.{}".format(prod_key_list[current_id])))

    return keyboard
