# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-bluelogin/flask_bluelogin/models/users.py
# Compiled at: 2017-05-04 13:42:46
from .base_model_ import Model
from ..util import NotFoundUserError, AlreadyExistUserError, Unauthorized

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if 'Users' not in cls._instances:
            cls._instances['Users'] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances['Users']


import six

@six.add_metaclass(Singleton)
class Users(Model):

    def __init__(self):
        """
        Users
        """
        self._users = {}

    def set_user(self, user):
        if user.id not in self._users:
            raise NotFoundUserError(user.id)
        self._users[user.id] = user

    def get_user(self, id):
        try:
            return self._users[id]
        except KeyError as e:
            raise NotFoundUserError(detail=id)

    def add_user(self, user):
        if user.id in self._users:
            raise AlreadyExistUserError(user.id)
        self._users[user.id] = user

    def check_password(self, user, password):
        if user.id not in self._users:
            raise NotFoundUserError(user.id)
        return self._users[user.id]._password == password