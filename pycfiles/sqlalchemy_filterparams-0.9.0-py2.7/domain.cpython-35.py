# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams_tests/models/domain.py
# Compiled at: 2016-02-20 19:32:44
# Size of source mod 2**32: 240 bytes
from sqlalchemy import Column, Integer, Unicode
from .base import Base

class Domain(Base):
    __tablename__ = 'domain'
    id = Column(Integer, primary_key=True)
    domain = Column(Unicode)