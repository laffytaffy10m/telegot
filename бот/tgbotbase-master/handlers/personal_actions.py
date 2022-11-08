import bot
from aiogram import types, Dispatcher
from dispatcher import dp
from dispatcher import bot
import config
from data_base import sqlite_db
#from keybords import kb_client --- импортируем кнопки если они будут

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Напиши /code для получения фильма')#,reply_markup=kb_client#)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напиши ему:\nhttps://t.me/chikibobiBot')
@dp.message_handler(commands=['code'])
async def kinocode(message:types.Message):
    await sqlite_db.sql_read(message)

#@dp.message_handler(content_types=['text'])
#async def code(message: types.Message):
   # if message.text =='101':
    #    await bot.send_message(message.from_user.id,'яйца')



#@dp.message_handler(is_owner=True,commands=['setfilm'])
#async def setlink_commands(message: types.Message):
 #   with open('link.txt','w+') as f:
   #     f.write(message.text.replace('/setfilm', '').strip())
    #    f.close()
  #  await message.answer('Фильм успешно сохранен')

#@dp.message_handler(is_owner=True,commands=['getfilm'])
#async def getlink_commands(message: types.Message):
  #  with open('link.txt','r') as f:
  #      content = f.readlines()
  #      f.close()
   # await message.answer('Текущий фильм: {}'.format(content[0].strip()))

