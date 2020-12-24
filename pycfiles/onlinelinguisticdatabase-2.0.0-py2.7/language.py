# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/language.py
# Compiled at: 2016-09-19 13:27:02
"""Language model"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime
from onlinelinguisticdatabase.model.meta import Base, now

class Language(Base):
    __tablename__ = 'language'

    def __repr__(self):
        return '<Language (%s)>' % self.Id

    Id = Column(Unicode(3), primary_key=True)
    Part2B = Column(Unicode(3))
    Part2T = Column(Unicode(3))
    Part1 = Column(Unicode(2))
    Scope = Column(Unicode(1))
    Type = Column(Unicode(1))
    Ref_Name = Column(Unicode(150))
    Comment = Column(Unicode(150))
    datetime_modified = Column(DateTime, default=now)