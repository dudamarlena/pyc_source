# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\auth.py
# Compiled at: 2015-01-11 13:52:03
from chatpy.error import ChatpyError
from chatpy.api import API

class AuthHandler(object):

    def apply_auth(self, url, method, headers, parameters):
        """Apply authentication headers to request"""
        raise NotImplementedError

    def get_username(self):
        """Return the username of the authenticated user"""
        raise NotImplementedError


class TokenAuthHandler(AuthHandler):

    def __init__(self, token):
        self.token = token
        self.username = None
        return

    def apply_auth(self, url, method, headers, parameters):
        headers['X-ChatWorkToken'] = self.token

    def get_username(self):
        if self.username is None:
            api = API(self)
            user = api.me()
            if user:
                self.username = user.name
            else:
                raise ChatpyError('Unable to get username, invalid token!')
        return self.username