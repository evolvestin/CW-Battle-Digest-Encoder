# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types
import urllib3
import re
import requests# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types
import urllib3
import re
import requests
import time
from time import sleep
import datetime
from datetime import datetime
import _thread
import random
from SQL import SQLighter

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
creds4 = ServiceAccountCredentials.from_json_keyfile_name('bitvo4.json', scope)
creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
client1 = gspread.authorize(creds1)
client3 = gspread.authorize(creds3)
client4 = gspread.authorize(creds4)
client5 = gspread.authorize(creds5)
data1 = client1.open('Digest').worksheet('main')
data3 = client3.open('Digest').worksheet('main')
data4 = client4.open('Digest').worksheet('main')
data5 = client5.open('Digest').worksheet('sup')
start = int(data5.cell(2, 2).value)
finite = int(data5.cell(2, 3).value)

bot = telebot.TeleBot('733988805:AAGi7yK8wziPgkn25R8a86XbPUlFwLSbBBE')
idMe = 396978030
checker = 641
bitva_ru = int(data1.cell(1, 1).value)
ignore_ru = str(data5.cell(2, 1).value)
our_month = int(data5.cell(1, 2).value)
ignore_ru = ignore_ru.split('/')
castle = '(🖤|🍆|🐢|🌹|🍁|☘️|🦇)'
castle_db = ['🖤', '🍆', '🐢', '🌹', '🍁', '☘️', '🦇']
castle_names = ['skala', 'farm', 'tort', 'rose', 'amber', 'oplot', 'night']
form_a = '⛳️Сводки с полей:\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n'

form_b = '🏆Очки:\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n\n' \
    + 'Битва (.+)'

# ====================================================================================
bot.send_message(idMe, '👀')


def big_time(stamp):
    day = datetime.utcfromtimestamp(int(stamp)).strftime('%d')
    month = datetime.utcfromtimestamp(int(stamp)).strftime('%m')
    year = datetime.utcfromtimestamp(int(stamp)).strftime('%Y')
    hours = datetime.utcfromtimestamp(int(stamp)).strftime('%H')
    minutes = datetime.utcfromtimestamp(int(stamp)).strftime('%M')
    seconds = datetime.utcfromtimestamp(int(stamp)).strftime('%S')
    data = '<code>' + str(day) + '.' + str(month) + '.' + str(year) + \
           ' ' + str(hours) + ':' + str(minutes) + ':' + str(seconds) + '</code>'
    return data


def bitva_cw3():
    while True:
        try:
            sleep(5)
            global data1
            global bitva_ru
            goo = []
            if str(bitva_ru) not in ignore_ru:
                text = requests.get('https://t.me/CWDigest/' + str(bitva_ru))
                search1 = re.search(form_a, str(text.text))
                search2 = re.search(form_b, str(text.text))
                if search1:
                    print('работаю https://t.me/CWDigest/' + str(bitva_ru))
                    bitva = str(int(time.mktime(datetime.strptime(search2.group(15), '%d/%m/%y %H:%M').timetuple())))
                    hours_btv = int(datetime.utcfromtimestamp(int(bitva)).strftime('%H'))
                    if hours_btv == 6 or hours_btv == 14 or hours_btv == 22:
                        bitva = str(int(bitva) + 3 * 60 * 60)
                    for i in search1.groups():
                        if i in castle and i != '':
                            points = '+0'
                            for g in search1.groups():
                                if g == i:
                                    points = search2.group(search2.groups().index(g) + 2)
                            gold = search1.group(search1.groups().index(i) + 3)
                            box = search1.group(search1.groups().index(i) + 4)
                            if gold != '😴':
                                gold = re.sub('💰', '', gold)
                            else:
                                gold = '+0'
                            if box != '':
                                box = re.sub('📦', '', box)
                            else:
                                box = '+0'
                            bitva = bitva + '/' + search1.group(search1.groups().index(i) + 1) + '.' + \
                                    search1.group(search1.groups().index(i) + 2) + '.' + gold + '.' + box + '.' + points
                    bitva = re.sub('🏆Очки:', '+0', bitva)
                    goo.append(str(bitva))
                    bitva_ru = bitva_ru + 1
                    try:
                        data1.insert_row(goo, 2)
                        data1.update_cell(1, 1, bitva_ru)
                    except:
                        creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
                        client1 = gspread.authorize(creds1)
                        data1 = client1.open('Digest').worksheet('main')
                        data1.insert_row(goo, 2)
                        data1.update_cell(1, 1, bitva_ru)
                else:
                    print('https://t.me/CWDigest/' + str(bitva_ru) + ' Битвы пока нет, ничего не делаю')
            else:
                print('https://t.me/CWDigest/' + str(bitva_ru) + ' В черном списке, пропускаю')
                bitva_ru = bitva_ru + 1

        except Exception as e:
            bot.send_message(idMe, str(e))
            bot.send_message(idMe, 'вылет bitva_ru')
            sleep(0.9)


def bitva_cw3_checker():
    while True:
        try:
            sleep(20)
            global data3
            global checker
            if str(checker) not in ignore_ru:
                text = requests.get('https://t.me/CWDigest/' + str(checker))
                search1 = re.search(form_a, str(text.text))
                search2 = re.search(form_b, str(text.text))
                if search1:
                    print('проверяю https://t.me/CWDigest/' + str(checker))
                    bitva = str(int(time.mktime(datetime.strptime(search2.group(15), '%d/%m/%y %H:%M').timetuple())))
                    hours_btv = int(datetime.utcfromtimestamp(int(bitva)).strftime('%H'))
                    if hours_btv == 6 or hours_btv == 14 or hours_btv == 22:
                        bitva = str(int(bitva) + 3 * 60 * 60)
                    for i in search1.groups():
                        if i in castle and i != '':
                            points = '+0'
                            for g in search1.groups():
                                if g == i:
                                    points = search2.group(search2.groups().index(g) + 2)
                            gold = search1.group(search1.groups().index(i) + 3)
                            box = search1.group(search1.groups().index(i) + 4)
                            if gold != '😴':
                                gold = re.sub('💰', '', gold)
                            else:
                                gold = '+0'
                            if box != '':
                                box = re.sub('📦', '', box)
                            else:
                                box = '+0'
                            bitva = bitva + '/' + search1.group(search1.groups().index(i) + 1) + '.' + \
                                    search1.group(search1.groups().index(i) + 2) + '.' + gold + '.' + box + '.' + points
                    bitva = re.sub('🏆Очки:', '+0', bitva)
                    try:
                        google = data3.col_values(1)
                    except:
                        creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                        client3 = gspread.authorize(creds3)
                        data3 = client3.open('Digest').worksheet('main')
                        google = data3.col_values(1)
                    checker = checker + 1
                    if bitva not in google:
                        bot.send_message(idMe, 'Привет\nhttps://t.me/CWDigest/' + str(checker - 1) +
                                         '\n\n' + str(bitva) + '\n\nЭтой битвы нет, в базе, проверь')
                else:
                    print('https://t.me/CWDigest/' + str(checker) + ' прошел все, нареканий нет')
            else:
                print('проверка https://t.me/CWDigest/' + str(checker) + ' В черном списке, пропускаю')
                checker = checker + 1

        except Exception as e:
            bot.send_message(idMe, str(e))
            bot.send_message(idMe, 'вылет bitva_ru_checker')
            sleep(0.9)


def summary_ru():
    while True:
        try:
            global data3
            global data5
            global start
            global finite
            sleep(300)
            db = SQLighter('actives.db')
            first_times = 0
            last_times = 0
            try:
                google = data3.col_values(1)
            except:
                creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                client3 = gspread.authorize(creds3)
                data3 = client3.open('Digest').worksheet('main')
                google = data3.col_values(1)
            google.pop(0)
            google.reverse()
            for i in castle_names:
                db.update_castle(i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            for i in google:
                bitva = i.split('/')
                if int(bitva[0]) >= start and int(bitva[0]) <= finite:
                    if int(bitva[0]) == start:
                        first_times = int(bitva[0])
                    if int(bitva[0]) == finite:
                        last_times = int(bitva[0])
                    bitva.pop(0)
                    for h in bitva:
                        splited = h.split('.')
                        name = castle_names[castle_db.index(splited[0])]
                        castle_array = db.get_castle(name)
                        gold = castle_array[1]
                        box = castle_array[2]
                        point = castle_array[3]
                        atk = castle_array[4]
                        atk_high = castle_array[5]
                        atk_low = castle_array[6]
                        deff = castle_array[7]
                        def_high = castle_array[8]
                        def_low = castle_array[9]
                        def_ger = castle_array[10]
                        sleeps = castle_array[11]
                        if splited[2][:1] == '+':
                            gold = gold + int(re.sub('\+', '', splited[2]))
                        else:
                            gold = gold - int(re.sub('-', '', splited[2]))
                        if splited[3][:1] == '+':
                            box = box + int(re.sub('\+', '', splited[3]))
                        else:
                            box = box - int(re.sub('-', '', splited[3]))
                        if splited[4][:1] == '+':
                            point = point + int(re.sub('\+', '', splited[4]))
                        else:
                            point = point - int(re.sub('-', '', splited[4]))
                        if splited[1] == '⚔️':
                            atk = atk + 1
                        elif splited[1] == '⚔️😎':
                            atk_high = atk_high + 1
                        elif splited[1] == '⚔️⚡️':
                            atk_low = atk_low + 1
                        elif splited[1] == '🛡':
                            deff = deff + 1
                        elif splited[1] == '🛡⚡️':
                            def_high = def_high + 1
                        elif splited[1] == '🛡👌':
                            def_low = def_low + 1
                        elif splited[1] == '🔱🛡⚡️':
                            def_ger = def_ger + 1
                        elif splited[1] == '😴️':
                            sleeps = sleeps + 1
                        else:
                            print(splited[1])
                        db.update_castle(name, gold, box, point, atk, atk_high, atk_low, deff, def_high, def_low,
                                         def_ger, sleeps)

            if last_times > 0:
                paper = db.get_paper()
                fi = big_time(first_times)
                la = big_time(last_times)
                text = '<b>Отчет за неделю</b> (' + fi + ' - ' + la + ')\n'
                for i in paper:
                    name = castle_db[castle_names.index(i[0])]
                    text = text + name + ': '
                    if i[1] >= 0:
                        text = text + '+' + str(i[1]) + '💰 '
                    else:
                        text = text + str(i[1]) + '💰 '
                    if i[2] >= 0:
                        text = text + '+' + str(i[2]) + '📦 '
                    else:
                        text = text + str(i[2]) + '📦 '
                    if i[3] >= 0:
                        text = text + '+' + str(i[3]) + '🏆 \n'
                    else:
                        text = text + str(i[3]) + '🏆 \n'
                    text = text + '⚔️<code>:' + str(i[4]) + '</code>'
                    if i[5] > 0:
                        text = text + '<code>|⚔️😎:' + str(i[5]) + '</code>'
                    if i[6] > 0:
                        text = text + '<code>|⚔️⚡️:' + str(i[6]) + '</code>'
                    if i[7] > 0:
                        text = text + '<code>|🛡:' + str(i[7]) + '</code>'
                    if i[8] > 0:
                        text = text + '<code>|🛡⚡:' + str(i[8]) + '</code>'
                    # if i[9] > 0:
                    # text = text + '<code>|🛡👌️:' + str(i[9]) + '</code>'
                    if i[10] > 0:
                        text = text + '<code>|🔱️:' + str(i[10]) + '</code>'
                    if i[11] > 0:
                        text = text + '<code>|😴:' + str(i[11]) + '</code>'

                    text = text + '\n'
                #bot.send_message(idMe, text, parse_mode='HTML')
                bot.send_message(-1001444070646, text, parse_mode='HTML')
                start = finite + (8 * 60 * 60)
                finite = finite + (7 * 24 * 60 * 60) #- (8 * 60 * 60)
                try:
                    data5.update_cell(2, 2, start)
                    data5.update_cell(2, 3, finite)
                except:
                    creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                    creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
                    client3 = gspread.authorize(creds3)
                    client5 = gspread.authorize(creds5)
                    data3 = client3.open('Digest').worksheet('main')
                    data5 = client5.open('Digest').worksheet('sup')
                    data5.update_cell(2, 2, start)
                    data5.update_cell(2, 3, finite)
        except Exception as e:
            bot.send_message(idMe, 'вылет summary_ru\n' + str(e))
            sleep(0.9)


def month():
    while True:
        try:
            global data3
            global data5
            global bitva_ru
            sleep(300)
            db = SQLighter('actives2.db')
            first_times = 0
            last_times = 0
            try:
                google = data3.col_values(1)
            except:
                creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                client3 = gspread.authorize(creds3)
                data3 = client3.open('Digest').worksheet('main')
                google = data3.col_values(1)
            google.pop(0)
            google.reverse()
            for i in castle_names:
                db.update_castle(i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            m = 0
            for i in google:
                bitva = i.split('/')
                month = int(datetime.utcfromtimestamp(int(bitva[0])).strftime('%m'))
                if month == our_month:
                    if m == 0:
                        first_times = int(bitva[0])
                        m = 1
                    if int(bitva[0]) > last_times:
                        last_times = int(bitva[0])
                    bitva.pop(0)
                    for h in bitva:
                        splited = h.split('.')
                        name = castle_names[castle_db.index(splited[0])]
                        castle_array = db.get_castle(name)
                        gold = castle_array[1]
                        box = castle_array[2]
                        point = castle_array[3]
                        atk = castle_array[4]
                        atk_high = castle_array[5]
                        atk_low = castle_array[6]
                        deff = castle_array[7]
                        def_high = castle_array[8]
                        def_low = castle_array[9]
                        def_ger = castle_array[10]
                        sleeps = castle_array[11]
                        if splited[2][:1] == '+':
                            gold = gold + int(re.sub('\+', '', splited[2]))
                        else:
                            gold = gold - int(re.sub('-', '', splited[2]))
                        if splited[3][:1] == '+':
                            box = box + int(re.sub('\+', '', splited[3]))
                        else:
                            box = box - int(re.sub('-', '', splited[3]))
                        if splited[4][:1] == '+':
                            point = point + int(re.sub('\+', '', splited[4]))
                        else:
                            point = point - int(re.sub('-', '', splited[4]))
                        if splited[1] == '⚔️':
                            atk = atk + 1
                        elif splited[1] == '⚔️😎':
                            atk_high = atk_high + 1
                        elif splited[1] == '⚔️⚡️':
                            atk_low = atk_low + 1
                        elif splited[1] == '🛡':
                            deff = deff + 1
                        elif splited[1] == '🛡⚡️':
                            def_high = def_high + 1
                        elif splited[1] == '🛡👌':
                            def_low = def_low + 1
                        elif splited[1] == '🔱🛡⚡️':
                            def_ger = def_ger + 1
                        elif splited[1] == '😴️':
                            sleeps = sleeps + 1
                        else:
                            print(splited[1])
                        db.update_castle(name, gold, box, point, atk, atk_high, atk_low, deff, def_high, def_low,
                                         def_ger, sleeps)

            posting = int(datetime.utcfromtimestamp(int(last_times + 8 * 60 * 60)).strftime('%m'))
            if posting == 1 and our_month == 12:
                posting = 13

            if posting > our_month:
                paper = db.get_paper()
                fi = big_time(first_times)
                la = big_time(last_times)
                text = '<b>Отчет за месяц</b> (' + fi + ' - ' + la + ')\n'
                for i in paper:
                    name = castle_db[castle_names.index(i[0])]
                    text = text + name + ': '
                    if i[1] >= 0:
                        text = text + '+' + str(i[1]) + '💰 '
                    else:
                        text = text + str(i[1]) + '💰 '
                    if i[2] >= 0:
                        text = text + '+' + str(i[2]) + '📦 '
                    else:
                        text = text + str(i[2]) + '📦 '
                    if i[3] >= 0:
                        text = text + '+' + str(i[3]) + '🏆 \n'
                    else:
                        text = text + str(i[3]) + '🏆 \n'
                    text = text + '⚔️<code>:' + str(i[4]) + '</code>'
                    if i[5] > 0:
                        text = text + '<code>|⚔️😎:' + str(i[5]) + '</code>'
                    if i[6] > 0:
                        text = text + '<code>|⚔️⚡️:' + str(i[6]) + '</code>'
                    if i[7] > 0:
                        text = text + '<code>|🛡:' + str(i[7]) + '</code>'
                    if i[8] > 0:
                        text = text + '<code>|🛡⚡:' + str(i[8]) + '</code>'
                    # if i[9] > 0:
                    # text = text + '<code>|🛡👌️:' + str(i[9]) + '</code>'
                    if i[10] > 0:
                        text = text + '<code>|🔱️:' + str(i[10]) + '</code>'
                    if i[11] > 0:
                        text = text + '<code>|😴:' + str(i[11]) + '</code>'
                    text = text + '\n'
                bot.send_message(-1001444070646, text, parse_mode='HTML')
                if posting == 13:
                    posting = 1
                try:
                    data5.update_cell(1, 2, int(posting))
                except:
                    creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
                    client5 = gspread.authorize(creds5)
                    data5 = client5.open('Digest').worksheet('sup')
                    data5.update_cell(1, 2, int(posting))

        except Exception as e:
            bot.send_message(idMe, 'вылет month\n' + str(e))
            sleep(0.9)


def double_checker():
    while True:
        try:
            sleep(1800)
            global data4
            try:
                google = data4.col_values(1)
            except:
                creds4 = ServiceAccountCredentials.from_json_keyfile_name('bitvo4.json', scope)
                client4 = gspread.authorize(creds4)
                data4 = client4.open('Digest').worksheet('main')
                google = data4.col_values(1)
            for i in google:
                if google.count(i) > 1:
                    bot.send_message(idMe, 'Элемент\n\n' + str(i) + '\n\nповторяется в базе '
                                     + str(google.count(i)) + ' раз.\nНа данный момент он находится на позиции '
                                     + str(google.index(i)) + ' в массиве')
        except Exception as e:
            bot.send_message(idMe, 'double_checker\n' + str(e))
            sleep(0.9)


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    if message.chat.id != idMe:
        bot.send_message(idMe, 'К тебе этот бот не имеет отношения, уйди пожалуйста')
    else:
        bot.send_message(idMe, 'Я работаю')


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        sleep(1)
        telepol()


if __name__ == '__main__':
    _thread.start_new_thread(bitva_cw3, ())
    _thread.start_new_thread(summary_ru, ())
    _thread.start_new_thread(bitva_cw3_checker, ())
    _thread.start_new_thread(month, ())
    _thread.start_new_thread(double_checker, ())
    telepol()
import time
from time import sleep
import datetime
from datetime import datetime
import _thread
import random
from SQL import SQLighter

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
creds4 = ServiceAccountCredentials.from_json_keyfile_name('bitvo4.json', scope)
creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
client1 = gspread.authorize(creds1)
client3 = gspread.authorize(creds3)
client4 = gspread.authorize(creds4)
client5 = gspread.authorize(creds5)
data1 = client1.open('Digest').worksheet('main')
data3 = client3.open('Digest').worksheet('main')
data4 = client4.open('Digest').worksheet('main')
data5 = client5.open('Digest').worksheet('sup')
start = int(data5.cell(2, 2).value)
finite = int(data5.cell(2, 3).value)

bot = telebot.TeleBot('733988805:AAGi7yK8wziPgkn25R8a86XbPUlFwLSbBBE')
idMe = 396978030
checker = 641
bitva_ru = int(data1.cell(1, 1).value)
ignore_ru = str(data5.cell(2, 1).value)
our_month = int(data5.cell(1, 2).value)
ignore_ru = ignore_ru.split('/')
castle = '(🖤|🍆|🐢|🌹|🍁|☘️|🦇)'
castle_db = ['🖤', '🍆', '🐢', '🌹', '🍁', '☘️', '🦇']
castle_names = ['skala', 'farm', 'tort', 'rose', 'amber', 'oplot', 'night']
form_a = '⛳️Сводки с полей:\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n' \
    + castle + ': (\S+) (\S*)\s*(\-*.*)\n'

form_b = '🏆Очки:\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n' \
    + castle + '.+: +(.+)\n\n' \
    + 'Битва (.+)'

# ====================================================================================
bot.send_message(idMe, '👀')


def big_time(stamp):
    day = datetime.utcfromtimestamp(int(stamp)).strftime('%d')
    month = datetime.utcfromtimestamp(int(stamp)).strftime('%m')
    year = datetime.utcfromtimestamp(int(stamp)).strftime('%Y')
    hours = datetime.utcfromtimestamp(int(stamp)).strftime('%H')
    minutes = datetime.utcfromtimestamp(int(stamp)).strftime('%M')
    seconds = datetime.utcfromtimestamp(int(stamp)).strftime('%S')
    data = '<code>' + str(day) + '.' + str(month) + '.' + str(year) + \
           ' ' + str(hours) + ':' + str(minutes) + ':' + str(seconds) + '</code>'
    return data


def bitva_cw3():
    while True:
        try:
            sleep(5)
            global data1
            global bitva_ru
            goo = []
            if str(bitva_ru) not in ignore_ru:
                text = requests.get('https://t.me/CWDigest/' + str(bitva_ru))
                search1 = re.search(form_a, str(text.text))
                search2 = re.search(form_b, str(text.text))
                if search1:
                    print('работаю https://t.me/CWDigest/' + str(bitva_ru))
                    bitva = str(int(time.mktime(datetime.strptime(search2.group(15), '%d/%m/%y %H:%M').timetuple())))
                    hours_btv = int(datetime.utcfromtimestamp(int(bitva)).strftime('%H'))
                    if hours_btv == 6 or hours_btv == 14 or hours_btv == 22:
                        bitva = str(int(bitva) + 3 * 60 * 60)
                    for i in search1.groups():
                        if i in castle and i != '':
                            points = '+0'
                            for g in search1.groups():
                                if g == i:
                                    points = search2.group(search2.groups().index(g) + 2)
                            gold = search1.group(search1.groups().index(i) + 3)
                            box = search1.group(search1.groups().index(i) + 4)
                            if gold != '😴':
                                gold = re.sub('💰', '', gold)
                            else:
                                gold = '+0'
                            if box != '':
                                box = re.sub('📦', '', box)
                            else:
                                box = '+0'
                            bitva = bitva + '/' + search1.group(search1.groups().index(i) + 1) + '.' + \
                                    search1.group(search1.groups().index(i) + 2) + '.' + gold + '.' + box + '.' + points
                    bitva = re.sub('🏆Очки:', '+0', bitva)
                    goo.append(str(bitva))
                    bitva_ru = bitva_ru + 1
                    try:
                        data1.insert_row(goo, 2)
                        data1.update_cell(1, 1, bitva_ru)
                    except:
                        creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
                        client1 = gspread.authorize(creds1)
                        data1 = client1.open('Digest').worksheet('main')
                        data1.insert_row(goo, 2)
                        data1.update_cell(1, 1, bitva_ru)
                else:
                    print('https://t.me/CWDigest/' + str(bitva_ru) + ' Битвы пока нет, ничего не делаю')
            else:
                print('https://t.me/CWDigest/' + str(bitva_ru) + ' В черном списке, пропускаю')
                bitva_ru = bitva_ru + 1

        except Exception as e:
            bot.send_message(idMe, str(e))
            bot.send_message(idMe, 'вылет bitva_ru')
            sleep(0.9)


def bitva_cw3_checker():
    while True:
        try:
            sleep(20)
            global data3
            global checker
            if str(checker) not in ignore_ru:
                text = requests.get('https://t.me/CWDigest/' + str(checker))
                search1 = re.search(form_a, str(text.text))
                search2 = re.search(form_b, str(text.text))
                if search1:
                    print('проверяю https://t.me/CWDigest/' + str(checker))
                    bitva = str(int(time.mktime(datetime.strptime(search2.group(15), '%d/%m/%y %H:%M').timetuple())))
                    hours_btv = int(datetime.utcfromtimestamp(int(bitva)).strftime('%H'))
                    if hours_btv == 6 or hours_btv == 14 or hours_btv == 22:
                        bitva = str(int(bitva) + 3 * 60 * 60)
                    for i in search1.groups():
                        if i in castle and i != '':
                            points = '+0'
                            for g in search1.groups():
                                if g == i:
                                    points = search2.group(search2.groups().index(g) + 2)
                            gold = search1.group(search1.groups().index(i) + 3)
                            box = search1.group(search1.groups().index(i) + 4)
                            if gold != '😴':
                                gold = re.sub('💰', '', gold)
                            else:
                                gold = '+0'
                            if box != '':
                                box = re.sub('📦', '', box)
                            else:
                                box = '+0'
                            bitva = bitva + '/' + search1.group(search1.groups().index(i) + 1) + '.' + \
                                    search1.group(search1.groups().index(i) + 2) + '.' + gold + '.' + box + '.' + points
                    bitva = re.sub('🏆Очки:', '+0', bitva)
                    try:
                        google = data3.col_values(1)
                    except:
                        creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                        client3 = gspread.authorize(creds3)
                        data3 = client3.open('Digest').worksheet('main')
                        google = data3.col_values(1)
                    checker = checker + 1
                    if bitva not in google:
                        bot.send_message(idMe, 'Привет\nhttps://t.me/CWDigest/' + str(checker - 1) +
                                         '\n\n' + str(bitva) + '\n\nЭтой битвы нет, в базе, проверь')
                else:
                    print('https://t.me/CWDigest/' + str(checker) + ' прошел все, нареканий нет')
            else:
                print('проверка https://t.me/CWDigest/' + str(checker) + ' В черном списке, пропускаю')
                checker = checker + 1

        except Exception as e:
            bot.send_message(idMe, str(e))
            bot.send_message(idMe, 'вылет bitva_ru_checker')
            sleep(0.9)


def summary_ru():
    while True:
        try:
            global data3
            global data5
            global start
            global finite
            sleep(300)
            db = SQLighter('actives.db')
            first_times = 0
            last_times = 0
            try:
                google = data3.col_values(1)
            except:
                creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                client3 = gspread.authorize(creds3)
                data3 = client3.open('Digest').worksheet('main')
                google = data3.col_values(1)
            google.pop(0)
            google.reverse()
            for i in castle_names:
                db.update_castle(i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            for i in google:
                bitva = i.split('/')
                if int(bitva[0]) >= start and int(bitva[0]) <= finite:
                    if int(bitva[0]) == start:
                        first_times = int(bitva[0])
                    if int(bitva[0]) == finite:
                        last_times = int(bitva[0])
                    bitva.pop(0)
                    for h in bitva:
                        splited = h.split('.')
                        name = castle_names[castle_db.index(splited[0])]
                        castle_array = db.get_castle(name)
                        gold = castle_array[1]
                        box = castle_array[2]
                        point = castle_array[3]
                        atk = castle_array[4]
                        atk_high = castle_array[5]
                        atk_low = castle_array[6]
                        deff = castle_array[7]
                        def_high = castle_array[8]
                        def_low = castle_array[9]
                        def_ger = castle_array[10]
                        sleeps = castle_array[11]
                        if splited[2][:1] == '+':
                            gold = gold + int(re.sub('\+', '', splited[2]))
                        else:
                            gold = gold - int(re.sub('-', '', splited[2]))
                        if splited[3][:1] == '+':
                            box = box + int(re.sub('\+', '', splited[3]))
                        else:
                            box = box - int(re.sub('-', '', splited[3]))
                        if splited[4][:1] == '+':
                            point = point + int(re.sub('\+', '', splited[4]))
                        else:
                            point = point - int(re.sub('-', '', splited[4]))
                        if splited[1] == '⚔️':
                            atk = atk + 1
                        elif splited[1] == '⚔️😎':
                            atk_high = atk_high + 1
                        elif splited[1] == '⚔️⚡️':
                            atk_low = atk_low + 1
                        elif splited[1] == '🛡':
                            deff = deff + 1
                        elif splited[1] == '🛡⚡️':
                            def_high = def_high + 1
                        elif splited[1] == '🛡👌':
                            def_low = def_low + 1
                        elif splited[1] == '🔱🛡⚡️':
                            def_ger = def_ger + 1
                        elif splited[1] == '😴️':
                            sleeps = sleeps + 1
                        else:
                            print(splited[1])
                        db.update_castle(name, gold, box, point, atk, atk_high, atk_low, deff, def_high, def_low,
                                         def_ger, sleeps)

            if last_times > 0:
                paper = db.get_paper()
                fi = big_time(first_times)
                la = big_time(last_times)
                text = '<b>Отчет за неделю</b> (' + fi + ' - ' + la + ')\n'
                for i in paper:
                    name = castle_db[castle_names.index(i[0])]
                    text = text + name + ': '
                    if i[1] >= 0:
                        text = text + '+' + str(i[1]) + '💰 '
                    else:
                        text = text + str(i[1]) + '💰 '
                    if i[2] >= 0:
                        text = text + '+' + str(i[2]) + '📦 '
                    else:
                        text = text + str(i[2]) + '📦 '
                    if i[3] >= 0:
                        text = text + '+' + str(i[3]) + '🏆 \n'
                    else:
                        text = text + str(i[3]) + '🏆 \n'
                    text = text + '⚔️<code>:' + str(i[4]) + '</code>'
                    if i[5] > 0:
                        text = text + '<code>|⚔️😎:' + str(i[5]) + '</code>'
                    if i[6] > 0:
                        text = text + '<code>|⚔️⚡️:' + str(i[6]) + '</code>'
                    if i[7] > 0:
                        text = text + '<code>|🛡:' + str(i[7]) + '</code>'
                    if i[8] > 0:
                        text = text + '<code>|🛡⚡:' + str(i[8]) + '</code>'
                    # if i[9] > 0:
                    # text = text + '<code>|🛡👌️:' + str(i[9]) + '</code>'
                    if i[10] > 0:
                        text = text + '<code>|🔱️:' + str(i[10]) + '</code>'
                    if i[11] > 0:
                        text = text + '<code>|😴:' + str(i[11]) + '</code>'

                    text = text + '\n'
                #bot.send_message(idMe, text, parse_mode='HTML')
                bot.send_message(-1001444070646, text, parse_mode='HTML')
                start = finite + (8 * 60 * 60)
                finite = finite + (7 * 24 * 60 * 60) #- (8 * 60 * 60)
                try:
                    data5.update_cell(2, 2, start)
                    data5.update_cell(2, 3, finite)
                except:
                    creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                    creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
                    client3 = gspread.authorize(creds3)
                    client5 = gspread.authorize(creds5)
                    data3 = client3.open('Digest').worksheet('main')
                    data5 = client5.open('Digest').worksheet('sup')
                    data5.update_cell(2, 2, start)
                    data5.update_cell(2, 3, finite)
        except Exception as e:
            bot.send_message(idMe, 'вылет summary_ru\n' + str(e))
            sleep(0.9)


def month():
    while True:
        try:
            global data3
            global data5
            global bitva_ru
            sleep(300)
            db = SQLighter('actives2.db')
            first_times = 0
            last_times = 0
            try:
                google = data3.col_values(1)
            except:
                creds3 = ServiceAccountCredentials.from_json_keyfile_name('bitvo3.json', scope)
                client3 = gspread.authorize(creds3)
                data3 = client3.open('Digest').worksheet('main')
                google = data3.col_values(1)
            google.pop(0)
            google.reverse()
            for i in castle_names:
                db.update_castle(i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            m = 0
            for i in google:
                bitva = i.split('/')
                month = int(datetime.utcfromtimestamp(int(bitva[0])).strftime('%m'))
                if month == our_month:
                    if m == 0:
                        first_times = int(bitva[0])
                        m = 1
                    if int(bitva[0]) > last_times:
                        last_times = int(bitva[0])
                    bitva.pop(0)
                    for h in bitva:
                        splited = h.split('.')
                        name = castle_names[castle_db.index(splited[0])]
                        castle_array = db.get_castle(name)
                        gold = castle_array[1]
                        box = castle_array[2]
                        point = castle_array[3]
                        atk = castle_array[4]
                        atk_high = castle_array[5]
                        atk_low = castle_array[6]
                        deff = castle_array[7]
                        def_high = castle_array[8]
                        def_low = castle_array[9]
                        def_ger = castle_array[10]
                        sleeps = castle_array[11]
                        if splited[2][:1] == '+':
                            gold = gold + int(re.sub('\+', '', splited[2]))
                        else:
                            gold = gold - int(re.sub('-', '', splited[2]))
                        if splited[3][:1] == '+':
                            box = box + int(re.sub('\+', '', splited[3]))
                        else:
                            box = box - int(re.sub('-', '', splited[3]))
                        if splited[4][:1] == '+':
                            point = point + int(re.sub('\+', '', splited[4]))
                        else:
                            point = point - int(re.sub('-', '', splited[4]))
                        if splited[1] == '⚔️':
                            atk = atk + 1
                        elif splited[1] == '⚔️😎':
                            atk_high = atk_high + 1
                        elif splited[1] == '⚔️⚡️':
                            atk_low = atk_low + 1
                        elif splited[1] == '🛡':
                            deff = deff + 1
                        elif splited[1] == '🛡⚡️':
                            def_high = def_high + 1
                        elif splited[1] == '🛡👌':
                            def_low = def_low + 1
                        elif splited[1] == '🔱🛡⚡️':
                            def_ger = def_ger + 1
                        elif splited[1] == '😴️':
                            sleeps = sleeps + 1
                        else:
                            print(splited[1])
                        db.update_castle(name, gold, box, point, atk, atk_high, atk_low, deff, def_high, def_low,
                                         def_ger, sleeps)

            posting = int(datetime.utcfromtimestamp(int(last_times + 8 * 60 * 60)).strftime('%m'))
            if posting == 1 and our_month == 12:
                posting = 13

            if posting > our_month:
                paper = db.get_paper()
                fi = big_time(first_times)
                la = big_time(last_times)
                text = '<b>Отчет за месяц</b> (' + fi + ' - ' + la + ')\n'
                for i in paper:
                    name = castle_db[castle_names.index(i[0])]
                    text = text + name + ': '
                    if i[1] >= 0:
                        text = text + '+' + str(i[1]) + '💰 '
                    else:
                        text = text + str(i[1]) + '💰 '
                    if i[2] >= 0:
                        text = text + '+' + str(i[2]) + '📦 '
                    else:
                        text = text + str(i[2]) + '📦 '
                    if i[3] >= 0:
                        text = text + '+' + str(i[3]) + '🏆 \n'
                    else:
                        text = text + str(i[3]) + '🏆 \n'
                    text = text + '⚔️<code>:' + str(i[4]) + '</code>'
                    if i[5] > 0:
                        text = text + '<code>|⚔️😎:' + str(i[5]) + '</code>'
                    if i[6] > 0:
                        text = text + '<code>|⚔️⚡️:' + str(i[6]) + '</code>'
                    if i[7] > 0:
                        text = text + '<code>|🛡:' + str(i[7]) + '</code>'
                    if i[8] > 0:
                        text = text + '<code>|🛡⚡:' + str(i[8]) + '</code>'
                    # if i[9] > 0:
                    # text = text + '<code>|🛡👌️:' + str(i[9]) + '</code>'
                    if i[10] > 0:
                        text = text + '<code>|🔱️:' + str(i[10]) + '</code>'
                    if i[11] > 0:
                        text = text + '<code>|😴:' + str(i[11]) + '</code>'
                    text = text + '\n'
                bot.send_message(-1001444070646, text, parse_mode='HTML')
                if posting == 13:
                    posting = 1
                try:
                    data5.update_cell(1, 2, int(posting))
                except:
                    creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
                    client5 = gspread.authorize(creds5)
                    data5 = client5.open('Digest').worksheet('sup')
                    data5.update_cell(1, 2, int(posting))

        except Exception as e:
            bot.send_message(idMe, 'вылет month\n' + str(e))
            sleep(0.9)


def double_checker():
    while True:
        try:
            sleep(1800)
            global data4
            try:
                google = data4.col_values(1)
            except:
                creds4 = ServiceAccountCredentials.from_json_keyfile_name('bitvo4.json', scope)
                client4 = gspread.authorize(creds4)
                data4 = client4.open('Digest').worksheet('main')
                google = data4.col_values(1)
            for i in google:
                if google.count(i) > 1:
                    bot.send_message(idMe, 'Элемент\n\n' + str(i) + '\n\nповторяется в базе '
                                     + str(google.count(i)) + ' раз.\nНа данный момент он находится на позиции '
                                     + str(google.index(i)) + ' в массиве')
        except Exception as e:
            bot.send_message(idMe, 'double_checker\n' + str(e))
            sleep(0.9)


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    if message.chat.id != idMe:
        bot.send_message(idMe, 'К тебе этот бот не имеет отношения, уйди пожалуйста')
    else:
        bot.send_message(idMe, 'Я работаю')


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        sleep(1)
        telepol()


if __name__ == '__main__':
    _thread.start_new_thread(bitva_cw3, ())
    _thread.start_new_thread(summary_ru, ())
    _thread.start_new_thread(bitva_cw3_checker, ())
    _thread.start_new_thread(month, ())
    _thread.start_new_thread(double_checker, ())
    telepol()
