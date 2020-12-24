# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/mpi_running_mean_std.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3981 bytes
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

import tensorflow as tf, deephyper.search.nas.baselines.common.tf_util as U, numpy as np

class RunningMeanStd(object):

    def __init__(self, epsilon=0.01, shape=()):
        self._sum = tf.get_variable(dtype=(tf.float64),
          shape=shape,
          initializer=(tf.constant_initializer(0.0)),
          name='runningsum',
          trainable=False)
        self._sumsq = tf.get_variable(dtype=(tf.float64),
          shape=shape,
          initializer=(tf.constant_initializer(epsilon)),
          name='runningsumsq',
          trainable=False)
        self._count = tf.get_variable(dtype=(tf.float64),
          shape=(),
          initializer=(tf.constant_initializer(epsilon)),
          name='count',
          trainable=False)
        self.shape = shape
        self.mean = tf.to_float(self._sum / self._count)
        self.std = tf.sqrt(tf.maximum(tf.to_float(self._sumsq / self._count) - tf.square(self.mean), 0.01))
        newsum = tf.placeholder(shape=(self.shape), dtype=(tf.float64), name='sum')
        newsumsq = tf.placeholder(shape=(self.shape),
          dtype=(tf.float64),
          name='var')
        newcount = tf.placeholder(shape=[], dtype=(tf.float64), name='count')
        self.incfiltparams = U.function([newsum, newsumsq, newcount], [], updates=[
         tf.assign_add(self._sum, newsum),
         tf.assign_add(self._sumsq, newsumsq),
         tf.assign_add(self._count, newcount)])

    def update(self, x):
        x = x.astype('float64')
        n = int(np.prod(self.shape))
        totalvec = np.zeros(n * 2 + 1, 'float64')
        addvec = np.concatenate([x.sum(axis=0).ravel(),
         np.square(x).sum(axis=0).ravel(), np.array([len(x)], dtype='float64')])
        if MPI is not None:
            MPI.COMM_WORLD.Allreduce(addvec, totalvec, op=(MPI.SUM))
        self.incfiltparams(totalvec[0:n].reshape(self.shape), totalvec[n:2 * n].reshape(self.shape), totalvec[(2 * n)])


@U.in_session
def test_runningmeanstd():
    for x1, x2, x3 in [
     (
      np.random.randn(3), np.random.randn(4), np.random.randn(5)),
     (
      np.random.randn(3, 2), np.random.randn(4, 2), np.random.randn(5, 2))]:
        rms = RunningMeanStd(epsilon=0.0, shape=(x1.shape[1:]))
        U.initialize()
        x = np.concatenate([x1, x2, x3], axis=0)
        ms1 = [x.mean(axis=0), x.std(axis=0)]
        rms.update(x1)
        rms.update(x2)
        rms.update(x3)
        ms2 = [rms.mean.eval(), rms.std.eval()]
        assert np.allclose(ms1, ms2)


@U.in_session
def test_dist():
    np.random.seed(0)
    p1, p2, p3 = np.random.randn(3, 1), np.random.randn(4, 1), np.random.randn(5, 1)
    q1, q2, q3 = np.random.randn(6, 1), np.random.randn(7, 1), np.random.randn(8, 1)
    comm = MPI.COMM_WORLD
    assert comm.Get_size() == 2
    if comm.Get_rank() == 0:
        x1, x2, x3 = p1, p2, p3
    else:
        if comm.Get_rank() == 1:
            x1, x2, x3 = q1, q2, q3
        else:
            assert False
            rms = RunningMeanStd(epsilon=0.0, shape=(1, ))
            U.initialize()
            rms.update(x1)
            rms.update(x2)
            rms.update(x3)
            bigvec = np.concatenate([p1, p2, p3, q1, q2, q3])

            def checkallclose(x, y):
                print(x, y)
                return np.allclose(x, y)

            assert checkallclose(bigvec.mean(axis=0), rms.mean.eval())
        assert checkallclose(bigvec.std(axis=0), rms.std.eval())


if __name__ == '__main__':
    test_dist()