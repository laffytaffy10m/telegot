import sqlite3 as sq
from dispatcher import dp,bot

def sql_start():
    global base , cur
    base = sq.connect('kinobot.db')
    cur = base.cursor()
    if base:
        print('data base connect ok!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT,name TEXT,description TEXT,code TEXT PRIMARY KEY)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'\nНазвание: {ret[1]}\nОписание: {ret[2]}\nКод: {ret[-1]}')
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()
async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE code == ?',(data,))
    base.commit()