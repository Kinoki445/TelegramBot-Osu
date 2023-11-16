import sqlite3
import datetime
import pytz
import os
from app import keyboards as kb
from osu import osu

tz = pytz.timezone('Asia/Yekaterinburg')
TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
DATE = (datetime.datetime.now(tz)).strftime('%d.%m')

# ============== Create tables ==============


async def db_start():
    global database, cursor
    database = sqlite3.connect(
        'data/database.db', check_same_thread=False, timeout=7)
    cursor = database.cursor()
    print("Подключен к SQLite3")
    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
        f.write(f'\n{TIME} {DATE}| Подключен к SQLite3')

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        user_id INTEGER UNIQUE NOT NULL,
        user_name TEXT NOT NULL,
        username STRING NOT NULL,
        osu_id INTEGER,
        name_osu STRING,
        join_date DATETIME NOT NULL
        )""")
    database.commit()


async def yourself_name(bot, message, data):
    cursor.execute(
        f"""UPDATE users SET name_osu = '{data}' WHERE user_id = {message.chat.id}""")
    database.commit()
    await osu.get_osu_profile(bot, message, data)


async def change_nick(bot, message, data):
    cursor.execute(
        f"""UPDATE users SET name_osu = '{data}' WHERE user_id = {message.chat.id}""")
    database.commit()
    await message.answer(f'Я поменял твой ник на: {data}', reply_markup=kb.main)

# ============== New users ==============


async def db_table_val(message, bot):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    username = message.from_user.username
    today = datetime.date.today()
    joindate = today.strftime('%d.%m.%Y')
    user = cursor.execute(
        f'SELECT * FROM users WHERE user_id = {us_id} ').fetchone()
    if user is None:
        cursor.execute('INSERT INTO users (user_id, user_name, username, join_date) VALUES (?, ?, ?, ?)',
                    (us_id, us_name, username, joindate))
        database.commit()
        await bot.send_message(chat_id=os.getenv('ADMIN_ID'), text=f'Зарегестрировался новый пользователь! @{username}, {us_name}')
        print(f'Пользователь {message.from_user.username} {message.from_user.first_name} зарегестрировался! в', (
            datetime.datetime.now(tz).strftime('%H:%M:%S')))
        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
            f.write(
                f'\n{TIME} {DATE}| Пользователь {message.from_user.username} {message.from_user.first_name} зарегестрировался!')
