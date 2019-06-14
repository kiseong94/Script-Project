#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import traceback

import box_office
import theater_info


TOKEN = '887936920:AAEOuYNJRh0yWC00ygyC00RRt38e6cV9u4s' #'여기에 텔레그램 토큰을 입력하세요'

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def RankData(date_param, user):
    print(user, date_param)
    res_list = box_office.GetBoxOfficeRankInfo(1)
    msg = ''
    for r in res_list:
        for n in r:
            msg += '[' + str(n['rank']) + '] ' + n['name'] + '\n'
    if msg:
        sendMessage( user, msg )
    else:
        sendMessage( user, '해당하는 데이터가 없습니다.')

def ScreeningData( date_param_location, date_param_theater, user):
    print(user, date_param_location, date_param_theater)
    res_list = theater_info.getTheaterInfo(date_param_location, "전체")
    movie_list = []
    msg = ''
    for r in res_list:
        if date_param_theater == r['name']:
            movie_list = theater_info.GetMovieInfo(r)['info']
            break

    if movie_list:
        for i in range(len(movie_list)):
            msg += '○' + movie_list[i]['movie'] + ' :'
            for n in range(len(movie_list[i]['time'])):
                msg += ' [' + movie_list[i]['time'][n] + ']'
            msg += '\n'
        sendMessage(user, msg)

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')
    movie_name = ''
    if args[0] == '랭킹':
        print('try to 랭킹', args[0])
        RankData( args[0], chat_id)
    elif text.startswith('검색') and len(args) >= 3:
        movie_name += args[2]
        if len(args) == 4:
            movie_name += ' ' + args[3]
        print('try to 검색', args[1], movie_name)
        ScreeningData(args[1], movie_name, chat_id)
    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n랭킹, 검색 [지역(도)][영화관] 중\n하나의 명령을 입력하세요.')


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', TOKEN )

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)

