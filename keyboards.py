from aiogram import types
from texts import text


def start_keyboard(language: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text[language]["start_but1"]),
                 types.KeyboardButton(text[language]["start_but2"]))
    return keyboard
