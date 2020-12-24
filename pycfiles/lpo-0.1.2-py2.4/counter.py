# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lpo/counter.py
# Compiled at: 2008-07-30 12:52:46
from sqlalchemy import orm
import tables as ta

class Counter(object):
    """
    """
    __module__ = __name__

    def __init__(self, name, start=0, algo=None):
        self.name = name
        self.count = start
        if algo is None:
            algo = lambda x: x + 1
        self.algo = algo
        return

    def __call__(self, count=None):
        if count is None:
            self.count = self.algo(self.count)
        else:
            self.count = count
        return self.count

    def reset(self, start=0):
        self.count = start


orm.mapper(Counter, ta.counters)