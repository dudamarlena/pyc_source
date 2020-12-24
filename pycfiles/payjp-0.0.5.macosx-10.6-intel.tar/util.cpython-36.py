# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/payjp/util.py
# Compiled at: 2018-06-22 02:45:13
# Size of source mod 2**32: 179 bytes
import sys

def utf8(value):
    if sys.version_info < (3, 0):
        if isinstance(value, unicode):
            return value.encode('utf-8')
    return value