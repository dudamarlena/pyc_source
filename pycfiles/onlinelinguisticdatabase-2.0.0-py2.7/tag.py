# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/tag.py
# Compiled at: 2016-09-19 13:27:02
"""Tag model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from onlinelinguisticdatabase.model.meta import Base, now

class Tag(Base):
    __tablename__ = 'tag'

    def __repr__(self):
        return '<Tag (%s)>' % self.id

    id = Column(Integer, Sequence('tag_seq_id', optional=True), primary_key=True)
    name = Column(Unicode(255), unique=True)
    description = Column(UnicodeText)
    datetime_modified = Column(DateTime, default=now)

    def get_dict(self):
        return {'id': self.id, 
           'name': self.name, 
           'description': self.description, 
           'datetime_modified': self.datetime_modified}