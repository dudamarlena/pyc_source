# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/speaker.py
# Compiled at: 2016-09-19 13:27:02
"""Speaker model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from onlinelinguisticdatabase.model.meta import Base, now

class Speaker(Base):
    __tablename__ = 'speaker'

    def __repr__(self):
        return '<Speaker (%s)>' % self.id

    id = Column(Integer, Sequence('speaker_seq_id', optional=True), primary_key=True)
    first_name = Column(Unicode(255))
    last_name = Column(Unicode(255))
    dialect = Column(Unicode(255))
    markup_language = Column(Unicode(100))
    page_content = Column(UnicodeText)
    html = Column(UnicodeText)
    datetime_modified = Column(DateTime, default=now)

    def get_dict(self):
        return {'id': self.id, 
           'first_name': self.first_name, 
           'last_name': self.last_name, 
           'dialect': self.dialect, 
           'markup_language': self.markup_language, 
           'page_content': self.page_content, 
           'html': self.html, 
           'datetime_modified': self.datetime_modified}