# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chibiegg/.pyenv/versions/cloudbackup/lib/python3.4/site-packages/cloudbackup/progressbar/compat.py
# Compiled at: 2014-12-28 14:20:28
# Size of source mod 2**32: 1460 bytes
"""Compatibility methods and classes for the progressbar module."""
try:
    next
except NameError:

    def next(iter):
        try:
            return iter.__next__()
        except AttributeError:
            return iter.next()


try:
    any
except NameError:

    def any(iterator):
        for item in iterator:
            if item:
                return True

        return False