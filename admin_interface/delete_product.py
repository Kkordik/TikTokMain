from aiogram import Dispatcher, types
from main_interface.main_classes import Product
from database.run_main_db import prod_tb
from main_interface.run_main_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import adm_del_prod_keyboard


class ProdState(StatesGroup):
    prod_id = State()
    approve_deleting = State()


async def admin_delete_product(call: types.CallbackQuery):
    products = Product(prod_tb)
    all_products = await products.get_all_products()
    keyboard = adm_del_prod_keyboard(list(all_products.values()))
    await ProdState.prod_id.set()
    await call.message.reply(text="CHOOSE PRODUCT TO DELETE: ", reply_markup=keyboard)


async def delete_product_call(call: types.CallbackQuery, state=FSMContext):
    await state.update_data(prod_id=int(call.data.split(".")[1]))
    await ProdState.next()
    await call.message.reply(text="TO DELETE PRODUCT WITH ID {} SEND 'YES' : ".format(call.data.split(".")[1]))


async def approve_deleting(message: types.Message, state: FSMContext):
    products = Product(prod_tb)
    if message.text == "YES":
        data = await state.get_data()
        try:
            await products.table.delete_line(id=data["prod_id"])
            await message.reply(text="DELETED")
        except Exception as ex:
            await message.reply(text=ex)
    else:
        await message.reply(text="product not deleted")
    await state.finish()


def register_admin_del_product(dp: Dispatcher):
    dp.register_callback_query_handler(admin_delete_product, lambda call: call.data == "admin_delete_prod")
    dp.register_callback_query_handler(delete_product_call, lambda call: call.data.split(".")[0] == "admin_del_prod",
                                       state=ProdState.prod_id)
    dp.register_message_handler(approve_deleting, state=ProdState.approve_deleting)
