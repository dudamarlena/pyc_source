# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/boolean.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 544 bytes
from __future__ import unicode_literals
from .base import Field

class Boolean(Field):
    __foreign__ = 'bool'
    __disallowed_operators__ = {'#array'}

    def to_foreign(self, obj, name, value):
        try:
            value = value.lower()
        except AttributeError:
            return bool(value)
        else:
            if value in ('true', 't', 'yes', 'y', 'on', '1', True):
                return True
            if value in ('false', 'f', 'no', 'n', 'off', '0', False):
                return False
            raise ValueError('Unknown or non-boolean value: ' + value)