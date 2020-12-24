# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/pkg/superjson/pkg/dateutil/_common.py
# Compiled at: 2018-12-19 11:16:55
__doc__ = '\nCommon code used in multiple modules.\n'

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