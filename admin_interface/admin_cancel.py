from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def admin_cancel_call(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.reply(text="CANCELED")


def register_admin_cancel(dp: Dispatcher):
    dp.register_callback_query_handler(admin_cancel_call, lambda call: call.data == "admin_cancel", state='*')
