import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import *
from main_interface.start_cmd import register_main_start_cmd

from classes.database_classes import Database, UsersTable


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def main(loop):
    # Register database and pool
    db = Database(HOST, USER, PASSWORD, NAME, PORT)
    await db.make_pool(loop)

    # Register user_table
    user_tb = UsersTable(db)

    # Register handlers
    register_main_start_cmd(dp)

    await user_tb.insert_vals(user_id=1111)

    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
