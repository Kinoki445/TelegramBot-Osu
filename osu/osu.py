from app import keyboards as kb
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
import flag


async def get_osu_profile(bot, message, data):
    try:
        await message.delete()
    except:
        await message.message.delete()
    user = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_user?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={data}').text)

    for i in user:
        osu_id = (int(i['user_id']))
        name = (i['username'])
        level = (i['level'])
        rank = (i['pp_rank'])
        rank_c = (i['pp_country_rank'])
        pp = (i['pp_raw'])
        acc = (float(i['accuracy']))
        country = (i['country'])
        playcounts = (float(i['total_seconds_played'])/3600)
        ss = (i['count_rank_ss'])
        ssh = (i['count_rank_ssh'])
        s = (i['count_rank_s'])
        sh = (i['count_rank_sh'])
        a = (i['count_rank_a'])

    text = (f'▸ <a href="https://osu.ppy.sh/users/{osu_id}">{name}</a>\n▸ <b>Playcount:</b> {round(playcounts, 3)}hrs\n▸ <b>level:</b> {level}\n▸ <b>Rank</b> #{rank} (<b> {flag.flag(country)}: </b>#{rank_c})\n▸ <b>PP:</b> {pp} <b>Acc:</b> {round(acc, 2)}%' +
            f'\n▸ <b>SS</b> {ss} <b>SSh</b> {ssh} <b>S</b> {s} <b>Sh</b> {sh} <b>A</b> {a}')

    more_user = InlineKeyboardMarkup()
    more_user.add(InlineKeyboardButton(text="best score", callback_data=f"bs:{osu_id}"),
                InlineKeyboardButton(text="last scores", callback_data=f"ls:{osu_id}:0"))
    more_user.add(InlineKeyboardButton(
        text="another user", callback_data="user"))
    more_user.add(InlineKeyboardButton(
        text='🔙back', callback_data='close_callback'))

    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message_id-1, text=f'{text}', parse_mode=ParseMode.HTML, reply_markup=more_user)
    except:
        try:
            await bot.send_message(message.chat.id, text=f'{text}', parse_mode=ParseMode.HTML, reply_markup=more_user)
        except:
            await bot.send_message(message.message.chat.id, text=f'{text}', parse_mode=ParseMode.HTML, reply_markup=more_user)


async def get_osu_best_scores(bot, message, data):
    try:
        await message.message.delete()
    except:
        await message.answer(f'Подожди собираю скоры {data}....')

    user = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_user?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={data}').text)

    for i in user:
        name = (i['username'])

    score = InlineKeyboardMarkup()
    user_best = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_user_best?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={data}').text)
    for i in user_best:
        id_map = (i['beatmap_id'])
        pp = i['pp']
        osu_map = json.loads(requests.get(
            f'https://osu.ppy.sh/api/get_beatmaps?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&b={id_map}').text)
        for i in osu_map:
            title = i['title']
            beatmap_id = i['beatmap_id']
            score.add(InlineKeyboardButton(
                text=(f'{title} | {pp} pp'), callback_data=f'ps:{beatmap_id}:{data}'))
    score.add(InlineKeyboardButton(
        text='🔙Назад', callback_data='close_callback'))
    try:
        await bot.send_message(message.message.chat.id, f'Все топ скоры <a href = "https://osu.ppy.sh/users/{data}">{name}</a>', parse_mode=ParseMode.HTML, reply_markup=score)
    except:
        await bot.send_message(message.chat.id, f'Все топ скоры <a href = "https://osu.ppy.sh/users/{data}">{name}</a>', parse_mode=ParseMode.HTML, reply_markup=score)

async def send_message(bot, message, data, user_id, map_id, list):
    back = InlineKeyboardMarkup()

    map = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_beatmaps?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&b={map_id}').text)

    for i in map:
        title = i['title']
        starts = (round(float(i['difficultyrating']), 2))
        bpm = i['bpm']
        maxcombo = i['max_combo']
        bitset = i['beatmapset_id']
        creator_id = i['creator_id']
        creator = i['creator']
        version = i['version']

    if data[0] == ('bs'):
        back.add(InlineKeyboardButton(text='🔙Назад', callback_data=f'pf:{user_id}'))

        if int(data[3]) == 1:
            fc = f'{data[2]}/{maxcombo} <b>FC</b>'
        else:
            fc = f'{maxcombo}/{data[2]}'

        if data[9] == '0':
            mods = '+NoMod'
        elif data[9] == '8':
            mods = '+HD'
        elif data[9] == '16':
            mods = '+HR'
        elif data[9] == '32':
            mods = '+SD'
        elif data[9] == '64':
            mods = '+DT'
        elif data[9] == '72':
            mods = '+HDDT'
        elif data[9] == '24':
            mods = '+HDHR'
        elif data[9] == '1,112':
            mods = '+HDHRDTFL'

        await bot.send_photo(message.message.chat.id, photo=f'https://assets.ppy.sh/beatmaps/{bitset}/covers/cover.jpg', caption=f'● <a href = "https://osu.ppy.sh/beatmapsets/{bitset}#osu/{map_id}">{title} [{version}]</a> / <a href="https://osu.ppy.sh/users/{creator_id}">{creator}</a>\n● ★{starts} <b>BPM:</b> {bpm} <b>{mods}</b>\n● <b>{data[11]}</b> ▸<b>{data[12]}pp</b> ▸<b>{data[8]}</b>% \n● {data[1]} ▸x{fc} [{data[6]}/{data[5]}/{data[4]}/{data[7]}]\n● <b>Score Set:</b> {data[10]}', parse_mode=ParseMode.HTML, reply_markup=back)
    else:
        all_list = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_user_recent?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={user_id}').text)


        if (len(all_list)-1) == list:
            back.add(InlineKeyboardButton(text='⬅️', callback_data=f'ls:{user_id}:{list-1}'),
                    InlineKeyboardButton(text='🔙Назад', callback_data=f'pf:{user_id}'))
        elif list == 0:
            back.add(InlineKeyboardButton(text='➡️', callback_data=f'ls:{user_id}:{list+1}'),
                    InlineKeyboardButton(text='🔙Назад', callback_data=f'pf:{user_id}'))
        else:
            back.add(InlineKeyboardButton(text='⬅️', callback_data=f'ls:{user_id}:{list-1}'),
                    InlineKeyboardButton(text='➡️', callback_data=f'ls:{user_id}:{list+1}'))
            back.add(InlineKeyboardButton(text='🔙Назад', callback_data=f'pf:{user_id}'))

        if int(data[3]) == 1:
            fc = f'{data[3]}/{maxcombo} <b>FC</b>'
        else:
            fc = f'{maxcombo}/{data[2]}'
            
        if int(data[8]) == 0:
            mods = '+NoMod'
        elif int(data[8]) == 8:
            mods = '+HD'
        elif int(data[8]) == 16:
            mods = '+HR'
        elif int(data[8]) == 32:
            mods = '+SD'
        elif int(data[8]) == 64:
            mods = '+DT'
        elif int(data[8]) == 72:
            mods = '+HDDT'
        elif int(data[8]) == 24:
            mods = '+HDHR'
        elif int(data[8]) == 1112:
            mods = '+HDHRDTFL'
        else:
            mods = '+MODS'

        try:
            await message.message.delete()
        except:
            await message.delete()

        try:
            await bot.send_photo(message.message.chat.id, photo=f'https://assets.ppy.sh/beatmaps/{bitset}/covers/cover.jpg', caption=(
                f'▸ <a href ="https://osu.ppy.sh/beatmapsets/{bitset}#osu/{map_id}">{title} [{version}]</a> / <a href="https://osu.ppy.sh/users/{creator_id}">{creator}</a>\n● ★{starts} <b>BPM: </b>{bpm} <b>{mods}</b>\n● {data[1]} ▸<b>{data[7]}%</b>\n● x{data[2]}/{maxcombo} [{data[5]}/{data[4]}/{data[3]}/{data[6]}]'), parse_mode=ParseMode.HTML, reply_markup=back)
        except:
            await bot.send_photo(message.chat.id, photo=f'https://assets.ppy.sh/beatmaps/{bitset}/covers/cover.jpg', caption=(
                f'▸ <a href ="https://osu.ppy.sh/beatmapsets/{bitset}#osu/{map_id}">{title} [{version}]</a> / <a href="https://osu.ppy.sh/users/{creator_id}">{creator}</a>\n● ★{starts} <b>BPM: </b>{bpm} <b>{mods}</b>\n● {data[1]} ▸<b>{data[7]}%</b>\n● x{data[2]}/{maxcombo} [{data[5]}/{data[4]}/{data[3]}/{data[6]}]'), parse_mode=ParseMode.HTML, reply_markup=back)


async def get_score(bot, message, user_id, map_id):
    user = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_scores?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&b={map_id}&u={user_id}').text)

    user = user[0]

    user_score_map = []
    user_score_map.append('bs')
    user_score_map.append(user['score'])
    user_score_map.append(user['maxcombo'])
    user_score_map.append(user['perfect'])

    user_score_map.append(int(user['count50']))
    user_score_map.append(int(user['count100']))
    user_score_map.append(int(user['count300']))
    user_score_map.append(int(user['countmiss']))

    user_score_map.append(round((300*user_score_map[6]+100*user_score_map[5]+50*user_score_map[4]) /
                                (300*(user_score_map[6]+user_score_map[5]+user_score_map[4]+user_score_map[7]))*100, 2))

    user_score_map.append(user['enabled_mods'])
    user_score_map.append(user['date'])
    user_score_map.append(user['rank'])
    user_score_map.append(user['pp'])

    await send_message(bot, message, user_score_map, user_id, map_id, 0)


async def last_scores(bot, callback, user_id, list):
    try:
        await callback.answer(f'Подожди собираю скоры {user_id}....')
    except:
        pass
    
    last_scores = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_user_recent?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={user_id}').text)

    user_score_map = []
    user_score_map.append('ls')
    i = last_scores[list]

    beatmap = (i['beatmap_id'])
    user_score_map.append(i['score'])
    user_score_map.append(i['maxcombo'])
    
    user_score_map.append(int(i['count50']))
    user_score_map.append(int(i['count100']))
    user_score_map.append(int(i['count300']))
    user_score_map.append(int(i['countmiss']))

    user_score_map.append(round((300*user_score_map[5]+100*user_score_map[4]+50*user_score_map[3]) /
                    (300*(user_score_map[5]+user_score_map[4]+user_score_map[3]+user_score_map[6]))*100, 2))

    user_score_map.append(i['enabled_mods'])
    
    await send_message(bot, callback, user_score_map, user_id, beatmap, list)

    # score = InlineKeyboardMarkup()
    # last_scores = json.loads(requests.get(
    #     f'https://osu.ppy.sh/api/get_user_recent?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={user_id}').text)

    # for i in last_scores:
    #     beatmap_id = i['beatmap_id']
    #     rank = i['rank']
    #     map = json.loads(requests.get(
    #         f'https://osu.ppy.sh/api/get_beatmaps?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&b={beatmap_id}').text)
    #     for i2 in map:
    #         title = i2['title']
    #         score.add(InlineKeyboardButton(
    #             text=(f'{title} | {rank}'), callback_data=f'll:{beatmap_id}:{user_id}'))

    # score.add(InlineKeyboardButton(
    #     text=(f'🔙 Назад'), callback_data=f'pf:{user_id}'))

    # try:
    #     await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Последние сыгранные карты пользователя!', parse_mode=ParseMode.HTML, reply_markup=score)
    # except:
    #     try:
    #         await callback.message.delete()
    #         await bot.send_message(callback.message.chat.id, text='Последние сыгранные карты пользователя!', parse_mode=ParseMode.HTML, reply_markup=score)
    #     except:
    #         await callback.delete()
    #         await bot.send_message(callback.chat.id, text='Последние сыгранные карты пользователя!', parse_mode=ParseMode.HTML, reply_markup=score)


async def last_score(bot, message, user, beatmap):
    last_scores = json.loads(requests.get(
        f'https://osu.ppy.sh/api/get_user_recent?k=a8050a07315b64fc12f2933742ec33b9e9f8016b&u={user}').text)

    user_score_map = []
    user_score_map.append('ls')

    for i in last_scores[0]:
        beatmap_id = i['beatmap_id']

        if beatmap == beatmap_id:
            user_score_map.append(i['score'])
            user_score_map.append(i['maxcombo'])
            
            user_score_map.append(int(i['count50']))
            user_score_map.append(int(i['count100']))
            user_score_map.append(int(i['count300']))
            user_score_map.append(int(i['countmiss']))

            user_score_map.append(round((300*user_score_map[5]+100*user_score_map[4]+50*user_score_map[3]) /
                            (300*(user_score_map[5]+user_score_map[4]+user_score_map[3]+user_score_map[6]))*100, 2))

            user_score_map.append(i['enabled_mods'])
    
    await send_message(bot, message, user_score_map, user, beatmap)
