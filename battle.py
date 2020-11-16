# -*- coding: utf-8 -*-
import os
import re
import objects
import _thread
import gspread
import requests
from time import sleep
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
from objects import code, stamper, log_time

stamp1 = objects.time_now()
objects.environmental_files(python=True)
Auth = objects.AuthCentre(os.environ['TOKEN'], dev_chat_id=396978030)
# ====================================================================================
e_trident = '🔱'
idMe = 396978030
last_post_id = None
checker_blocking = None
castle = '(🖤|🍆|🐢|🌹|🍁|☘|🦇)'
main_address = 'https://t.me/ChatWarsDigest/'
castle_list = ['🖤', '🍆', '🐢', '🌹', '🍁', '☘', '🦇']
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
    sheet = gspread.service_account('1.json').open('Digest').worksheet('main2')
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


executive = Auth.thread_exec
bot = Auth.start_main_bot('non-async')
worksheet, google_values = creation_google_values()
# ====================================================================================
Auth.start_message(stamp1)


def spacer(col):
    space = ''
    for j in range(col):
        space += ' '
    return space


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
                                worksheet = gspread.service_account('1.json').open('Digest').worksheet('main2')
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
                executive()
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
                    worksheet = gspread.service_account('1.json').open('Digest').worksheet('main2')
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
            executive()


def summary(time_start, time_end):
    from timer import timer
    castle_db = {}
    for i in castle_list:
        castle_db[i] = defaultdict(dict)
        castle_db[i]['money'] = 0
        castle_db[i]['box'] = 0
        castle_db[i]['trophy'] = 0
        castle_db[i]['🔱'] = 0
        for mini in character:
            castle_db[i][character.get(mini)] = 0
    for battle in google:
        trophy_search = re.search('По итогам сражений замкам начислено:/(.*)', battle)
        time_search = re.search(r'(\d{2}) (.*) 10(..).*Результаты сражений:', battle)
        soup = re.sub('.*Результаты сражений:/', '', battle)
        soup = re.sub('//По итогам сражений замкам начислено:.+', '', soup)
        splited = re.split('//', soup)
        if time_search:
            date = timer(time_search) + 3 * 60 * 60
            if time_start <= date <= time_end:
                if trophy_search:
                    trophy = re.split('/', trophy_search.group(1))
                    for i in trophy:
                        search = re.search(castle + r'.+ \+(\d+) 🏆 очков', i)
                        if search:
                            castle_db[search.group(1)]['trophy'] += int(search.group(2))
                for string in splited:
                    search = re.search(castle, string)
                    if search:
                        for m in character:
                            if m in string:
                                mini = character.get(m)
                                if e_trident in string:
                                    mini = e_trident
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
    for i in listed:
        castle_temp.append(i[0])
    text = ''
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


def world_top(time_start, time_end):
    from timer import timer
    castle_db = {}
    for i in castle_list:
        castle_db[i] = defaultdict(dict)
        castle_db[i]['trophy'] = 0
        for pos in range(1, 8):
            castle_db[i][pos] = 0
    for battle in reversed(google):
        trophy_search = re.search('По итогам сражений замкам начислено:/(.*)', battle)
        time_search = re.search(r'(\d{2}) (.*) 10(..).*Результаты сражений:', battle)
        if time_search:
            date = timer(time_search) + 3 * 60 * 60
            if time_start <= date <= time_end:
                if trophy_search:
                    trophy = re.split('/', trophy_search.group(1))
                    for i in trophy:
                        search = re.search(castle + r'.+ \+(\d+) 🏆 очков', i)
                        if search:
                            castle_db[search.group(1)]['trophy'] += int(search.group(2))
                castle_temp = []
                listed = list(castle_db.items())
                listed.sort(key=lambda arr: arr[1]['trophy'])
                for i in listed:
                    castle_temp.append(i[0])
                castle_temp.reverse()
                for i in castle_temp:
                    castle_db[i][castle_temp.index(i) + 1] += 1
    max_len_pos = 0
    castle_temp = []
    listed = list(castle_db.items())
    listed.sort(key=lambda arr: arr[1]['trophy'])
    for i in listed:
        array = castle_db.get(i[0])
        castle_temp.append(i[0])
        for pos in range(1, 8):
            amount = str(array[pos])
            if len(amount) > max_len_pos:
                max_len_pos = len(amount)
    text = '🏅|'
    for i in range(1, 8):
        text += spacer(max_len_pos - 2) + str(i) + 'м|'
    text += '🏆\n'
    for i in reversed(castle_temp):
        array = castle_db.get(i)
        text += i + '|'
        for pos in range(1, 8):
            amount = str(array[pos])
            text += spacer(max_len_pos - len(amount)) + amount + '|'
        if array['trophy'] >= 0:
            text += str(array['trophy']) + ' \n'
    return code(text)


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    try:
        if message.text.startswith('/summary'):
            modified = re.sub('/summary ', '', message.text)
            search = re.search('(.*?)-(.*?)\n(.*)', modified)
            if search:
                starting = stamper(search.group(1), '%d.%m.%Y %H:%M:%S')
                ending = stamper(search.group(2), '%d.%m.%Y %H:%M:%S')
                text = search.group(3)
                if str(starting) != 'False' and str(ending) != 'False':
                    text += '\n(' + log_time(starting - 3 * 60 * 60, code) + code(' - ')
                    text += log_time(ending - 3 * 60 * 60, code) + ')\n' + summary(starting, ending)
                bot.send_message(message.chat.id, text, parse_mode='HTML')

        elif message.text.startswith('/place'):
            modified = re.sub('/place ', '', message.text)
            search = re.search('(.+?)-(.+)', modified)
            if search:
                text = '<b>Ротация замков в worldtop\'е</b>'
                starting = stamper(search.group(1), '%d.%m.%Y %H:%M:%S')
                ending = stamper(search.group(2), '%d.%m.%Y %H:%M:%S')
                if str(starting) != 'False' and str(ending) != 'False':
                    text += '\n' + log_time(starting - 3 * 60 * 60, code) + code(' - ')
                    text += log_time(ending - 3 * 60 * 60, code) + '\n' + world_top(starting, ending)
                bot.send_message(message.chat.id, text, parse_mode='HTML')

        elif message.chat.id == idMe:
            if message.text.startswith('/base'):
                doc = open('log.txt', 'rt')
                bot.send_document(idMe, doc)
                doc.close()
            else:
                bot.send_message(message.chat.id, 'Я работаю')
    except IndexError and Exception:
        executive(str(message))


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60)
    except IndexError and Exception:
        bot.stop_polling()
        sleep(1)
        telegram_polling()


if __name__ == '__main__':
    gain = [battle_to_google, battle_in_google_checker]
    for thread_element in gain:
        _thread.start_new_thread(thread_element, ())
    telegram_polling()
