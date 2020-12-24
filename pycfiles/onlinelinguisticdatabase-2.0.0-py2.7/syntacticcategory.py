# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/syntacticcategory.py
# Compiled at: 2016-09-19 13:27:02
"""SyntacticCategory model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from onlinelinguisticdatabase.model.meta import Base, now

class SyntacticCategory(Base):
    __tablename__ = 'syntacticcategory'

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        return '<SyntacticCategory (%s)>' % self.id

    id = Column(Integer, Sequence('syntacticcategory_seq_id', optional=True), primary_key=True)
    name = Column(Unicode(255))
    type = Column(Unicode(60))
    description = Column(UnicodeText)
    datetime_modified = Column(DateTime, default=now)

    def get_dict(self):
        return {'id': self.id, 
           'name': self.name, 
           'type': self.type, 
           'description': self.description, 
           'datetime_modified': self.datetime_modified}