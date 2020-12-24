# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/long_.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 265 bytes
from __future__ import unicode_literals
from bson.int64 import Int64
from .number import Number

class Long(Number):
    __foreign__ = 'long'

    def to_foreign(self, obj, name, value):
        return Int64(int(value))