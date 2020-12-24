# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/schema.py
# Compiled at: 2011-02-12 01:39:53
"""(Default) Schema(s) / Data

...
"""
from hashlib import md5
from sqlalchemy import Boolean, Column, Integer, PickleType, Sequence, String
from dbm import Base
version = 1

class System(Base):
    __tablename__ = 'system'
    name = Column(String(20), primary_key=True)
    value = Column(String(80))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "<System('%s', '%s')>" % (self.name, self.value)


class User(Base):
    __tablename__ = 'users'
    username = Column(String(20), primary_key=True)
    password = Column(String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User('%s')>" % self.username


class Permission(Base):
    __tablename__ = 'permissions'
    username = Column(String(20), primary_key=True)
    action = Column(String(20), primary_key=True)

    def __init__(self, username, action):
        self.username = username
        self.action = action

    def __repr__(self):
        return "<Permission('%s', '%s')>" % (self.username, self.action)


class Session(Base):
    __tablename__ = 'sessions'
    sid = Column(String(256), primary_key=True)
    authenticated = Column(Boolean, index=True, primary_key=True)
    data = Column(PickleType)
    time = Column(Integer, index=True)

    def __init__(self, sid, authenticated):
        self.sid = sid
        self.authenticated = authenticated

    def __repr__(self):
        return "<Session('%s', '%s')>" % (self.sid, self.authenticated)


DATA = (
 (
  User,
  (
   (
    'admin', md5('admin').hexdigest()),)),
 (
  Permission,
  (
   ('anonymous', 'PAGE_DOWNLOAD'),
   ('anonymous', 'PAGE_HISTORY'),
   ('anonymous', 'PAGE_VIEW'),
   ('anonymous', 'SEARCH_VIEW'),
   ('authenticated', 'PAGE_EDIT'),
   ('authenticated', 'PAGE_DELETE'),
   ('authenticated', 'PAGE_RENAME'),
   ('authenticated', 'PAGE_UPLOAD'),
   ('admin', 'SAHRIS_ADMIN'))),
 (
  System,
  (
   (
    'schema_version', str(version)),)))