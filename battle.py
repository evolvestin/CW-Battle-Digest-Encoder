# -*- coding: utf-8 -*-
import os
import re
import asyncio
import gspread
import objects
import _thread
import requests
from time import sleep
from aiogram import types
from bs4 import BeautifulSoup
from collections import Counter
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from objects import bold, code, stamper, log_time
stamp1 = objects.time_now()
objects.environmental_files(python=True)
Auth = objects.AuthCentre(os.environ['TOKEN'])
# ====================================================================================
idMe = 396978030
last_post_id = None
async_blocking = None
checker_blocking = None
eight_hours = 8 * 60 * 60
main_address = 'https://t.me/ChatWarsDigest/'
castle_dict = {'🖤': 'Скала', '🍆': 'Ферма', '🐢': 'Тортуга',
               '🌹': 'Замок Рассвета', '🍁': 'Амбер', '☘': 'Оплот', '🦇': 'Ночной Замок'}
standard_command_list = ['/place', '/season', '/average', '/summary', '/worldtop']
castle_names_search = '(' + '|'.join(castle_dict.values()) + ')'
castle_search = '(' + '|'.join(castle_dict) + ')'
battle_patterns = {
    'со значительным преимуществом': '⚔😎',
    'успешно атаковали защитников': '⚔',
    'разыгралась настоящая бойня, но все-таки силы атакующих были ': '⚔⚡',
    'успешно отбились от': '🛡',
    'легко отбились от': '🛡👌',
    'героически отразили ': '🛡⚡',
    'скучали, на них ': '🛡😴'}


def worldtop_encoder(top):
    response_dict = {}
    response_stamp = 0
    top = re.sub('[️🏅]', '', re.sub(r'\s+', ' ', top))
    top = re.sub(castle_names_search, '', top).split('/')
    if len(top):
        text_stamp = re.sub(r'\D', '', top[0])
        if len(text_stamp):
            response_stamp = int(text_stamp)
            for string in top:
                search = re.search(r'#\s\d\s(.*?)\s(\d+)\s🏆 очков', string)
                if search:
                    response_dict[search.group(1)] = int(search.group(2))
    return response_stamp, response_dict


def creation_google_values():
    from timer import timer
    battle_sheet = gspread.service_account('1.json').open('Digest').worksheet('main')
    top_sheet = gspread.service_account('2.json').open('Digest').worksheet('top')
    battle_values = battle_sheet.col_values(1)
    top_values = top_sheet.col_values(1)
    battles = {}
    tops = {}
    for array in [Counter(battle_values), Counter(top_values)]:
        for value in array:
            battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', value)
            if battle_search:
                indexer = battle_values
                post_id = str(value.split('/')[0])
                battles[timer(battle_search)] = re.sub('️', '', value)
                except_text = code('Element id:') + objects.html_link(main_address + post_id, post_id)
            else:
                indexer = top_values
                stamp, encoded = worldtop_encoder(value)
                except_text = code('Element ') + log_time(stamp, code, form='normal')
                if tops.get(stamp) is None:
                    tops[stamp] = encoded
                else:
                    for castle in tops[stamp]:
                        if tops[stamp][castle] < encoded[castle]:
                            tops[stamp] = encoded
                            break
            if array[value] > 1:
                text = '\nRepeating in base ' + str(array[value]) + ' times.\nPosition '
                Auth.send_dev_message(except_text + code(text + str(indexer.index(value)) + ' in table.'), tag=None)
    return battle_sheet, battles, battle_values, top_sheet, tops, top_values


first_cw_battle_stamp = 1527516000  # (28.05.2018 17:00, GMT+3) Самая первая битва в ChatWars 3
battle_standard_stamp = 1606831200  # (01.12.2020 17:00, GMT+3) Начало сезона, после этой даты собираем /worldtop
worksheet, google_dict, google_values, top_worksheet, top_dict, google_top_values = creation_google_values()
bot = Auth.start_main_bot('async')
dispatcher = Dispatcher(bot)
# ====================================================================================
start_message = Auth.start_message(stamp1)


def former(text):
    response = 'False'
    soup = BeautifulSoup(text, 'html.parser')
    is_post_not_exist = soup.find('div', class_='tgme_widget_message_error')
    if is_post_not_exist is None:
        post_raw = str(soup.find('div', class_='tgme_widget_message_text js-message_text')).replace('<br/>', '\n')
        get_au_id = soup.find('div', class_='tgme_widget_message_link')
        if get_au_id:
            au_id = re.sub('t.me/.*?/', '', get_au_id.get_text())
            post = BeautifulSoup(post_raw, 'html.parser').get_text()
            response = au_id + '/' + re.sub('/', '&#47;', post).replace('\n', '/')
    return response


def battle_to_google():
    from timer import timer
    global worksheet, google_dict, last_post_id, google_values
    value = re.sub(r'\D', '', google_values[-1].split('/')[0])
    if len(value) > 0:
        last_post_id = int(value) + 1
        false_barrier = 0
        while True:
            try:
                if checker_blocking is None:
                    print_text = main_address + str(last_post_id)
                    battle = former(requests.get(print_text + '?embed=1').text)
                    battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', battle)
                    if battle_search:
                        if battle not in google_values:
                            row = str(len(google_values) + 1)
                            try:
                                battle_range = worksheet.range('A' + row + ':A' + row)
                                battle_range[0].value = battle
                                worksheet.update_cells(battle_range)
                            except IndexError and Exception:
                                worksheet = gspread.service_account('1.json').open('Digest').worksheet('main')
                                battle_range = worksheet.range('A' + row + ':A' + row)
                                battle_range[0].value = battle
                                worksheet.update_cells(battle_range)
                            objects.printer(print_text + ' Добавил битву в таблицу')
                            google_dict[timer(battle_search)] = re.sub('️', '', battle)
                            google_values.append(battle)
                            last_post_id += 1
                            sleep(1.2)
                        else:
                            objects.printer(print_text + ' Битва уже была в таблице')
                            last_post_id += 1
                    elif battle == 'False':
                        if false_barrier < 4:
                            false_barrier += 1
                            last_post_id += 1
                            sleep(1)
                        else:
                            objects.printer(print_text + ' Постов нет вместе с false_barrier, ищем заново')
                            last_post_id -= false_barrier
                            false_barrier = 0
                            sleep(3)
                    else:
                        last_post_id += 1  # Это не битва, пропускаем
                else:
                    sleep(20)
            except IndexError and Exception:
                Auth.thread_exec()
    else:
        Auth.send_json(None, 'war_google', 'Не найдено нормальное значение last_post_id, тред не может быть начат')


def battle_in_google_checker():
    from timer import timer
    from copy import deepcopy
    global worksheet, google_dict, google_values, checker_blocking
    while last_post_id is None:
        pass
    if last_post_id:
        check_id = deepcopy(last_post_id)
    else:
        check_id = 0
    false_barrier = 0
    while True:
        try:
            print_text = main_address + str(check_id)
            battle = former(requests.get(print_text + '?embed=1').text)
            battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', battle)
            if battle_search:
                print_text += ' Проверил'
                if battle not in google_values:
                    checker_blocking = True
                    sleep(10)
                    row = str(len(google_values) + 1)
                    worksheet = gspread.service_account('1.json').open('Digest').worksheet('main')
                    battle_range = worksheet.range('A' + row + ':A' + row)
                    battle_range[0].value = battle
                    worksheet.update_cells(battle_range)
                    google_dict[timer(battle_search)] = re.sub('️', '', battle)
                    google_values.append(battle)
                    sleep(10)
                    checker_blocking = None
                    print_text += ', добавил в таблицу пропавшую битву'
                objects.printer(print_text)
                check_id -= 1
            elif battle == 'False':
                if false_barrier < 4:
                    false_barrier += 1
                    check_id -= 1
                    sleep(1)
                else:
                    objects.printer(print_text + ' Постов нет вместе с false_barrier, ищем заново')
                    if check_id <= 4:
                        objects.printer('Проверка завершена успешно')
                        _thread.exit()
                    check_id -= false_barrier
                    false_barrier = 0
                    sleep(3)
            else:
                check_id -= 1   # Это не битва, пропускаем
            sleep(2)
        except IndexError and Exception:
            Auth.thread_exec()


def world_top_sorted(date_start, date_end, sorting='trophy'):
    castle_db = {}
    for castle in [c for c in castle_dict]:
        castle_db[castle] = {}
        castle_db[castle]['🔱'] = 0
        castle_db[castle]['box'] = 0
        castle_db[castle]['money'] = 0
        castle_db[castle]['trophy'] = 0
        castle_db[castle]['addition'] = 0
        for position in range(1, 8):
            castle_db[castle][position] = 0
        for pattern in battle_patterns:
            castle_db[castle][battle_patterns.get(pattern)] = 0
    for battle_date in sorted(google_dict):
        trophy_search = re.search('По итогам сражений замкам начислено:/(.*)', google_dict[battle_date])
        if date_start <= battle_date <= date_end:
            battle_top_dict = top_dict.get(battle_date)
            if trophy_search:
                trophy = re.split('/', trophy_search.group(1))
                for i in trophy:
                    search = re.search(castle_search + r'.+ \+(\d+) 🏆 очков', i)
                    if search:
                        castle_db[search.group(1)]['trophy'] += int(search.group(2))
            for string in re.split('//', google_dict[battle_date]):
                search = re.search(castle_search, string)
                box_search = re.search('.*потеряно (.*?) складских ячеек', string)
                money_search = re.search('.*(на|отобрали) (.*?) золотых монет', string)
                if search:
                    for pattern in battle_patterns:
                        if pattern in string:
                            castle_db[search.group(1)][battle_patterns.get(pattern)] += 1
                            break
                        elif '🔱' in string:
                            castle_db[search.group(1)]['🔱'] += 1
                            break
                    if box_search:
                        castle_db[search.group(1)]['box'] -= int(box_search.group(1))
                    if money_search:
                        sign = '+'
                        if money_search.group(1) == 'на':
                            sign = '-'
                        castle_db[search.group(1)]['money'] += int(sign + money_search.group(2))
            if battle_top_dict:
                for castle in battle_top_dict:
                    trophy_from_top = battle_top_dict[castle]
                    trophy_from_battle = castle_db[castle]['trophy']
                    if trophy_from_top > trophy_from_battle:
                        castle_db[castle]['trophy'] = trophy_from_top
                        castle_db[castle]['addition'] += trophy_from_top - trophy_from_battle
            castle_temp = [i[0] for i in sorted(castle_db.items(), key=lambda x: x[1]['trophy'], reverse=True)]
            for i in castle_temp:
                castle_db[i][castle_temp.index(i) + 1] += 1
    return sorted(castle_db.items(), key=lambda x: x[1][sorting], reverse=True)


def text_header(date_start, date_end, text, time_in_brackets=False):
    brackets = ['', '']
    if time_in_brackets:
        brackets = ['&#40;', '&#41;']
    time_frame = [log_time(value, gmt=3, form='au_normal') for value in [date_start, date_end]]
    return bold(text) + '\n' + brackets[0] + code(' - '.join(time_frame)) + brackets[1] + '\n'


def summary(date_start, date_end, period='период'):
    text, postscript = '', ''
    castle_list = world_top_sorted(date_start, date_end, 'money')
    battle_date_start = last_battle_date = battle_date_end = first_cw_battle_stamp
    if date_start < first_cw_battle_stamp:
        first_cw_battle = log_time(first_cw_battle_stamp, gmt=3, form='au_normal')
        postscript += '\nБитв раньше ' + first_cw_battle + ' быть не может'
        date_start = first_cw_battle_stamp

    while battle_date_start < date_start:
        battle_date_start += eight_hours

    while last_battle_date <= objects.time_now():
        last_battle_date += eight_hours
    last_battle_date -= eight_hours

    while battle_date_end <= date_end:
        battle_date_end += eight_hours
    battle_date_end -= eight_hours

    if battle_date_end > last_battle_date:
        last_cw_battle = log_time(last_battle_date, gmt=3, form='au_normal')
        postscript += '\nБитв после ' + last_cw_battle + ' еще не произошло'
        battle_date_end = last_battle_date

    battle_range = range(battle_date_start, battle_date_end + 1, eight_hours)
    text = text_header(battle_date_start, battle_date_end, 'Отчет за ' + period, True)
    missed_battles = [log_time(date, gmt=3, form='au_normal') for date in battle_range if date not in google_dict]
    if missed_battles:
        postscript += '\nЕсть неучтённые битвы (отсутствуют в базе, а может и вообще):\n' + ', '.join(missed_battles)

    for castle in castle_list:
        fence = ''
        text += castle[0] + ': '
        castle_stats = dict(castle[1])
        for array in [['money', '💰 '], ['box', '📦 '], ['trophy', '🏆 \n']]:
            main = array[0]
            if castle_stats[main] >= 0 and main != 'box':
                text += '+' + str(castle_stats[main]) + array[1]
            elif castle_stats[main] < 0:
                text += str(castle_stats[main]) + array[1]
        for emoji in ['⚔', '⚔😎', '⚔⚡', '🛡', '🛡⚡', '🔱']:
            if castle_stats.get(emoji) > 0:
                text += code(fence + emoji + ':' + str(castle_stats.get(emoji)))
                if fence == '':
                    fence = '|'
        if fence:
            text += '\n'
    if postscript and period == 'период':
        remain_len = 4096 - len(re.sub('<.*?>', '', text))
        text += code(postscript[:remain_len])
    return text


def true_world_top(date_start, date_end):
    text = '🏅|'
    max_len_position = 2
    castle_list = world_top_sorted(date_start, date_end)
    title = text_header(date_start, date_end, 'Ротация замков в /worldtop')
    for castle in castle_list:
        castle_stats = dict(castle[1])
        for castle_param in castle_stats:
            if castle_param != 'trophy':
                len_position = len(str(castle_stats[castle_param]))
                if len_position > max_len_position:
                    max_len_position = len_position
    for i in range(1, 8):
        text += ' ' * (max_len_position - 2) + str(i) + 'м|'
    text += '🏆\n'
    for castle in castle_list:
        text += castle[0] + '|'
        castle_stats = dict(castle[1])
        for castle_param in castle_stats:
            if castle_param != 'trophy':
                amount = str(castle_stats[castle_param])
                text += ' ' * (max_len_position - len(amount)) + amount + '|'
        text += str(castle_stats['trophy']) + ' \n'
    return title + code(text)


def average_top(date_start, date_end):
    castles_by_average = {}
    castle_list = world_top_sorted(date_start, date_end)
    text = text_header(date_start, date_end, 'Среднее место за сезон')
    for castle in castle_list:
        places_summary = 0
        numbers_battle = 0
        castle_name = castle[0]
        castle_stats = dict(castle[1])
        for castle_param in castle_stats:
            if type(castle_param) == int:
                places_summary += castle_param * castle_stats[castle_param]
                numbers_battle += castle_stats[castle_param]
        average = round(places_summary / numbers_battle, 2)
        castles_by_average[castle_name + castle_dict[castle_name]] = average
    castle_list = sorted(castles_by_average.items(), key=lambda x: x[1])
    for castle in castle_list:
        place = str(castle_list.index(castle) + 1)
        text += '# ' + place + ' ' + castle[0] + ' ' + bold(castle[1]) + '\n'
    return text


def cw_world_top(date_start, date_end):
    text = '🏅'
    share_link = 'https://t.me/share/url?url=/worldtop'
    castle_list = world_top_sorted(date_start, date_end)
    for place in range(1, len(castle_list) + 1):
        addition = ''
        castle = castle_list[place - 1][0]
        castle_stats = dict(castle_list[place - 1][1])
        if place != 1:
            text += ' ' * 5
        if castle_stats['addition'] > 0:
            addition = code('+' + str(castle_stats['addition']))
        text += '# ' + str(place) + ' ' + castle + castle_dict.get(castle)
        text += ' ' + bold(castle_stats['trophy']) + addition + ' 🏆 очков\n'
    return text + code('Для обновления: ') + objects.html_link(share_link, '/worldtop')


async def seasoned(message):
    text = 'ERROR'
    commands = await bot.get_my_commands()
    if message['text'].lower().startswith('/season'):
        command_function = true_world_top
    elif message['text'].lower().startswith('/average'):
        command_function = average_top
    elif message['text'].lower().startswith('/worldtop'):
        command_function = cw_world_top
    else:
        command_function = summary
    for command in commands:
        if command['command'] == 'season':
            search = re.search('(.*?)—(.*)', command['description'])
            if search:
                starting = stamper(search.group(1), '%d/%m/%Y %H:%M') - 3 * 60 * 60
                ending = stamper(search.group(2), '%d/%m/%Y %H:%M') - 3 * 60 * 60
                if starting and ending:
                    text = command_function(starting, ending)
                    break
    await bot.send_message(message['chat']['id'], text, parse_mode='HTML')


@dispatcher.message_handler()
async def repeat_all_messages(message: types.Message):
    global top_dict, top_worksheet, async_blocking, google_top_values
    try:
        text = 'ERROR'
        if message['text'].lower() in ['/season', '/average', '/worldtop']:
            await seasoned(message)

        elif message['text'].lower().startswith(tuple(standard_command_list)):
            bot_username = Auth.get_me.get('username').lower()
            command_list = [command + '@' + bot_username for command in standard_command_list]
            if message['text'].lower() in command_list:
                await seasoned(message)
            else:
                modified = re.sub('/(summary|place|season|average|worldtop) ', '', message['text'].lower(), 1)
                modified = re.sub(r'[./\\]+', '.', modified)
                modified = re.sub('\'', '&#39;', modified)
                modified = re.sub('[—-]+', '-', modified)
                modified = objects.html_secure(modified)
                modified = re.sub(r'\.+', '.', modified)
                modified = re.sub('\n+', '\n', modified)
                modified = re.sub(' +', ' ', modified)
                modified = re.sub('\n', '', modified)

                search = re.search('(.*?)-(.*)', modified)
                if message['text'].lower().startswith('/season'):
                    command_function = true_world_top
                elif message['text'].lower().startswith('/average'):
                    command_function = average_top
                elif message['text'].lower().startswith('/worldtop'):
                    command_function = cw_world_top
                else:
                    command_function = summary

                if search:
                    starting = stamper(search.group(1), '%d.%m.%Y %H:%M') - 3 * 60 * 60
                    ending = stamper(search.group(2), '%d.%m.%Y %H:%M') - 3 * 60 * 60
                    if starting and ending:
                        text = command_function(starting, ending)
                await bot.send_message(message['chat']['id'], text, parse_mode='HTML')

        elif message['forward_from']:
            send_reply = True
            if message['chat']['id'] < 0:
                send_reply = False
            battle_stamp = battle_standard_stamp
            if message['forward_from']['username'] == 'ChatWarsBot':
                if message['text'].startswith('🏅'):
                    if dict(message).get('forward_date') > battle_stamp:
                        while battle_stamp < dict(message).get('forward_date'):
                            battle_stamp += eight_hours
                        battle_stamp -= eight_hours
                        top_text = str(battle_stamp) + '/' + re.sub('\n', '/', message['text'])
                        text = bold('Битва') + ' за ' + log_time(battle_stamp, gmt=3, tag=code, form=True) + '\n'
                        if top_text not in google_top_values:
                            while async_blocking is True:
                                await asyncio.sleep(0.1)

                            async_blocking = True
                            text += 'Добавлена в базу'
                            row = str(len(google_top_values) + 1)
                            battle_stamp, encoded = worldtop_encoder(top_text)
                            try:
                                top_range = top_worksheet.range('A' + row + ':A' + row)
                                top_range[0].value = top_text
                                top_worksheet.update_cells(top_range)
                            except IndexError and Exception:
                                top_worksheet = gspread.service_account('2.json').open('Digest').worksheet('main')
                                top_range = worksheet.range('A' + row + ':A' + row)
                                top_range[0].value = top_text
                                top_worksheet.update_cells(top_range)
                            google_top_values.append(top_text)
                            if top_dict.get(battle_stamp) is None:
                                top_dict[battle_stamp] = encoded
                            else:
                                for castle in top_dict[battle_stamp]:
                                    if top_dict[battle_stamp][castle] < encoded[castle]:
                                        top_dict[battle_stamp] = encoded
                                        break
                            text += bold(' успешно.')
                            await asyncio.sleep(2)
                            async_blocking = None
                        else:
                            text += bold('Уже находится в базе') + ', но спасибо 😀.'
                    else:
                        text = bold('Древние') + ' битвы обходились без нужды в ' + bold('WORLDTOP') + \
                               ', так что не стоит, спасибо 😀.'
                else:
                    link = objects.html_link('https://t.me/share/url?url=/worldtop', '/worldtop')
                    text = 'Это не очень похоже на ' + bold('WORLDTOP') + ' из CW.\n'
                    text += 'Пожалуйста, отправь в CW ' + bold(link) + ' (жми) и потом форварди сюда.'
            else:
                text = 'Это не от CW форвард, ' + bold('дурень.')

            if send_reply:
                await bot.send_message(message['chat']['id'], text, parse_mode='HTML',
                                       reply_to_message_id=message['message_id'])

        elif message['chat']['id'] == idMe:
            if message.text.startswith('/log'):
                await bot.send_document(message['chat']['id'], open('log.txt', 'r'))

    except IndexError and Exception:
        await Auth.async_exec(str(message))


async def changing_season_start_description():
    from datetime import datetime
    while True:
        try:
            stamp = objects.time_now()
            minute = int(datetime.utcfromtimestamp(stamp).strftime('%M'))
            day = int(datetime.utcfromtimestamp(stamp + 3 * 60 * 60).strftime('%d'))
            hour = int(datetime.utcfromtimestamp(stamp + 3 * 60 * 60).strftime('%H'))
            month = int(datetime.utcfromtimestamp(stamp + 3 * 60 * 60).strftime('%m'))
            if hour == 17 and day == 1 and month in [3, 6, 9, 12]:
                commands = await bot.get_my_commands()
                for command in commands:
                    if command['command'] == 'season':
                        desc = log_time(stamp - minute * 60, gmt=3, form='b_channel')
                        command['description'] = desc + '—' + desc
                        await bot.set_my_commands(commands)
                        objects.printer('Изменено описание команды /season на ' + desc + '—' + desc)
                        await Auth.edit_dev_message(start_message, '#new_season ' + code(desc))
                await asyncio.sleep(3600)
            await asyncio.sleep(1)
        except IndexError and Exception:
            await Auth.async_exec()


async def changing_season_description():
    from timer import timer
    while True:
        try:
            commands = await bot.get_my_commands()
            for command in commands:
                if command['command'] == 'season':
                    last_battle_stamp = 0
                    search = re.search('(.*?)—(.*?)', command['description'])
                    for battle in google_values:
                        time_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', battle)
                        if time_search:
                            stamp = timer(time_search)
                            if last_battle_stamp < stamp:
                                last_battle_stamp = stamp
                    if search:
                        desc = search.group(1) + '—' + log_time(last_battle_stamp, gmt=3, form='b_channel')
                        if command['description'] != desc:
                            command['description'] = desc
                            await bot.set_my_commands(commands)
                            objects.printer('Изменено описание команды /season на ' + desc)
            await asyncio.sleep(10)
        except IndexError and Exception:
            await Auth.async_exec()


if __name__ == '__main__':
    gain = [battle_to_google, battle_in_google_checker]
    async_gain = [changing_season_description, changing_season_start_description]
    for thread_element in gain:
        _thread.start_new_thread(thread_element, ())
    for thread_element in async_gain:
        dispatcher.loop.create_task(thread_element())
    executor.start_polling(dispatcher)
