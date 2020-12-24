# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/keyboard.py
# Compiled at: 2016-09-19 13:27:02
"""Keyboard model: encodes a mapping between JavaScript key codes and Unicode
characters."""
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from sqlalchemy.orm import relation
from onlinelinguisticdatabase.model.meta import Base, now
import simplejson as json

class Keyboard(Base):
    __tablename__ = 'keyboard'

    def __repr__(self):
        return '<Keyboard (%s)>' % self.id

    id = Column(Integer, Sequence('keyboard_seq_id', optional=True), primary_key=True)
    name = Column(Unicode(255), unique=True)
    description = Column(UnicodeText)
    keyboard = Column(UnicodeText, default='{}')
    enterer_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    enterer = relation('User', primaryjoin='Keyboard.enterer_id==User.id')
    modifier_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    modifier = relation('User', primaryjoin='Keyboard.modifier_id==User.id')
    datetime_entered = Column(DateTime)
    datetime_modified = Column(DateTime, default=now)

    def get_dict(self):
        """Return a Python dictionary representation of the Keyboard.  This
        facilitates JSON-stringification, cf. utils.JSONOLDEncoder. Relational
        data are truncated, e.g., keyboard_dict['elicitor'] is a dict with keys
        for 'id', 'first_name' and 'last_name' (cf. get_mini_user_dict above) and
        lacks keys for other attributes such as 'username',
        'personal_page_content', etc.

        """
        try:
            keyboard = json.loads(self.keyboard)
        except (json.decoder.JSONDecodeError, TypeError):
            keyboard = {}

        return {'id': self.id, 
           'name': self.name, 
           'description': self.description, 
           'keyboard': keyboard, 
           'datetime_entered': self.datetime_entered, 
           'datetime_modified': self.datetime_modified, 
           'enterer': self.get_mini_user_dict(self.enterer), 
           'modifier': self.get_mini_user_dict(self.modifier)}