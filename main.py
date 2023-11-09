from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import BotCommand
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import sqlite3

from app import database as db
from app import keyboards as kb
from osu import osu

import os
import datetime as dt
import pytz
import time as tm

tz = pytz.timezone('Asia/Yekaterinburg')

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)

# ============== Start bot ==============


async def on_startup(_):
    bot_commands = [
        BotCommand(command="/start", description="launch the bot"),
        BotCommand(command="/menu", description="call menu"),
        BotCommand(command="/us", description="view osu profile"),
        BotCommand(command="/bs", description="get user's top scores"),
        BotCommand(command="/ls", description="get user's last scores")
    ]
    await db.db_start()
    await bot.set_my_commands(bot_commands)

    TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
    DATE = (dt.datetime.now(tz)).strftime('%d.%m')
    print('Бот запущен:', TIME)
    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
        f.write(f'\n{TIME} {DATE}| Бот запущен')

# ============== Comand /start ==============


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.db_table_val(message, bot)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как администратор!', reply_markup=kb.main)
    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать в @best_osu_bot', reply_markup=kb.main)

# ============== Comand /menu ==============


@dp.message_handler(commands=['menu'])
async def cmd_start(message: types.Message):
    await db.db_table_val(message, bot)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вот что я могу сделать: ', reply_markup=kb.main)
    else:
        await message.answer(f'Вот что я могу сделать: ', reply_markup=kb.main)

# ============== Comand /us ==============


@dp.message_handler(commands=['us'])
async def us(message: types.Message):
    data = (message.text.split())
    if len(data) <= 1:
        await message.answer(f'Напиши ник пользователя после команды /us')
    else:
        await osu.get_osu_profile(bot, message, data[1])


# ============== Comand /bs ==============


@dp.message_handler(commands=['bs'])
async def us(message: types.Message):
    data = (message.text.split())
    if len(data) <= 1:
        await message.answer(f'Напиши ник пользователя после команды /bs')
    else:
        await osu.get_osu_best_scores(bot, message, data[1])

# ============== Comand /ls ==============


@dp.message_handler(commands=['ls'])
async def us(message: types.Message):
    data = (message.text.split())
    if len(data) <= 1:
        await message.answer(f'Напиши ник пользователя после команды /ls')
    else:
        await osu.last_scores(bot, message, data[1], 0)

# ============== StatesGroup ==============


class my_fsm(StatesGroup):
    osu_id = State()
    yourself = State()


@dp.callback_query_handler(text='user')
async def user(callback: types.CallbackQuery):
    await my_fsm.osu_id.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Напиши ник пользователя в osu!', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.osu_id)
async def user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await osu.get_osu_profile(bot, message, data)
    await state.finish()


@dp.callback_query_handler(text='yourself')
async def yourself(callback: types.CallbackQuery, state: FSMContext):
    await my_fsm.yourself.set()
    database = sqlite3.connect(
        'data/database.db', check_same_thread=False, timeout=7)
    cursor = database.cursor()
    cursor.execute(
        f'SELECT name_osu FROM users WHERE user_id = {callback.message.chat.id}')
    data = cursor.fetchone()
    print(data[0])
    if data[0] != None:
        await osu.get_osu_profile(bot, callback.message, data[0])
        await state.finish()
    else:
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Напиши свой ник в osu', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.yourself)
async def yourself(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await db.yourself_name(bot, message, data)
    await state.finish()

# ============== Another text(message) ==============


@dp.message_handler()
async def answer(message: types.Message):
    message_to_bot = message.text.lower()
    if message.content_type.lower() == 'text':
        if message_to_bot == 'меню' or message_to_bot == 'menu':
            await message.answer('Вот что я могу сделать: ', reply_markup=kb.main)
            await bot.delete_message(message.chat.id, message.message_id)
        else:
            await bot.send_message(message.chat.id, f'Вы написали: {message.text}\nЕсли хотите узнать что может бот напишите /menu\nБудут вопросы пишите: @Kinoki445', parse_mode='html')
            TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
            DATE = (dt.datetime.now(tz)).strftime('%d.%m')
            print(f'{TIME} {DATE} | Пользователь @{message.from_user.username} {message.from_user.first_name} написал {message.text}')
            await bot.delete_message(message.chat.id, message.message_id)
            try:
                with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                    f.write(
                        f'\n{TIME} {DATE}| Пользователь @{message.from_user.username} {message.from_user.first_name} написал {message.text}')
            except:
                pass

# ============== FSM cancel ==============


@dp.callback_query_handler(state="*", text='close_callback')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Я отменил твой запрос', reply_markup=kb.main)
    await state.finish()

# ============== callback data ==============


@dp.callback_query_handler()
async def callback_query_keyboard(callback: types.CallbackQuery):
    if callback.data == 'close':
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            try:
                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Вот что я могу сделать: ', reply_markup=kb.main)
            except:
                await callback.message.delete()
                await callback.message.answer(f'Вот что я могу сделать: ', reply_markup=kb.main)
            else:
                await callback.message.delete()
                await callback.message.answer(f'Вот что я могу сделать: ', reply_markup=kb.main)

    elif callback.data[0:3] == 'bs:':
        await osu.get_osu_best_scores(bot, callback, callback.data[3:])

    elif callback.data[0:3] == 'ls:':
        info = callback.data.split(':')
        await osu.last_scores(bot, callback, info[1], int(info[2]))

    elif callback.data[0:3] == 'll:':
        info = callback.data.split(':')
        await osu.last_score(bot, callback, info[2], info[1])

    elif callback.data[0:3] == 'ps:':
        info = callback.data.split(':')
        await osu.get_score(bot, callback, info[2], info[1])

    elif callback.data[0:3] == 'pf:':
        info = callback.data.split(':')
        await osu.get_osu_profile(bot, callback, info[1])

# ============== Start __main__ ==============

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
