# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/iterator.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Iterator']
__authors__ = ['Tim Chow']

class Iterator(object):

    def __init__(self, it):
        self._it = it
        self._cursor = 0

    def has_next(self):
        return self._cursor < len(self._it)

    def next(self):
        try:
            return self._it[self._cursor]
        finally:
            self._cursor = self._cursor + 1

    def remove(self):
        try:
            return self._it.pop(self._cursor - 1)
        finally:
            self._cursor = self._cursor - 1