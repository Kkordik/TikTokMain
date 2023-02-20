from aiogram import Dispatcher, types
from main_interface.main_classes import Product
from main_interface.run_main_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import adm_cancel_keyboard


async def admin_cancel_call(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.reply(text="CANCELED")


def register_admin_cancel(dp: Dispatcher):
    dp.register_callback_query_handler(admin_cancel_call, lambda call: call.data == "admin_cancel", state='*')
