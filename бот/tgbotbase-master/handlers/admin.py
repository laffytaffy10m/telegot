from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types
from dispatcher import dp
from aiogram.dispatcher.filters import Text
from dispatcher import bot
from data_base import sqlite_db
from keybords import client
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    code = State()


@dp.message_handler(commands=['moderator'],is_chat_admin=True)
async def make_changes_command(message:types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id,'да мой господин',reply_markup=client.button_case_admin)
    await message.delete()
#Начало диолога загрузки
@dp.message_handler(commands='Download',state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузить фото')
#Первый ответ
@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message:types.Message,state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')
#Второй ответ
@dp.message_handler(state=FSMAdmin.name)
async def load_name(message:types.Message,state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')
#Третий ответ
@dp.message_handler(state=FSMAdmin.description)
async def load_description(message:types.Message,state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи код для фильма')
@dp.message_handler(state=FSMAdmin.code)
async def load_code(message:types.Message,state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['code'] = (message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} удалена', show_alert=True)

@dp.message_handler(commands=['delete'])
async def delete_item(message:types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0],f'\nНазвание: {ret[1]}\nОписание: {ret[2]}\nКод: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[-1]}', callback_data=f'del {ret[-1]}')))




@dp.message_handler(state="*",commands='cancel')
@dp.message_handler(Text(equals='отмена',ignore_case=True),state="*")
async def cancel_handler(message:types.Message,state:FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Ок')
    await state.finish()