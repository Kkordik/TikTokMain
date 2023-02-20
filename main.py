import asyncio
from main_interface.run_main_bot import dp
from main_interface.start_cmd import register_main_start_cmd
from main_interface.shop_call import register_main_shop_call
from message_handler import register_message_handler
from main_interface.help_msg import register_main_help_msg
from main_interface.temporar import register_get_photo_id
from admin_interface.add_product import register_add_prod_call
from admin_interface.admin_cancel import register_admin_cancel


async def main(_loop):
    # Register handlers
    register_main_start_cmd(dp)
    register_main_shop_call(dp)
    register_message_handler(dp)
    register_main_help_msg(dp)
    register_get_photo_id(dp)
    register_add_prod_call(dp)
    register_admin_cancel(dp)

    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
