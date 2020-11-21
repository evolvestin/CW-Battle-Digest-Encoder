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
checker_blocking = None
share_link = 'https://t.me/share/url?url='
main_address = 'https://t.me/ChatWarsDigest/'
castle_dict = {'🖤': 'Скала', '🍆': 'Ферма', '🐢': 'Тортуга',
               '🌹': 'Замок Рассвета', '🍁': 'Амбер', '☘': 'Оплот', '🦇': 'Ночной Замок'}
castle_search = '(' + '|'.join(castle_dict) + ')'
character = {
    'со значительным преимуществом': '⚔😎',
    'успешно атаковали защитников': '⚔',
    'разыгралась настоящая бойня, но все-таки силы атакующих были ': '⚔⚡',
    'успешно отбились от': '🛡',
    'легко отбились от': '🛡👌',
    'героически отразили ': '🛡⚡',
    'скучали, на них ': '🛡😴',
}


def creation_google_values():
    sheet = gspread.service_account('1.json').open('Digest').worksheet('main')
    raw_values = sheet.col_values(1)
    values = []
    counter_values = Counter(raw_values)
    for value in counter_values:
        values.append(re.sub('️', '', value))
        if counter_values[value] > 1:
            post_id = str(value.split('/')[0])
            text = '\nПовторяется в базе ' + str(counter_values[value]) + \
                ' раз(а).\nНа данный момент он находится на позиции ' + str(raw_values.index(value)) + ' в таблице.'
            text = code('Элемент с id:') + objects.html_link(main_address + post_id, post_id) + code(text)
            Auth.send_dev_message(text, tag=None)
    return sheet, values


worksheet, google_values = creation_google_values()
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
    global worksheet, last_post_id, google_values
    value = re.sub(r'\D', '', google_values[-1].split('/')[0])
    if len(value) > 0:
        last_post_id = int(value) + 1
        false_barrier = 0
        while True:
            try:
                if checker_blocking is None:
                    print_text = main_address + str(last_post_id)
                    text = former(requests.get(print_text + '?embed=1').text)
                    battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', text)
                    if battle_search:
                        if re.sub('️', '', text) not in google_values:
                            row = str(len(google_values) + 1)
                            try:
                                battle_range = worksheet.range('A' + row + ':A' + row)
                                battle_range[0].value = text
                                worksheet.update_cells(battle_range)
                            except IndexError and Exception:
                                worksheet = gspread.service_account('1.json').open('Digest').worksheet('main')
                                battle_range = worksheet.range('A' + row + ':A' + row)
                                battle_range[0].value = text
                                worksheet.update_cells(battle_range)
                            google_values.append(re.sub('️', '', text))
                            objects.printer(print_text + ' Добавил битву в таблицу')
                            last_post_id += 1
                            sleep(1.2)
                        else:
                            objects.printer(print_text + ' Битва уже была в таблице')
                            last_post_id += 1
                    elif text == 'False':
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
    from copy import deepcopy
    global worksheet, checker_blocking
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
            text = former(requests.get(print_text + '?embed=1').text)
            battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', text)
            if battle_search:
                print_text += ' Проверил'
                if re.sub('️', '', text) not in google_values:
                    checker_blocking = True
                    sleep(10)
                    row = str(len(google_values) + 1)
                    worksheet = gspread.service_account('1.json').open('Digest').worksheet('main')
                    battle_range = worksheet.range('A' + row + ':A' + row)
                    battle_range[0].value = text
                    worksheet.update_cells(battle_range)
                    sleep(10)
                    checker_blocking = None
                    print_text += ', добавил в таблицу пропавшую битву'
                objects.printer(print_text)
                check_id -= 1
            elif text == 'False':
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


def summary(date_start, date_end, text):
    from timer import timer
    castle_db = {}
    for i in [c for c in castle_dict]:
        castle_db[i] = {}
        castle_db[i]['money'] = 0
        castle_db[i]['box'] = 0
        castle_db[i]['trophy'] = 0
        castle_db[i]['🔱'] = 0
        for mini in character:
            castle_db[i][character.get(mini)] = 0
    for battle in google_values:
        trophy_search = re.search('По итогам сражений замкам начислено:/(.*)', battle)
        time_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', battle)
        soup = re.sub('.*Результаты сражений:/', '', battle)
        soup = re.sub('//По итогам сражений замкам начислено:.+', '', soup)
        split = re.split('//', soup)
        if time_search:
            date = timer(time_search) + 3 * 60 * 60
            if date_start <= date <= date_end:
                if trophy_search:
                    trophy = re.split('/', trophy_search.group(1))
                    for i in trophy:
                        search = re.search(castle_search + r'.+ \+(\d+) 🏆 очков', i)
                        if search:
                            castle_db[search.group(1)]['trophy'] += int(search.group(2))
                for string in split:
                    search = re.search(castle_search, string)
                    if search:
                        for m in character:
                            if m in string:
                                mini = character.get(m)
                                if '🔱' in string:
                                    mini = '🔱'
                                castle_db[search.group(1)][mini] += 1
                                break

                        money_search = re.search('.*(на|отобрали) (.*?) золотых монет', string)
                        if money_search:
                            if money_search.group(1) == 'на':
                                sign = '-'
                            else:
                                sign = '+'
                            castle_db[search.group(1)]['money'] += int(sign + money_search.group(2))

                        box_search = re.search('.*потеряно (.*?) складских ячеек', string)
                        if box_search:
                            castle_db[search.group(1)]['box'] += int(box_search.group(1))
    castle_temp = []
    listed = list(castle_db.items())
    listed.sort(key=lambda arr: arr[1]['money'])
    text = text_header(date_start, date_end, text, True)
    for i in listed:
        castle_temp.append(i[0])
    for i in reversed(castle_temp):
        array = castle_db.get(i)
        text += i + ': '
        if array['money'] >= 0:
            text += '+' + str(array['money']) + '💰 '
        else:
            text += str(array['money']) + '💰 '
        if array['box'] > 0:
            text += '+' + str(array['box']) + '📦 '
        elif array['box'] < 0:
            text += str(array['box']) + '📦 '
        if array['trophy'] >= 0:
            text += '+' + str(array['trophy']) + '🏆 \n'
        text += code('⚔:' + str(array['⚔']))
        if array['⚔😎'] > 0:
            text += code('|⚔😎:' + str(array['⚔😎']))
        if array['⚔⚡'] > 0:
            text += code('|⚔⚡:' + str(array['⚔⚡']))
        if array['🛡'] > 0:
            text += code('|🛡:' + str(array['🛡']))
        if array['🛡⚡'] > 0:
            text += code('|🛡⚡:' + str(array['🛡⚡']))
        if array['🔱'] > 0:
            text += code('|🔱:' + str(array['🔱']))
        text += '\n'
    return text


def world_top_sorted(date_start, date_end):
    from timer import timer
    castle_db = {}
    for i in [c for c in castle_dict]:
        castle_db[i] = {}
        castle_db[i]['trophy'] = 0
        for pos in range(1, 8):
            castle_db[i][pos] = 0
    for battle in google_values:
        trophy_search = re.search('По итогам сражений замкам начислено:/(.*)', battle)
        battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', battle)
        if battle_search:
            if date_start <= (timer(battle_search) + 3 * 60 * 60) <= date_end:
                if trophy_search:
                    trophy = re.split('/', trophy_search.group(1))
                    for i in trophy:
                        search = re.search(castle_search + r'.+ \+(\d+) 🏆 очков', i)
                        if search:
                            castle_db[search.group(1)]['trophy'] += int(search.group(2))
                castle_temp = [i[0] for i in sorted(castle_db.items(), key=lambda x: x[1]['trophy'], reverse=True)]
                for i in castle_temp:
                    castle_db[i][castle_temp.index(i) + 1] += 1
    return sorted(castle_db.items(), key=lambda x: x[1]['trophy'], reverse=True)


def text_header(date_start, date_end, text, time_in_brackets=False):
    brackets = ['', '']
    if time_in_brackets:
        brackets = ['&#40;', '&#41;']
    text = bold(text) + '\n' + brackets[0] + log_time(date_start, code, gmt=0, form='au_normal') + code(' - ')
    return text + log_time(date_end, code, gmt=0, form='au_normal') + brackets[1] + '\n'


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
    castle_list = world_top_sorted(date_start, date_end)
    text = text_header(date_start, date_end, 'Среднее место за сезон')
    for castle in castle_list:
        places_summary = 0
        numbers_battle = 0
        castle_stats = dict(castle[1])
        for castle_param in castle_stats:
            if type(castle_param) == int:
                places_summary += castle_param * castle_stats[castle_param]
                numbers_battle += castle_stats[castle_param]
        average = round(places_summary / numbers_battle, 2)
        place = castle_list.index(castle) + 1
        text += '# ' + str(place) + ' ' + castle[0] + castle_dict[castle[0]] + ' ' + bold(average) + '\n'
    return text


def cw_world_top(date_start, date_end):
    text = '🏅'
    castle_list = world_top_sorted(date_start, date_end)
    for i in range(1, len(castle_list) + 1):
        if i != 1:
            text += ' ' * 5
        castle = castle_list[i - 1][0]
        castle_stats = dict(castle_list[i - 1][1])
        text += '# ' + str(i) + ' ' + castle + castle_dict.get(castle) + ' '
        text += bold(castle_stats['trophy']) + ' 🏆 очков\n'
    text += code('Если нашли ошибку: ') + '@evolvestin'
    return text


@dispatcher.message_handler()
async def repeat_all_messages(message: types.Message):
    try:
        text = 'ERROR'
        if message['text'].lower() in ['/season', '/average', '/worldtop']:
            commands = await bot.get_my_commands()
            if message['text'].lower().startswith('/season'):
                command_function = true_world_top
            elif message['text'].lower().startswith('/worldtop'):
                command_function = cw_world_top
            else:
                command_function = average_top
            for command in commands:
                if command['command'] == 'season':
                    search = re.search('(.*?)—(.*)', command['description'])
                    if search:
                        starting = stamper(search.group(1), '%d/%m/%Y %H:%M')
                        ending = stamper(search.group(2), '%d/%m/%Y %H:%M')
                        if starting and ending:
                            text = command_function(starting, ending)
                            break
            await bot.send_message(message['chat']['id'], text, parse_mode='HTML')

        elif message['text'].lower().startswith(('/summary', '/place', '/season', '/average', '/worldtop')):
            modified = re.sub('/(summary|place|season|average|worldtop) ', '', message['text'].lower(), 1)
            modified = re.sub(r'[./\\]+', '.', modified)
            modified = re.sub('\'', '&#39;', modified)
            modified = re.sub('[—-]+', '-', modified)
            modified = objects.html_secure(modified)
            modified = re.sub(r'\.+', '.', modified)
            modified = re.sub('\n+', '\n', modified)
            modified = re.sub(' +', ' ', modified)
            if message['text'].lower().startswith('/summary'):
                search_fraze = '(.*?)-(.*?)\n(.*)'
                command_function = summary
            else:
                modified = re.sub('\n', '', modified)
                command_function = true_world_top
                search_fraze = '(.*?)-(.*)'

            if message['text'].lower().startswith('/average'):
                command_function = average_top
            elif message['text'].lower().startswith('/worldtop'):
                command_function = cw_world_top

            search = re.search(search_fraze, modified)
            if search:
                starting = stamper(search.group(1), '%d.%m.%Y %H:%M')
                ending = stamper(search.group(2), '%d.%m.%Y %H:%M')
                if starting and ending:
                    if message['text'].lower().startswith('/summary'):
                        text = command_function(starting, ending, search.group(3))
                    else:
                        text = command_function(starting, ending)
            await bot.send_message(message['chat']['id'], text, parse_mode='HTML')

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
                        desc = log_time(stamp - minute * 60, form='b_channel')
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
                        desc = search.group(1) + '—' + log_time(last_battle_stamp, form='b_channel')
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
