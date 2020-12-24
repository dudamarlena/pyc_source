# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/ttl.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 710 bytes
from __future__ import unicode_literals
from datetime import datetime, timedelta
from numbers import Number
from .date import Date
from ...util import utcnow

class TTL(Date):
    __doc__ = 'A specialized Date field used to store dates in the future by timedelta from now.'
    __foreign__ = 'date'
    __disallowed_operators__ = {'#array'}

    def to_foreign(self, obj, name, value):
        if isinstance(value, timedelta):
            value = utcnow() + value
        else:
            if isinstance(value, datetime):
                value = value
            else:
                if isinstance(value, Number):
                    value = utcnow() + timedelta(days=value)
                else:
                    raise ValueError('Invalid TTL value: ' + repr(value))
        return super(TTL, self).to_foreign(obj, name, value)