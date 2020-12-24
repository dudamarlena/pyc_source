# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/page.py
# Compiled at: 2016-09-19 13:27:02
"""Page model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from onlinelinguisticdatabase.model.meta import Base, now

class Page(Base):
    __tablename__ = 'page'

    def __repr__(self):
        return '<Page (%s)>' % self.id

    id = Column(Integer, Sequence('page_seq_id', optional=True), primary_key=True)
    name = Column(Unicode(255), unique=True)
    heading = Column(Unicode(255))
    markup_language = Column(Unicode(100))
    content = Column(UnicodeText)
    html = Column(UnicodeText)
    datetime_modified = Column(DateTime, default=now)