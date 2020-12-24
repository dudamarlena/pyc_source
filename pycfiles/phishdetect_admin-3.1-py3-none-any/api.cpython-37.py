# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-admin/phishdetectadmin/api.py
# Compiled at: 2019-12-25 05:29:13
# Size of source mod 2**32: 2696 bytes
import requests
from .const import *
from . import session

def get_events():
    url = '{}{}?key={}'.format(session.__node__['host'], NODE_EVENTS_FETCH, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def get_raw_messages():
    url = '{}{}?key={}'.format(session.__node__['host'], NODE_RAW_FETCH, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def get_raw_details(uuid):
    url = '{}{}/{}/?key={}'.format(session.__node__['host'], NODE_RAW_DETAILS, uuid, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def add_indicators(indicators_type, indicators, tags=[]):
    data = {'type':indicators_type, 
     'indicators':indicators, 
     'tags':tags}
    url = '{}{}?key={}'.format(session.__node__['host'], NODE_INDICATORS_ADD, session.__node__['key'])
    res = requests.post(url, json=data)
    return res.json()


def get_indicator_details(indicator):
    url = '{}{}/{}/?key={}'.format(session.__node__['host'], NODE_INDICATORS_DETAILS, indicator, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def get_users_pending():
    url = '{}{}?key={}'.format(session.__node__['host'], NODE_USERS_PENDING, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def get_users_active():
    url = '{}{}?key={}'.format(session.__node__['host'], NODE_USERS_ACTIVE, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def activate_user(api_key):
    url = '{}{}/{}/?key={}'.format(session.__node__['host'], NODE_USERS_ACTIVATE, api_key, session.__node__['key'])
    res = requests.get(url)
    return res.json()


def deactivate_user(api_key):
    url = '{}{}/{}/?key={}'.format(session.__node__['host'], NODE_USERS_DEACTIVATE, api_key, session.__node__['key'])
    res = requests.get(url)
    return res.json()