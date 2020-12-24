# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/alphahome/notify.py
# Compiled at: 2017-08-13 10:47:32
import requests, json
home = str()

def notice(appid, token, degree, message):
    global home
    url = 'https://api.alphaho.me/home/notice/'
    requests.post(url, data={'appid': appid, 
       'token': token, 
       'home': home, 
       'degree': degree, 
       'message': message})


def set_home(h):
    global home
    home = h