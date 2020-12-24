# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams_tests/models/email.py
# Compiled at: 2016-02-20 19:32:44
# Size of source mod 2**32: 385 bytes
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class EMail(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    mail = Column(Unicode)
    domain_id = Column(Integer, ForeignKey('domain.id'))
    domain = relationship('Domain')