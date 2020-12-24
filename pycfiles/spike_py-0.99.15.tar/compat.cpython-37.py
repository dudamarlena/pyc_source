# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/compat.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 1442 bytes
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