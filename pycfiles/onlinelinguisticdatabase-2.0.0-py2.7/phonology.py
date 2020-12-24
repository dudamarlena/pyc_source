# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/phonology.py
# Compiled at: 2016-09-19 13:27:02
"""Phonology model"""
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean
from sqlalchemy.orm import relation
from onlinelinguisticdatabase.model.meta import Base, now
from onlinelinguisticdatabase.lib.parser import PhonologyFST

class Phonology(PhonologyFST, Base):
    __tablename__ = 'phonology'

    def __repr__(self):
        return '<Phonology (%s)>' % self.id

    id = Column(Integer, Sequence('phonology_seq_id', optional=True), primary_key=True)
    UUID = Column(Unicode(36))
    name = Column(Unicode(255))
    description = Column(UnicodeText)
    script = Column(UnicodeText)
    enterer_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    enterer = relation('User', primaryjoin='Phonology.enterer_id==User.id')
    modifier_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    modifier = relation('User', primaryjoin='Phonology.modifier_id==User.id')
    datetime_entered = Column(DateTime)
    datetime_modified = Column(DateTime, default=now)
    compile_succeeded = Column(Boolean, default=False)
    compile_message = Column(Unicode(255))
    compile_attempt = Column(Unicode(36))
    parent_directory = Column(Unicode(255))
    word_boundary_symbol = Column(Unicode(10))

    def get_dict(self):
        return {'id': self.id, 
           'UUID': self.UUID, 
           'name': self.name, 
           'description': self.description, 
           'script': self.script, 
           'enterer': self.get_mini_user_dict(self.enterer), 
           'modifier': self.get_mini_user_dict(self.modifier), 
           'datetime_entered': self.datetime_entered, 
           'datetime_modified': self.datetime_modified, 
           'compile_succeeded': self.compile_succeeded, 
           'compile_message': self.compile_message, 
           'compile_attempt': self.compile_attempt}