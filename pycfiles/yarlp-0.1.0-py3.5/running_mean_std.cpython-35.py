# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/common/running_mean_std.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 1618 bytes
import numpy as np

class RunningMeanStd(object):

    def __init__(self, epsilon=0.0001, shape=()):
        self.mean = np.zeros(shape, 'float64')
        self.var = np.ones(shape, 'float64')
        self.count = epsilon

    def update(self, x):
        batch_mean = np.mean(x, axis=0)
        batch_var = np.var(x, axis=0)
        batch_count = x.shape[0]
        self.update_from_moments(batch_mean, batch_var, batch_count)

    def update_from_moments(self, batch_mean, batch_var, batch_count):
        delta = batch_mean - self.mean
        tot_count = self.count + batch_count
        new_mean = self.mean + delta * batch_count / tot_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        M2 = m_a + m_b + np.square(delta) * self.count * batch_count / (self.count + batch_count)
        new_var = M2 / (self.count + batch_count)
        new_count = batch_count + self.count
        self.mean = new_mean
        self.var = new_var
        self.count = new_count


def test_runningmeanstd():
    for x1, x2, x3 in [
     (
      np.random.randn(3), np.random.randn(4), np.random.randn(5)),
     (
      np.random.randn(3, 2), np.random.randn(4, 2), np.random.randn(5, 2))]:
        rms = RunningMeanStd(epsilon=0.0, shape=x1.shape[1:])
        x = np.concatenate([x1, x2, x3], axis=0)
        ms1 = [x.mean(axis=0), x.var(axis=0)]
        rms.update(x1)
        rms.update(x2)
        rms.update(x3)
        ms2 = [rms.mean, rms.var]
        if not np.allclose(ms1, ms2):
            raise AssertionError