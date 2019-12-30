# -*- coding: utf-8 -*-
import re
import sys
import _thread
import gspread
import telebot
import datetime
import requests
import traceback
from time import sleep
from SQL import SQLighter
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
from oauth2client.service_account import ServiceAccountCredentials

stamp1 = int(datetime.now().timestamp())
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
checker = 4
bitva_id = int(data1.cell(1, 1).value)
ignore = str(data5.cell(2, 1).value)
our_month = int(data5.cell(1, 2).value)
ignore = ignore.split('/')
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


def bold(txt):
    return '<b>' + txt + '</b>'


def code(txt):
    return '<code>' + txt + '</code>'


def logtime(stamp):
    day = datetime.utcfromtimestamp(int(stamp)).strftime('%d')
    month = datetime.utcfromtimestamp(int(stamp)).strftime('%m')
    year = datetime.utcfromtimestamp(int(stamp)).strftime('%Y')
    hours = datetime.utcfromtimestamp(int(stamp)).strftime('%H')
    minutes = datetime.utcfromtimestamp(int(stamp)).strftime('%M')
    seconds = datetime.utcfromtimestamp(int(stamp)).strftime('%S')
    data = '<code>' + str(day) + '.' + str(month) + '.' + str(year) + \
           ' ' + str(hours) + ':' + str(minutes) + ':' + str(seconds) + '</code>'
    return data


logfile_start = open('log.txt', 'w')
logfile_start.write('Начало записи лога ' + re.sub('<.*?>', '', logtime(0)))
logfile_start.close()
# ====================================================================================
start_message = bot.send_message(idMe, code(logtime(stamp1) + '\n' + logtime(0)), parse_mode='HTML')


def executive(new):
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
                text = requests.get(printext)
                soup = former(text, bitva_id)
                time_search = re.search('(\d{2}) (.*) 10(..).*Результаты сражений:', soup)
                if time_search:
                    try:
                        data1.insert_row(soup, 3)
                        data1.update_cell(1, 1, bitva_id)
                    except:
                        creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
                        client1 = gspread.authorize(creds1)
                        data1 = client1.open('Digest').worksheet('main')
                        data1.insert_row(soup, 3)
                        data1.update_cell(1, 1, bitva_id)
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
            executive(war_google)


def war_checker():
    while True:
        try:
            sleep(8)
            global data3
            global checker
            printext = 'https://t.me/ChatWarsDigest/' + str(checker)
            if str(checker) not in ignore:
                text = requests.get(printext)
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
            executive(war_checker)


def summary_ru():
    while True:
        try:
            global data3
            global data5
            global start
            global finite
            sleep(30)
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
                fi = logtime(first_times)
                la = logtime(last_times)
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
            sleep(500)
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
                fi = logtime(first_times)
                la = logtime(last_times)
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
        except IndexError:
            executive(double_checker)


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    if message.chat.id != idMe:
        bot.send_message(message.chat.id, 'К тебе этот бот не имеет отношения, уйди пожалуйста')
    else:
        if message.text.startswith('/base'):
            modified = re.sub('/base_', '', message.text)
            if modified.startswith('n'):
                doc = open('actives.db', 'rb')
                bot.send_document(idMe, doc)
            elif modified.startswith('o'):
                doc = open('actives2.db', 'rb')
                bot.send_document(idMe, doc)
            else:
                doc = open('log.txt', 'rt')
                bot.send_document(idMe, doc)
            doc.close()
        else:
            bot.send_message(message.chat.id, 'Я работаю')


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        sleep(1)
        telepol()


if __name__ == '__main__':
    gain = [war_google, war_checker, double_checker]
    thread_array = defaultdict(dict)
    for i in gain:
        thread_id = _thread.start_new_thread(i, ())
        thread_start_name = re.findall('<.+?\s(.+?)\s.*>', str(i))
        thread_array[thread_id] = defaultdict(dict)
        thread_array[thread_id]['name'] = thread_start_name[0]
        thread_array[thread_id]['function'] = i
    telepol()
