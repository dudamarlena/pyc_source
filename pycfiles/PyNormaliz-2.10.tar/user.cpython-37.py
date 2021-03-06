# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/models/user.py
# Compiled at: 2019-03-11 04:26:11
# Size of source mod 2**32: 995 bytes
from sqlalchemy import Column, Integer, String, DateTime
from norm.models import Model

class User(Model):
    """User"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column((String(64)), nullable=False)
    last_name = Column((String(64)), nullable=False)
    username = Column((String(64)), unique=True, nullable=False)
    email = Column((String(64)), unique=True, nullable=False)
    last_login = Column(DateTime)
    login_count = Column(Integer)
    fail_login_count = Column(Integer)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()