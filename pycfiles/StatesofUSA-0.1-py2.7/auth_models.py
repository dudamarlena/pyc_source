# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statesofusa/auth_models.py
# Compiled at: 2016-03-09 12:21:34
__author__ = 'Isham'
USER_TOKEN_DICT = {'user1': '8590ae64-74e0-480a-a3ff-b676e4d0e9aa', 
   'user2': '38c50d14-436b-4e3e-b447-e2e9334fea1a'}

class Token(object):
    """
        Class to handle client tokens.
    """

    def __init__(self, usr, tok):
        self.user = usr
        self.token = tok

    @staticmethod
    def get(token):
        token_object = None
        for client_name, client_token in USER_TOKEN_DICT.items():
            if client_token == token:
                token_object = Token(client_name, client_token)

        return token_object