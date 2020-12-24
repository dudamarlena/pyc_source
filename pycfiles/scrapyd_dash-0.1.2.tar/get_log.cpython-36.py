# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dainius/Desktop/scrapyd-dash/scrapyd_dash/operations/get_log.py
# Compiled at: 2019-07-11 03:54:51
# Size of source mod 2**32: 231 bytes
import requests, json

def get_log(href):
    timeout = 5
    try:
        with requests.get(href, timeout=timeout) as (r):
            return r.json()
    except:
        raise Exception('LogParser server does not respond')