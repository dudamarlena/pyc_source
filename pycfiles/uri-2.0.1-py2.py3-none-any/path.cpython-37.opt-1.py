# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/part/path.py
# Compiled at: 2018-10-31 09:19:39
# Size of source mod 2**32: 937 bytes
from __future__ import unicode_literals
from re import compile as r
from .base import ProxyPart
from ..compat import Path, str

class PathPart(ProxyPart):
    attribute = '_path'
    cast = Path
    empty = '/'

    def __get__(self, obj, cls=None):
        value = super(PathPart, self).__get__(obj, cls)
        if value is None:
            value = Path()
            obj._trailing = False
        return value

    def __set__(self, obj, value):
        value = str(value)
        obj._trailing = value.endswith('/')
        if obj.authority:
            if not value.startswith('/'):
                raise ValueError('Can only assign rooted paths to URI with authority.')
        super(PathPart, self).__set__(obj, value)

    def render(self, obj, value):
        result = super(PathPart, self).render(obj, value)
        if result is None or result == '.':
            if not obj._host:
                return ''
            return self.empty
        if obj._trailing:
            if not result.endswith('/'):
                result += '/'
        return result