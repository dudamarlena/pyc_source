# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/acktr/running_stat.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 1320 bytes
import numpy as np

class RunningStat(object):

    def __init__(self, shape):
        self._n = 0
        self._M = np.zeros(shape)
        self._S = np.zeros(shape)

    def push(self, x):
        x = np.asarray(x)
        assert x.shape == self._M.shape
        self._n += 1
        if self._n == 1:
            self._M[...] = x
        else:
            oldM = self._M.copy()
            self._M[...] = oldM + (x - oldM) / self._n
            self._S[...] = self._S + (x - oldM) * (x - self._M)

    @property
    def n(self):
        return self._n

    @property
    def mean(self):
        return self._M

    @property
    def var(self):
        if self._n > 1:
            return self._S / (self._n - 1)
        return np.square(self._M)

    @property
    def std(self):
        return np.sqrt(self.var)

    @property
    def shape(self):
        return self._M.shape


def test_running_stat():
    for shp in ((), (3, ), (3, 4)):
        li = []
        rs = RunningStat(shp)
        for _ in range(5):
            val = np.random.randn(*shp)
            rs.push(val)
            li.append(val)
            m = np.mean(li, axis=0)
            assert np.allclose(rs.mean, m)
            v = np.square(m) if len(li) == 1 else np.var(li, ddof=1, axis=0)
            if not np.allclose(rs.var, v):
                raise AssertionError