from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def start_cmd(message: types.Message):
    await message.answer("hi its a bot")


def register_main_start_cmd(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start")
