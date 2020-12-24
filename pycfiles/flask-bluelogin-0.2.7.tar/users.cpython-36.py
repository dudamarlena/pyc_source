# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-bluelogin/flask_bluelogin/models/users.py
# Compiled at: 2017-04-30 09:29:28
# Size of source mod 2**32: 1649 bytes
from .base_model_ import Model
from ..util import NotFoundUserError, AlreadyExistUserError, Unauthorized
from flask import current_app

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = (super(Singleton, cls).__call__)(*args, **kwargs)
        return cls._instances[cls]


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
            current_app.logger.error(id)
            current_app.logger.error(self._users[id])
            return self._users[id]
        except KeyError as e:
            raise NotFoundUserError(detail=id)

    def add_user(self, user):
        if user.id in self._users:
            raise AlreadyExistUserError(user.id)
        self._users[user.id] = user

    def check_password(self, user, password):
        current_app.logger.error('check %s' % password)
        if user.id not in self._users:
            raise NotFoundUserError(user.id)
        current_app.logger.error('check %s' % self._users[user.id]._password)
        current_app.logger.error(self._users[user.id]._password == password)
        return self._users[user.id]._password == password