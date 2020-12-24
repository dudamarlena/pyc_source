# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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