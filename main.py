import asyncio
from main_interface.run_main_bot import dp
from main_interface.start_cmd import register_main_start_cmd
from main_interface.shop_msg import register_main_shop_msg
from main_interface.help_msg import register_main_help_msg
# from main_interface.temporar import register_get_photo_id


async def main(_loop):
    # Register handlers
    register_main_start_cmd(dp)
    register_main_shop_msg(dp)
    register_main_help_msg(dp)
    #register_get_photo_id(dp)

    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
