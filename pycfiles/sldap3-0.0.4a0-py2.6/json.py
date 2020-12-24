# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\backend\user\json.py
# Compiled at: 2015-04-13 15:52:16
"""
"""
import json
from ..user import UserBaseBackend
from ...core.user import User

class JsonUserBackend(UserBaseBackend):

    def __init__(self, json_file):
        self.json_file = json_file
        try:
            self.users = json.load(open(json_file))
        except Exception:
            self.users = {}

        super().__init__()

    def find_user(self, identity):
        if identity in self.users:
            return User(identity, self.users[identity])
        else:
            return

    def add_user(self, identity, authorization, credentials):
        if identity not in self.users:
            self.users[identity] = {'auth': authorization, 'password': credentials}
            return True
        return False

    def del_user(self, identity):
        if identity in self.users:
            del self.users[identity]
            return True
        return False

    def modify_user(self, identity, new_identity):
        if identity in self.users:
            if self.add_user(new_identity, self.users[identity]):
                self.del_user(identity)
                return True
        return False

    def check_credentials(self, user, credentials):
        if user.identity in self.users:
            if self.users[user.identity]['password'] == credentials:
                return True
        return False

    def store(self):
        json.dump({'users': self.users}, open(self.json_file, 'w+'))

    @classmethod
    def unauthenticated(cls):
        return User('un-authenticated')

    @classmethod
    def anonymous(cls):
        return User('anonymous')