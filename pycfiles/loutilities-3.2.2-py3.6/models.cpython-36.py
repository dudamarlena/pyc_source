# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\models.py
# Compiled at: 2018-07-03 16:23:03
# Size of source mod 2**32: 2701 bytes
"""
models - dummy unit test models
=====================================================
from https://raw.githubusercontent.com/louking/sqlalchemy-datatables/master/tests/models.py

"""
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
Base = declarative_base()

class User(Base):
    __doc__ = 'Define a User.'
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=(datetime.datetime.utcnow))
    address = relationship('Address', uselist=False, backref=(backref('user')))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % self.name

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)

    @hybrid_property
    def dummy(self):
        return '%s%s-DUMMY' % (self.name[0:1], str(self.id))

    @dummy.expression
    def dummy(cls):
        return True


class Address(Base):
    __doc__ = 'Define an Address.'
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    description = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % self.id

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)


class NotUnique(Base):
    __doc__ = '\n    table with values which are not necessarily unique\n    '
    __tablename__ = 'notunique'
    id = Column(Integer, primary_key=True)
    value = Column(String)


class SeveralAttrs(Base):
    __doc__ = '\n    table with several attributes\n    '
    __tablename__ = 'severalattrs'
    id = Column(Integer, primary_key=True)
    intAttr1 = Column(Integer)
    strAttr2 = Column(String)
    strAttr3 = Column(String)
    boolAttr4 = Column(Boolean)
    dateAttr5 = Column(DateTime)