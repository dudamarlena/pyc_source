# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/posey/Documents/python-sdk/spawner/statistics.py
# Compiled at: 2020-04-19 18:33:55
# Size of source mod 2**32: 329 bytes
import requests, json, pandas

def correlation(token, list1, list2):
    list1 = ','.join([str(item) for item in list1])
    list2 = ','.join([str(item) for item in list1])
    url = 'https://spawnerapi.com/correlation/' + list1 + '/' + list2 + '/' + token
    response = requests.get(url).text
    return response