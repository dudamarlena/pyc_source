# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/value.py
# Compiled at: 2015-10-11 07:17:06
from .baseitem import BaseItem
from dbmanagr import KIND_FOREIGN_VALUE, KIND_FOREIGN_KEY, KIND_VALUE
from dbmanagr import IMAGE_FOREIGN_VALUE, IMAGE_FOREIGN_KEY, IMAGE_VALUE
TITLES = {KIND_FOREIGN_VALUE: '← %s', 
   KIND_FOREIGN_KEY: '→ %s', 
   KIND_VALUE: '%s'}
ICONS = {KIND_FOREIGN_VALUE: IMAGE_FOREIGN_VALUE, 
   KIND_FOREIGN_KEY: IMAGE_FOREIGN_KEY, 
   KIND_VALUE: IMAGE_VALUE}

class Value(BaseItem):
    """A value from the database"""

    def __init__(self, value, subtitle, autocomplete, validity, kind):
        self._value = value
        self._subtitle = subtitle
        self._autocomplete = autocomplete
        self._validity = validity
        self._kind = kind

    def title(self):
        if type(self._value) is buffer:
            return '[BLOB]'
        return TITLES.get(self._kind, KIND_VALUE) % self._value

    def subtitle(self):
        return self._subtitle

    def autocomplete(self):
        return self._autocomplete

    def validity(self):
        return self._validity

    def icon(self):
        return ICONS.get(self._kind, KIND_VALUE)

    def value(self):
        return self._value

    def as_json(self):
        return {'__cls__': str(self.__class__), 
           'value': self._value, 
           'subtitle': self._subtitle}