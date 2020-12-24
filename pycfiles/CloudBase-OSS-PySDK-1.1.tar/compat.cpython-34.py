# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chibiegg/.pyenv/versions/cloudbackup/lib/python3.4/site-packages/cloudbackup/progressbar/compat.py
# Compiled at: 2014-12-28 14:20:28
# Size of source mod 2**32: 1460 bytes
__doc__ = 'Compatibility methods and classes for the progressbar module.'
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