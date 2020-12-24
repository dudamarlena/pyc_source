# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jobspider\baseclass\utils\get_cookies.py
# Compiled at: 2016-03-23 21:00:33
import requests

def get_cookie(url):
    resp = requests.get(url)
    return resp.cookies.items()