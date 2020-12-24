# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/regex.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 172 bytes
from __future__ import unicode_literals
from .string import String

class Regex(String):
    __foreign__ = 'regex'
    __disallowed_operators__ = {'#array'}