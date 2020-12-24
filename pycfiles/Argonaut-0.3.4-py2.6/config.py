# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/config.py
# Compiled at: 2011-02-18 19:15:08
"""The config model"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, UnicodeText
from argonaut.model.meta import Base, Session

class Config(Base):
    __tablename__ = 'config'
    id = Column(Unicode(50), primary_key=True)
    value = Column(UnicodeText)

    def __init__(self, id=None, value=None):
        self.id = id
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return "<Config('%s','%s')>" % (self.id, self.value)

    __str__ = __unicode__


def get(id):
    return str(Session.query(Config).get(id).value)