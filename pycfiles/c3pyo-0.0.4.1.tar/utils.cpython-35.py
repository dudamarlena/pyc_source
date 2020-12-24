# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Documents/Projects/C3PyO/c3pyo/utils.py
# Compiled at: 2016-10-20 03:13:45
# Size of source mod 2**32: 209 bytes
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def is_iterable(x):
    if isinstance(x, list) or isinstance(x, set) or isinstance(x, tuple):
        return True
    else:
        return False