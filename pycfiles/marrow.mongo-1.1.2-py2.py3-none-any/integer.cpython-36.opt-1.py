# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/integer.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 234 bytes
from __future__ import unicode_literals
from .number import Number

class Integer(Number):
    __foreign__ = 'integer'

    def to_foreign(self, obj, name, value):
        return int(value)