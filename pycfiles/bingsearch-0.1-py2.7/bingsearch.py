# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bingsearch.py
# Compiled at: 2012-06-18 20:10:32
import requests
URL = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/Web?Query=%(query)s&$top=50&$format=json'
API_KEY = 'SECRET_API_KEY'

def request(query, **params):
    r = requests.get(URL % {'query': query}, auth=('', API_KEY))
    return r.json['d']['results']