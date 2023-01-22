import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from main_interface.start_cmd import register_main_start_cmd
from main_interface.shop_msg import register_main_shop_msg
from main_interface.help_msg import register_main_help_msg


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def main(_loop):
    # Register handlers
    register_main_start_cmd(dp)
    register_main_shop_msg(dp)
    register_main_help_msg(dp)

    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
