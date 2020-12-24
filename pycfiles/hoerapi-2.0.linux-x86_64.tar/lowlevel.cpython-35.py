# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/lowlevel.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 706 bytes
import requests
from hoerapi.errors import InvalidJsonError, ApiError, NoDataError
API_URL = 'http://hoersuppe.de/api/'

def status():
    try:
        rjson = requests.get(API_URL, params={'action': 'getLiveByID'}).json()
        return rjson['status'] == 0 and rjson['msg'] == 'no ID given'
    except:
        return False


def call_api(action, params={}):
    params = params.copy()
    params['action'] = action
    r = requests.get(API_URL, params=params)
    try:
        rjson = r.json()
    except:
        raise InvalidJsonError(r.text)

    if rjson['status'] != 1:
        raise ApiError(rjson['msg'])
    if 'data' not in rjson:
        raise NoDataError()
    return rjson['data']