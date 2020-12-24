# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: superjson/pkg/dateutil/_common.py
# Compiled at: 2019-04-10 22:47:40
"""
Common code used in multiple modules.
"""

class weekday(object):
    __slots__ = [
     'weekday', 'n']

    def __init__(self, weekday, n=None):
        self.weekday = weekday
        self.n = n

    def __call__(self, n):
        if n == self.n:
            return self
        else:
            return self.__class__(self.weekday, n)

    def __eq__(self, other):
        try:
            if self.weekday != other.weekday or self.n != other.n:
                return False
        except AttributeError:
            return False

        return True

    __hash__ = None

    def __repr__(self):
        s = ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')[self.weekday]
        if not self.n:
            return s
        else:
            return '%s(%+d)' % (s, self.n)