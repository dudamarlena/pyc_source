# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/flaskapp/base/models.py
# Compiled at: 2019-07-24 05:34:04
# Size of source mod 2**32: 485 bytes
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column((String(50)), unique=True)
    password = Column(String(64))

    def __init__(self, name=None, password=None):
        assert name is not None
        assert password is not None
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name