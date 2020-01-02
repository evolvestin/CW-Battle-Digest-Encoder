# -*- coding: utf-8 -*-
import re
import sys
import time
import _thread
import gspread
import telebot
import requests
import traceback
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
from oauth2client.service_account import ServiceAccountCredentials

stamp1 = int(datetime.now().timestamp())
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
creds2 = ServiceAccountCredentials.from_json_keyfile_name('bitvo2.json', scope)
creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
client1 = gspread.authorize(creds1)
client2 = gspread.authorize(creds2)
client3 = gspread.authorize(creds3)
data1 = client1.open('Digest').worksheet('main')
data2 = client2.open('Digest').worksheet('main')
data3 = client3.open('Digest').worksheet('main')
checker = 4
idMe = 396978030
e_trident = '🔱'
bitva_id = int(data1.cell(1, 1).value)
ignore = str(data1.cell(2, 1).value)
ignore = ignore.split('/')
castle = '(🖤|🍆|🐢|🌹|🍁|☘️|🦇)'
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


# ====================================================================================


def bold(txt):
    return '<b>' + txt + '</b>'


def code(txt):
    return '<code>' + txt + '</code>'


def stamper(date, adder):
    import datetime
    try:
        stamp = int(datetime.datetime.strptime(date, "%d.%m.%Y").timestamp() + adder)
    except:
        stamp = False
    return stamp


def logtime(stamp):
    if stamp == 0:
        stamp = int(datetime.now().timestamp())
    day = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%d')
    month = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%m')
    year = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%Y')
    hours = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%H')
    minutes = datetime.utcfromtimestamp(int(stamp)).strftime('%M')
    seconds = datetime.utcfromtimestamp(int(stamp)).strftime('%S')
    message = str(day) + '.' + str(month) + '.' + str(year) + ' ' + str(hours) + ':' \
        + str(minutes) + ':' + str(seconds)
    return message


logfile_start = open('log.txt', 'w')
logfile_start.write('Начало записи лога ' + re.sub('<.*?>', '', logtime(0)))
logfile_start.close()
# ====================================================================================
bot = telebot.TeleBot('733988805:AAGi7yK8wziPgkn25R8a86XbPUlFwLSbBBE')
start_message = bot.send_message(idMe, code(logtime(stamp1) + '\n' + logtime(0)), parse_mode='HTML')


def executive(new, logs):
    global thread_array
    search = re.search('<function (\S+)', str(new))
    if search:
        name = search.group(1)
    else:
        name = ''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_raw = traceback.format_exception(exc_type, exc_value, exc_traceback)
    error = ''
    for i in error_raw:
        error += str(i)
    bot.send_message(idMe, 'Вылет ' + name + '\n' + error)
    if logs == 0:
        sleep(100)
        thread_id = _thread.start_new_thread(new, ())
        thread_array[thread_id] = defaultdict(dict)
        thread_array[thread_id]['name'] = name
        thread_array[thread_id]['function'] = new
        bot.send_message(idMe, 'Запущен ' + bold(name), parse_mode='HTML')
        sleep(30)
        _thread.exit()


def printer(printer_text):
    thread_name = str(thread_array[_thread.get_ident()]['name'])
    logfile = open('log.txt', 'a')
    log_print_text = thread_name + ' ' + printer_text
    logfile.write('\n' + re.sub('<.*?>', '', logtime(0)) + log_print_text)
    logfile.close()
    print(log_print_text)


def timer(search):
    s_day = int(search.group(1))
    s_month = str(search.group(2))
    s_year = int(search.group(3)) - 60
    stamp = int(datetime.now().timestamp())
    sec = ((stamp + (3 * 60 * 60) - 1530309600) * 3)
    if s_month == 'Wintar':
        month = 1
    elif s_month == 'Hornung':
        month = 2
    elif s_month == 'Lenzin':
        month = 3
    elif s_month == 'Ōstar':
        month = 4
    elif s_month == 'Winni':
        month = 5
    elif s_month == 'Brāh':
        month = 6
    elif s_month == 'Hewi':
        month = 7
    elif s_month == 'Aran':
        month = 8
    elif s_month == 'Witu':
        month = 9
    elif s_month == 'Wīndume':
        month = 10
    elif s_month == 'Herbist':
        month = 11
    elif s_month == 'Hailag':
        month = 12
    else:
        month = 0

    if month != 0:
        day31 = 31 * 24 * 60 * 60
        day30 = 30 * 24 * 60 * 60
        day28 = 28 * 24 * 60 * 60
        seconds = 0 - (24 * 60 * 60)
        if s_year == 4:
            day28 = day28 + 24 * 60 * 60
        elif s_year > 4:
            seconds = seconds + 24 * 60 * 60
        seconds = seconds + day30 + day31 + 31536000 * (s_year - 1)  # Wīndume
        if month == 1:
            seconds = seconds
        elif month == 2:
            seconds = seconds + day31
        elif month == 3:
            seconds = seconds + day31 + day28
        elif month == 4:
            seconds = seconds + day31 + day28 + day31
        elif month == 5:
            seconds = seconds + day31 + day28 + day31 + day30
        elif month == 6:
            seconds = seconds + day31 + day28 + day31 + day30 + day31
        elif month == 7:
            seconds = seconds + day31 + day28 + day31 + day30 + day31 + day30
        elif month == 8:
            seconds = seconds + day31 + day28 + day31 + day30 + day31 + day30 + day31
        elif month == 9:
            seconds = seconds + day31 + day28 + day31 + day30 + day31 + day30 + day31 + day31
        elif month == 10:
            seconds = seconds + day31 + day28 + day31 + day30 + day31 + day30 + day31 + day31 + day30
        elif month == 11:
            seconds = seconds + day31 + day28 + day31 + day30 + day31 + day30 + day31 + day31 + day30 + day31
            if s_year == 0:
                seconds = 0 - (24 * 60 * 60)
        elif month == 12:
            seconds = seconds + day31 + day28 + day31 + day30 + day31 + day30 + day31 + day31 + day30 + day31 + day30
            if s_year == 0:
                seconds = day30 - (24 * 60 * 60)

        seconds = seconds + s_day * 24 * 60 * 60
        stack = int(stamp + (seconds - sec) / 3) + 2 * 60 * 60
        return stack


def former(text, id):
    soup = BeautifulSoup(text.text, 'html.parser')
    is_post_not_exist = str(soup.find('div', class_='tgme_widget_message_error'))
    if str(is_post_not_exist) == 'None':
        brief = str(soup.find('div', class_='tgme_widget_message_text js-message_text'))
        brief = re.sub(' (dir|class|style)=\\"\w+[^\\"]+\\"', '', brief)
        brief = re.sub('(<b>|</b>|<i>|</i>|<div>|</div>)', '', brief)
        brief = re.sub('/', '&#47;', brief)
        brief = re.sub('(<br&#47;>)', '/', brief)
        brief = str(id) + '/' + brief
    else:
        brief = 'false'
    return brief


def war_google():
    while True:
        try:
            sleep(1)
            global data1
            global bitva_id
            printext = 'https://t.me/ChatWarsDigest/' + str(bitva_id)
            if str(bitva_id) not in ignore:
                text = requests.get(printext + '?embed=1')
                soup = former(text, bitva_id)
                time_search = re.search('(\d{2}) (.*) 10(..).*Результаты сражений:', soup)
                if time_search:
                    try:
                        data1.insert_row([soup], 3)
                        data1.update_cell(1, 1, bitva_id + 1)
                    except:
                        creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
                        client1 = gspread.authorize(creds1)
                        data1 = client1.open('Digest').worksheet('main')
                        data1.insert_row([soup], 3)
                        data1.update_cell(1, 1, bitva_id + 1)
                    sleep(5)
                    printext += ' Добавил битву в google'
                    bitva_id += 1
                elif soup == 'false':
                    printext += ' Ничего нет, ничего не делаю'
                else:
                    printext += ' Это не битва, пропускаю'
                    bitva_id += 1
            else:
                printext += ' В черном списке, пропускаю'
                bitva_id += 1
            printer(printext)
        except IndexError:
            executive(war_google, 0)


def war_checker():
    while True:
        try:
            sleep(8)
            global data3
            global checker
            printext = 'https://t.me/ChatWarsDigest/' + str(checker)
            if str(checker) not in ignore:
                text = requests.get(printext + '?embed=1')
                soup = former(text, checker)
                time_search = re.search('(\d{2}) (.*) 10(..).*Результаты сражений:', soup)
                if time_search:
                    try:
                        google = data3.col_values(1)
                    except:
                        creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                        client3 = gspread.authorize(creds3)
                        data3 = client3.open('Digest').worksheet('main')
                        google = data3.col_values(1)
                    if soup not in google:
                        bot.send_message(idMe, 'Привет\n' + printext + '\n\n' + str(soup) +
                                         '\n\nЭтой битвы нет, в базе, проверь')
                    printext += ' Проверил'
                    checker += 1
                elif soup == 'false':
                    printext += ' Ничего нет, ничего не делаю'
                    sleep(20)
                else:
                    printext += ' Это не битва, пропускаю'
                    checker += 1
            else:
                printext += ' В черном списке, пропускаю'
                checker += 1
            printer(printext)
        except IndexError:
            executive(war_checker, 0)


def summary(time_start, time_end):
    print('time_start = ' + str(time_start) + ' ' + logtime(time_start))
    print('time_end = ' + str(time_end) + ' ' + logtime(time_end))
    global data2
    try:
        google = data2.col_values(1)
    except:
        creds2 = ServiceAccountCredentials.from_json_keyfile_name('bitvo2.json', scope)
        client2 = gspread.authorize(creds2)
        data2 = client2.open('Digest').worksheet('main')
        google = data2.col_values(1)
    google.pop(0)
    google.pop(0)
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
        time_search = re.search('(\d{2}) (.*) 10(..).*Результаты сражений:', battle)
        soup = re.sub('.*Результаты сражений:/', '', battle)
        soup = re.sub('//По итогам сражений замкам начислено:.+', '', soup)
        splited = re.split('//', soup)
        if time_search:
            date = timer(time_search)
            if time_start <= date <= time_end:
                print('date = ' + str(date) + ' ' + logtime(date))
                if trophy_search:
                    trophy = re.split('/', trophy_search.group(1))
                    for i in trophy:
                        search = re.search(castle + '.+ \+(\d+) 🏆 очков', i)
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


def double_checker():
    while True:
        try:
            sleep(1800)
            global data2
            try:
                google = data2.col_values(1)
            except:
                creds2 = ServiceAccountCredentials.from_json_keyfile_name('bitvo2.json', scope)
                client2 = gspread.authorize(creds2)
                data2 = client2.open('Digest').worksheet('main')
                google = data2.col_values(1)
            for i in google:
                if google.count(i) > 1:
                    bot.send_message(idMe, 'Элемент\n\n' + str(i) + '\n\nповторяется в базе '
                                     + str(google.count(i)) + ' раз.\nНа данный момент он находится на позиции '
                                     + str(google.index(i)) + ' в массиве')
        except IndexError:
            executive(double_checker, 0)


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    try:
        if message.text.startswith('/summary'):
            modified = re.sub('/summary ', '', message.text)
            search = re.search('(.*?)-(.*?)\n(.*)', modified)
            if search:
                starting = stamper(search.group(1), 0)
                ending = stamper(search.group(2), 17 * 60 * 60)
                print(starting)
                print(ending)
                text = search.group(3)
                if str(starting) != 'False' and str(ending) != 'False':
                    text += '\n(' + code(logtime(starting) + ' - ' + logtime(ending)) + ')\n'
                    text += summary(starting, ending)
                bot.send_message(message.chat.id, text, parse_mode='HTML')
        elif message.chat.id == idMe:
            if message.text.startswith('/base'):
                doc = open('log.txt', 'rt')
                bot.send_document(idMe, doc)
                doc.close()
            else:
                bot.send_message(message.chat.id, 'Я работаю')
    except IndexError:
        executive(repeat_all_messages, 1)


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        sleep(1)
        telepol()


if __name__ == '__main__':
    gain = []
    # gain = [war_google, war_checker, double_checker]
    thread_array = defaultdict(dict)
    for i in gain:
        thread_id = _thread.start_new_thread(i, ())
        thread_start_name = re.findall('<.+?\s(.+?)\s.*>', str(i))
        thread_array[thread_id] = defaultdict(dict)
        thread_array[thread_id]['name'] = thread_start_name[0]
        thread_array[thread_id]['function'] = i
    telepol()
