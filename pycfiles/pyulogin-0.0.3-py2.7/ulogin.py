# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyulogin/ulogin.py
# Compiled at: 2014-03-05 06:52:49
"""
Copyright (c)2014 Gurov Dmitri 

See the file license.txt for copying permission.

this file contains constans and data necessary for work with ulogin service:

url-- URL of ulogin's data provider(handler of this URL transform token to actual user data) 

fields-- list of all available field of user's profile from ulogin

UloginError -- dictionary with exceptions 
 """
import exceptions
url = 'http://ulogin.ru/token.php'
fields = ['first_name', 'last_name', 'email', 'nickname', 'bdate', 'sex',
 'phone', 'photo', 'photo_big', 'city', 'country', 'network', 'profile', 'uid', 'identity', 'manual', 'verified_email']
UloginError = {'token expired': exceptions.TokenExpired, 'invalid token': exceptions.InvalidToken, 'host is not XXX': exceptions.HostError}