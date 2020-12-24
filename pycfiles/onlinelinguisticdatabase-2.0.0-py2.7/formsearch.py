# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/formsearch.py
# Compiled at: 2016-09-19 13:27:02
"""FormSearch model"""
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from sqlalchemy.orm import relation
from onlinelinguisticdatabase.model.meta import Base, now
import logging
log = logging.getLogger(__name__)

class FormSearch(Base):
    __tablename__ = 'formsearch'

    def __repr__(self):
        return '<FormSearch (%s)>' % self.id

    id = Column(Integer, Sequence('formsearch_seq_id', optional=True), primary_key=True)
    name = Column(Unicode(255))
    search = Column(UnicodeText)
    description = Column(UnicodeText)
    enterer_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    enterer = relation('User')
    datetime_modified = Column(DateTime, default=now)

    def get_dict(self):
        return {'id': self.id, 
           'name': self.name, 
           'search': self.json_loads(self.search), 
           'description': self.description, 
           'enterer': self.get_mini_user_dict(self.enterer), 
           'datetime_modified': self.datetime_modified}