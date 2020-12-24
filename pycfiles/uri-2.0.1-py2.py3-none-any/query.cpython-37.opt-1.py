# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/part/query.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 510 bytes
from __future__ import unicode_literals
from ..compat import str
from ..qso import QSO
from .base import ProxyPart

class QueryPart(ProxyPart):
    attribute = '_query'
    prefix = '?'
    terminator = '#'
    cast = QSO

    def __get__(self, obj, cls=None):
        result = super(QueryPart, self).__get__(obj, cls)
        if result is None:
            result = obj._query = QSO()
        return result

    def __set__(self, obj, value):
        if value is None:
            value = ''
        super(QueryPart, self).__set__(obj, value)