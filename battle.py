# -*- coding: utf-8 -*-
import os
import re
import objects
import _thread
import gspread
import requests
from time import sleep
from bs4 import BeautifulSoup
from collections import defaultdict
from objects import code, stamper, log_time

stamp1 = objects.time_now()
objects.environmental_files(python=True)
# ====================================================================================
data1 = gspread.service_account('1.json').open('Digest').worksheet('main2')
data2 = gspread.service_account('2.json').open('Digest').worksheet('main2')
google = data1.col_values(1)

e_trident = '🔱'
idMe = 396978030
bitva_id = int(google[0])
checker = int(google[0]) - 1
ignore = google[1].split('/')
castle = '(🖤|🍆|🐢|🌹|🍁|☘️|🦇)'
main_address = 'https://t.me/ChatWarsDigest/'
castle_list = ['🖤', '🍆', '🐢', '🌹', '🍁', '☘️', '🦇']
character = {
    'со значительным преимуществом': '⚔😎',
    'успешно атаковали защитников': '⚔',
    'разыгралась настоящая бойня, но все-таки силы атакующих были ': '⚔⚡',
    'успешно отбились от': '🛡',
    'легко отбились от': '🛡👌',
    'героически отразили ': '🛡⚡',
    'скучали, на них ': '🛡😴',
}
google.pop(0)
google.pop(0)
Auth = objects.AuthCentre(os.environ['TOKEN'])
bot = Auth.start_main_bot('non-async')
executive = Auth.thread_exec
#Auth.start_message(stamp1)
# ====================================================================================


def spacer(col):
    space = ''
    for j in range(col):
        space += ' '
    return space


def former_old(text, post_id):
    soup = BeautifulSoup(text.text, 'html.parser')
    is_post_not_exist = str(soup.find('div', class_='tgme_widget_message_error'))
    if str(is_post_not_exist) == 'None':
        brief = str(soup.find('div', class_='tgme_widget_message_text js-message_text'))
        brief = re.sub(r' (dir|class|style)=\\"\w+[^\\"]+\\"', '', brief)
        brief = re.sub('(<b>|</b>|<i>|</i>|<div>|</div>)', '', brief)
        brief = re.sub('/', '&#47;', brief)
        brief = re.sub('(<br&#47;>)', '/', brief)
        brief = str(post_id) + '/' + brief
    else:
        brief = 'false'
    return brief


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
    worksheet = gspread.service_account('1.json').open('Digest').worksheet('main2')
    google_values = worksheet.col_values(1)
    value = re.sub(r'\D', '', google_values[-1].split('/')[0])
    if len(value) > 0:
        last_post_id = int(value) + 1
        false_barrier = 0
        while True:
            try:
                print_text = main_address + str(last_post_id)
                response = requests.get(print_text + '?embed=1')
                text = former(response.text)
                battle_search = re.search(r'(\d{2}) (.*?) 10(\d{2}).Результаты сражений:', text)
                if battle_search:
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
                    google_values.append(text)
                    sleep(1.2)
                    print_text += ' Добавил битву в таблицу'
                    last_post_id += 1
                elif text == 'False':
                    if false_barrier < 4:
                        print_text += ' Поста нет, false_barrier = ' + str(false_barrier)
                        false_barrier += 1
                        last_post_id += 1
                        sleep(1)
                    else:
                        print_text += ' Постов нет вместе с false_barrier, ищем заново'
                        last_post_id -= false_barrier
                        false_barrier = 0
                        sleep(3)
                else:
                    print_text += ' Это не битва, пропускаю'
                    last_post_id += 1
                objects.printer(print_text)
            except IndexError and Exception:
                executive()
    else:
        Auth.send_json(None, 'war_google', 'Не найдено нормальное значение last_post_id, тред не может быть начат')


def war_checker():
    while True:
        try:
            global data2
            global checker
            printext = main_address + str(checker)
            if str(checker) not in ignore and checker > 3:
                text = requests.get(printext + '?embed=1')
                soup = former(text, checker)
                time_search = re.search(r'(\d{2}) (.*) 10(..).*Результаты сражений:', soup)
                if time_search:
                    try:
                        checking = data2.col_values(1)
                    except IndexError and Exception:
                        data2 = gspread.service_account('2.json').open('Digest').worksheet('main2')
                        checking = data2.col_values(1)
                    if soup not in checking:
                        doc_text = code('Привет\n' + printext + '\nЭтой битвы нет, в базе, проверь')
                        bot.send_message(idMe, doc_text, parse_mode='HTML')
                    printext += ' Проверил'
                    checker -= 1
                elif soup == 'false':
                    printext += ' Ничего нет, ничего не делаю'
                    sleep(20)
                else:
                    printext += ' Это не битва, пропускаю'
                    checker -= 1
            else:
                printext += ' В черном списке, пропускаю'
                checker -= 1
            objects.printer(printext)
            sleep(5)
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


def double_checker():
    while True:
        try:
            sleep(1800)
            for i in google:
                if google.count(i) > 1:
                    bot.send_message(idMe, 'Элемент\n\n' + str(i) + '\n\nповторяется в базе '
                                     + str(google.count(i)) + ' раз.\nНа данный момент он находится на позиции '
                                     + str(google.index(i)) + ' в массиве')
            objects.printer('готов')
        except IndexError and Exception:
            executive()


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60)
    except IndexError and Exception:
        bot.stop_polling()
        sleep(1)
        telegram_polling()


if __name__ == '__main__':
    gain = [battle_to_google]
    for thread_element in gain:
        _thread.start_new_thread(thread_element, ())
    telegram_polling()
