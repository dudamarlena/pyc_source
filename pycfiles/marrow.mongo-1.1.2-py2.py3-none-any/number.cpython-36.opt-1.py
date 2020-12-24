# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/number.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 516 bytes
from __future__ import unicode_literals
from numbers import Number as NumberABC
from .base import Field
from ....schema.compat import unicode

class Number(Field):
    __foreign__ = 'number'
    __disallowed_operators__ = {'#array'}

    def to_foreign(self, obj, name, value):
        if isinstance(value, NumberABC):
            return value
        else:
            if isinstance(value, unicode):
                if value.isnumeric():
                    return int(value)
                else:
                    return float(value)
            return int(value)