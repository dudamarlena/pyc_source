# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/service/user_service.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 387 bytes
from domain import user

class UserManager(object):

    def __init__(self):
        self._UserManager__online_users = {}

    def user_login(self, u):
        if isinstance(u, user.User):
            self._UserManager__online_users[u.account] = u

    def user_logout(self, account):
        self._UserManager__online_users.pop(account, None)

    @property
    def online_users(self):
        return self._UserManager__online_users