# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/http.py
# Compiled at: 2014-10-17 04:09:18
import json, hashlib, requests
from os import environ
from os.path import join
from titan import __version__ as version
from config import titanConfig
TITAN_PATH = environ.get('TITAN_PATH') or '/var/lib/titan/'
TITAN_CONFIG = join('/etc/', 'titan.conf')
CONFIG = titanConfig(TITAN_CONFIG, TITAN_PATH)
HEADERS = {'User-Agent': 'titanOSX %s' % version, 
   'X-Titan-Token': CONFIG['reporting']['token']}

def request(url, data=None, type=None):
    r = None
    try:
        if data is not None:
            r = post(url, data)
        elif type is None:
            r = get(url)
        else:
            r = globals()[type](url)
        if r is not None and r.status_code == 402:
            print ':: API TOKEN REQUIRED'
            exit()
        return (r.status_code, r.content)
    except requests.exceptions.ConnectionError as e:
        return (0, 'A connection could not be established')
    except requests.exceptions.HTTPError as e:
        return (
         e.status, e.message)
    except requests.exceptions.RequestException as e:
        return (
         0, e.message)

    return


def post(url, data=None):
    r = requests.post(url, data=data, headers=HEADERS)
    return r


def get(url):
    r = requests.get(url, headers=HEADERS)
    return r


def put(url):
    r = requests.put(url, headers=HEADERS)
    return r


def delete(url):
    r = requests.delete(url, headers=HEADERS)
    return r