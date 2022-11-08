from aiogram import executor
from dispatcher import dp
import handlers
from handlers import admin
from data_base import sqlite_db

async def on_startup(_):
    sqlite_db.sql_start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)

