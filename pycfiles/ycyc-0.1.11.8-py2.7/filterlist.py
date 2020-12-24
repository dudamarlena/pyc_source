# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/ycollections/filterlist.py
# Compiled at: 2016-03-30 08:43:32
from collections import deque

class FilterList(deque):

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def filter(self, func):
        """
        Return a new FilterList which filter by func
        """
        return self.__class__(filter(func, self))

    def exclude(self, func):
        """
        Return a new FilterList which exclude by func
        """
        return self.filter(lambda x: not func(x))

    def first(self, default=None):
        """
        Return the first item if existed, otherwise return default
        """
        if self:
            return self[0]
        return default

    def last(self, default=None):
        """
        Return the last item if existed, otherwise return default
        """
        if self:
            return self[(-1)]
        return default