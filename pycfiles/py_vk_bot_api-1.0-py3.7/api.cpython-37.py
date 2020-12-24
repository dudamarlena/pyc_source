# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_vk_bot_api\api.py
# Compiled at: 2019-05-11 13:02:12
# Size of source mod 2**32: 1047 bytes
from requests import post
from .exceptions import *
from .session import session as ses

class api(object):

    def __init__(self, session, v='5.95'):
        if not isinstance(session, ses):
            raise mySword('invalid session')
        self.token = session.token
        self.ver = v

    def call(self, method, params={}):
        res = post(f"https://api.vk.com/method/{method}", {**{'access_token':self.token,  'v':self.ver}, **params}).json()
        if 'error' not in res:
            return res['response']
        return res

    def parseuid(self, text):
        try:
            if 'vk.com/' in text:
                u = (text.split('vk.com/')[1] + ' ').split(' ')[0]
                u = u.split('/')[0] if '/' in u else u
            else:
                u = text.strip()
            try:
                return self.call('users.get', {'user_ids': u})[0]['id']
            except:
                return -self.call('groups.getById', {'group_ids': u})[0]['id']

        except:
            return