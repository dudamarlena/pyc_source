# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/http_client/auth_handler.py
# Compiled at: 2015-03-04 21:31:22


class AuthHandler:
    HTTP_PASSWORD = 0

    def __init__(self, auth):
        self.auth = auth

    def get_auth_type(self):
        if 'api_key' in self.auth:
            self.auth['password'] = ''
            return self.HTTP_PASSWORD
        return -1

    def set(self, request):
        if len(self.auth.keys()) == 0:
            return request
        auth = self.get_auth_type()
        flag = False
        if auth == self.HTTP_PASSWORD:
            request = self.http_password(request)
            flag = True
        if not flag:
            raise StandardError('Unable to calculate authorization method. Please check')
        return request

    def http_password(self, request):
        request['auth'] = (
         self.auth['api_key'], self.auth['password'])
        return request