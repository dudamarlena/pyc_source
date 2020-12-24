# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/cryptorandom/prng.py
# Compiled at: 2016-10-21 13:39:48
from __future__ import division
import numpy as np

class lcgRandom:

    def __init__(self, seed=1234567890, A=0, B=65539, M=2147483648):
        self.state = seed
        self.A = A
        self.B = B
        self.M = M

    def getState(self):
        return (
         self.state, self.A, self.B, self.M)

    def setState(self, seed=1234567890, A=0, B=65539, M=2147483648):
        self.state = seed
        self.A = A
        self.B = B
        self.M = M

    def nextRandom(self):
        self.state = (self.A + self.B * self.state) % self.M
        return self.state / self.M

    def random(self, size=None):
        if size == None:
            return self.nextRandom()
        else:
            return np.reshape(np.array([ self.nextRandom() for i in np.arange(np.prod(size)) ]), size)
            return

    def randint(self, low=0, high=None, size=None):
        if high == None:
            high, low = low, 0
        if size == None:
            return low + np.floor(self.nextRandom() * (high - low))
        else:
            return low + np.floor(self.random(size=size) * (high - low))
            return


def _int32(x):
    return int(4294967295 & x)


class MT19937:

    def __init__(self, seed):
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[(i - 1)] ^ self.mt[(i - 1)] >> 30) + i)

    def random(self, size=None):
        if size == None:
            return self.nextRandom()
        else:
            return np.reshape(np.array([ self.nextRandom() for i in np.arange(np.prod(size)) ]), size)
            return

    def nextRandom(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.index = self.index + 1
        return _int32(y)

    def twist(self):
        for i in range(624):
            y = _int32((self.mt[i] & 2147483648) + (self.mt[((i + 1) % 624)] & 2147483647))
            self.mt[i] = self.mt[((i + 397) % 624)] ^ y >> 1
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 2567483615

        self.index = 0