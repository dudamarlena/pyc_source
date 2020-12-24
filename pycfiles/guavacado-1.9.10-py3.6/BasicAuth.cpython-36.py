# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/BasicAuth.py
# Compiled at: 2020-04-06 15:29:31
# Size of source mod 2**32: 904 bytes
import base64

class BasicAuth(object):
    __doc__ = '\n\t\t"Basic" authentication scheme handler\n\t'

    def __init__(self, auth_handler=None, auth_dict=None, realm='Guavacado Server'):
        self.auth_type = 'Basic'
        self.realm = realm
        self.auth_dict = auth_dict
        self.auth_handler = auth_handler
        if self.auth_handler is None:
            self.auth_handler = self.check_auth_dict

    def authenticate(self, auth_type, credentials):
        """Convert the credentials to plain-text and call auth_handler to check if they are valid"""
        decoded = base64.b64decode(credentials).decode('utf-8')
        username, password = tuple(decoded.split(':', 1))
        return self.auth_handler(username, password)

    def check_auth_dict(self, username, password):
        if self.auth_dict is None:
            return False
        else:
            if username not in self.auth_dict:
                return False
            if self.auth_dict[username] == password:
                return True
            return False