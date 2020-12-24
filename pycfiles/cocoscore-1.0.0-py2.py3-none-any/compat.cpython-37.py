# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\compat.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2135 bytes
from __future__ import division, print_function, unicode_literals
import six
if six.PY3:

    def asciibytes(s):
        return bytes(s, 'ASCII')


else:

    def asciibytes(s):
        if type(s) != bytes:
            s = s.encode('ASCII')
        return s