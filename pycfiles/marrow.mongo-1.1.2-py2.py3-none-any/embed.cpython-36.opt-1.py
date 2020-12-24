# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/embed.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 417 bytes
from __future__ import unicode_literals
from .base import _HasKind, _CastingKind, Field

class Embed(_HasKind, _CastingKind, Field):
    __foreign__ = 'object'
    __allowed_operators__ = {'#document', '$eq', '#rel'}

    def __init__(self, *args, **kw):
        if args:
            kw['kind'], args = args[0], args[1:]
            kw.setdefault('default', lambda : self._kind()())
        (super(Embed, self).__init__)(*args, **kw)