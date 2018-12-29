# -*- coding: utf-8 -*-
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

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
creds5 = ServiceAccountCredentials.from_json_keyfile_name('bitvo5.json', scope)
client1 = gspread.authorize(creds1)
client5 = gspread.authorize(creds5)
data1 = client1.open('Digest').worksheet('main')
data5 = client1.open('Digest').worksheet('sup')

bot = telebot.TeleBot('658667571:AAERNsgYO-l0Ge7egyDbeSEPpuVDfJKeF5Q')
idMe = 396978030
bitva_ru = int(data1.cell(1, 1).value)
ignore_ru = str(data5.cell(2, 1).value)
ignore_ru = ignore_ru.split('/')
castle = '(🖤|🍆|🐢|🌹|🍁|☘️|🦇)'
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


def bitva_cw3():
    while True:
        try:
            sleep(3)
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
                    goo.append(bitva)
                    try:
                        data1.update_cell(1, 1, bitva_ru)
                        data1.insert_row(goo, 2)
                    except:
                        creds1 = ServiceAccountCredentials.from_json_keyfile_name('bitvo1.json', scope)
                        client1 = gspread.authorize(creds1)
                        data1 = client1.open('Digest').worksheet('main')
                        data1.update_cell(1, 1, bitva_ru)
                        data1.insert_row(goo, 2)
                    bitva_ru = bitva_ru + 1
                else:
                    print('https://t.me/chatwars3/' + str(bitva_ru) + ' Битвы пока нет, ничего не делаю')
            else:
                print('https://t.me/chatwars3/' + str(bitva_ru) + ' В черном списке, пропускаю')
                bitva_ru = bitva_ru + 1

        except Exception as e:
            bot.send_message(idMe, 'вылет bitva_ru')
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
    telepol()
