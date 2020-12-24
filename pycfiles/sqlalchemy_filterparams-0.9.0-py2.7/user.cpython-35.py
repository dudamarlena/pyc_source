# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams_tests/models/user.py
# Compiled at: 2016-02-20 19:32:05
# Size of source mod 2**32: 504 bytes
from sqlalchemy import Column, Integer, Unicode, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    fullname = Column(Unicode)
    date_of_birth = Column(Date)
    created_at = Column(DateTime)
    email_id = Column(Integer, ForeignKey('email.id'))
    email = relationship('EMail')