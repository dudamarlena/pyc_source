# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\helper\http.py
# Compiled at: 2016-07-12 07:50:52
# Size of source mod 2**32: 1115 bytes
from datascryer.helper.python import python_3
if python_3():
    import urllib.request, urllib.error, urllib.parse
else:
    import urllib2

def get(url):
    if python_3():
        return urllib.request.urlopen(urllib.request.Request(url))
    else:
        return urllib2.urlopen(urllib2.Request(url))


def quote(string):
    if python_3():
        return urllib.parse.quote(string)
    else:
        return urllib2.quote(string)


def read(response):
    if python_3():
        return response.read().decode('utf8')
    else:
        return response.read()


def post(url, data, json=False):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if python_3():
        req = urllib.request.Request(url)
        if json:
            req.add_header('Content-Type', 'application/json; charset=utf-8')
        return urllib.request.urlopen(req, data)
    else:
        req = urllib2.Request(url, data)
        if json:
            req.add_header('Content-Type', 'application/json; charset=utf-8')
        return urllib2.urlopen(req)