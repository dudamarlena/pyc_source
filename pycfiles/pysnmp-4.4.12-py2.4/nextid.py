# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/nextid.py
# Compiled at: 2019-08-18 17:24:05
import random
random.seed()

class Integer(object):
    """Return a next value in a reasonably MT-safe manner"""
    __module__ = __name__

    def __init__(self, maximum, increment=256):
        self.__maximum = maximum
        if increment >= maximum:
            increment = maximum
        self.__increment = increment
        self.__threshold = increment // 2
        e = random.randrange(self.__maximum - self.__increment)
        self.__bank = list(range(e, e + self.__increment))

    def __repr__(self):
        return '%s(%d, %d)' % (self.__class__.__name__, self.__maximum, self.__increment)

    def __call__(self):
        v = self.__bank.pop(0)
        if v % self.__threshold:
            return v
        else:
            e = self.__bank[(-1)] + 1
            if e > self.__maximum:
                e = 0
            self.__bank.extend(range(e, e + self.__threshold))
            return v