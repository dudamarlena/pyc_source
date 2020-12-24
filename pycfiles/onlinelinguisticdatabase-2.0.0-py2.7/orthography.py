# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/orthography.py
# Compiled at: 2016-09-19 13:27:02
"""Orthography model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean
from onlinelinguisticdatabase.model.meta import Base, now

class Orthography(Base):
    __tablename__ = 'orthography'

    def __repr__(self):
        return '<Orthography (%s)>' % self.id

    id = Column(Integer, Sequence('orthography_seq_id', optional=True), primary_key=True)
    name = Column(Unicode(255))
    orthography = Column(UnicodeText)
    lowercase = Column(Boolean, default=False)
    initial_glottal_stops = Column(Boolean, default=True)
    datetime_modified = Column(DateTime, default=now)