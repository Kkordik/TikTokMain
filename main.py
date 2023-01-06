from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import BOT_TOKEN
from main_interface.start_cmd import register_main_start_cmd

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


if __name__ == '__main__':
    register_main_start_cmd(dp)
    executor.start_polling(dp)
