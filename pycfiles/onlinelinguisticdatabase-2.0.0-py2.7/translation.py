# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/translation.py
# Compiled at: 2016-09-19 13:27:02
"""Translation model"""
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from onlinelinguisticdatabase.model.meta import Base, now

class Translation(Base):
    __tablename__ = 'translation'

    def __repr__(self):
        return '<Translation (%s)>' % self.id

    id = Column(Integer, Sequence('translation_seq_id', optional=True), primary_key=True)
    transcription = Column(UnicodeText, nullable=False)
    grammaticality = Column(Unicode(255))
    form_id = Column(Integer, ForeignKey('form.id'))
    datetime_modified = Column(DateTime, default=now)