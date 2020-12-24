# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\workpy\post.py
# Compiled at: 2019-08-10 00:50:49
# Size of source mod 2**32: 433 bytes
import requests, json
headers = {'content-type': 'application/json;charset=utf-8'}

def get(url):
    res = requests.get(url, headers=headers)
    return res.text


def post(url, msg):
    data = msg if isinstance(msg, str) else tojson(msg)
    res = requests.post(url, data=data, headers=headers)
    return res.text


def tojson(msg):
    return json.dumps(msg, ensure_ascii=False)


def tobean(msg):
    return json.loads(msg)