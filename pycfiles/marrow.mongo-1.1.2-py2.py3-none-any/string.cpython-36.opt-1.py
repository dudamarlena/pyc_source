# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/string.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 739 bytes
from __future__ import unicode_literals
from .base import Field
from ....schema import Attribute
from ....schema.compat import unicode

class String(Field):
    __foreign__ = 'string'
    __disallowed_operators__ = {'#array'}
    strip = Attribute(default=False)
    case = Attribute(default=None)

    def to_foreign(self, obj, name, value):
        value = unicode(value)
        if self.strip is True:
            value = value.strip()
        else:
            if self.strip:
                value = value.strip(self.strip)
            if self.case in (1, True, 'u', 'upper'):
                value = value.upper()
            else:
                if self.case in (-1, False, 'l', 'lower'):
                    value = value.lower()
                elif self.case == 'title':
                    value = value.title()
        return value