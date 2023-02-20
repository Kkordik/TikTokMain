from aiogram import Dispatcher, types
from main_interface.main_classes import Text, Product
from database.run_main_db import text_tb, prod_tb
from main_interface.run_main_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import adm_cancel_keyboard


class ProdState(StatesGroup):
    prod_title = State()
    prod_description = State()
    prod_price = State()
    prod_vid_amount = State()
    prod_photo_id = State()
    approve_adding = State()


async def add_prod_call(call: types.CallbackQuery):
    await ProdState.prod_title.set()
    await bot.send_message(call.message.chat.id, text="1. Send product title: ", reply_markup=adm_cancel_keyboard())


async def prod_title(message: types.Message, state: FSMContext):
    await state.update_data(prod_title=message.text)
    await ProdState.next()
    await bot.send_message(message.chat.id, text="2. Send product description: ",
                           reply_markup=adm_cancel_keyboard())


async def prod_description(message: types.Message, state: FSMContext):
    await state.update_data(prod_description=message.text)
    await ProdState.next()
    await bot.send_message(message.chat.id, text="3. Send product price (text, not only numbers): ",
                           reply_markup=adm_cancel_keyboard())


async def prod_price(message: types.Message, state: FSMContext):
    await state.update_data(prod_price=message.text)
    await ProdState.next()
    await bot.send_message(message.chat.id, text="4. Send product video amount (number): ",
                           reply_markup=adm_cancel_keyboard())


async def prod_vid_amount(message: types.Message, state: FSMContext):
    await state.update_data(prod_vid_amount=int(message.text))
    await ProdState.next()
    await bot.send_message(message.chat.id, text="5. Send product photo (DO NOT DELETE THAT PHOTO AFTER SENDING):",
                           reply_markup=adm_cancel_keyboard())


async def prod_photo_id(message: types.Message, state: FSMContext):
    await state.update_data(prod_photo_id=message.photo[0].file_id)
    data = await state.get_data()
    text = str(await Text(text_tb).get_const_text("ru", "product"))
    await bot.send_photo(message.chat.id, photo=data["prod_photo_id"],
                         caption=text.format(data["prod_title"], data["prod_price"], data["prod_description"],
                                             data["prod_vid_amount"]), parse_mode="HTML")
    await bot.send_message(message.chat.id, text="CHECK ALL DATA AND SEND 'YES' TO ADD IT TO DATABASE",
                           reply_markup=adm_cancel_keyboard())
    await ProdState.next()


async def approve_adding(message: types.Message, state: FSMContext):
    products = Product(prod_tb)
    if message.text == "YES":
        data = await state.get_data()
        try:
            await products.table.insert_vals(prod_title=data["prod_title"], prod_price=data["prod_price"],
                                             prod_descr=data["prod_description"], vid_amount=data["prod_vid_amount"],
                                             prod_photo=data["prod_photo_id"])
            await message.reply(text="ADDED")
        except Exception as ex:
            await message.reply(text=ex)
    else:
        await message.reply(text="product not added")
    await state.finish()


def register_add_prod_call(dp: Dispatcher):
    dp.register_callback_query_handler(add_prod_call, lambda call: call.data == "admin_add_prod")
    dp.register_message_handler(prod_title, state=ProdState.prod_title)
    dp.register_message_handler(prod_description, state=ProdState.prod_description)
    dp.register_message_handler(prod_price, state=ProdState.prod_price)
    dp.register_message_handler(prod_vid_amount, state=ProdState.prod_vid_amount)
    dp.register_message_handler(prod_photo_id, content_types=["photo"], state=ProdState.prod_photo_id)
    dp.register_message_handler(approve_adding, state=ProdState.approve_adding)
