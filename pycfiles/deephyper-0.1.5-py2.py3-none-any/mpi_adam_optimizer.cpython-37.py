# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/mpi_adam_optimizer.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3292 bytes
import numpy as np, tensorflow as tf
import deephyper.search.nas.baselines.common as U
from deephyper.search.nas.baselines.common.tests.test_with_mpi import with_mpi
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

class MpiAdamOptimizer(tf.train.AdamOptimizer):
    __doc__ = 'Adam optimizer that averages gradients across mpi processes.'

    def __init__(self, comm, **kwargs):
        self.comm = comm
        (tf.train.AdamOptimizer.__init__)(self, **kwargs)

    def compute_gradients(self, loss, var_list, **kwargs):
        grads_and_vars = (tf.train.AdamOptimizer.compute_gradients)(self, loss, var_list, **kwargs)
        grads_and_vars = [(g, v) for g, v in grads_and_vars if g is not None]
        flat_grad = tf.concat([tf.reshape(g, (-1, )) for g, v in grads_and_vars], axis=0)
        shapes = [v.shape.as_list() for g, v in grads_and_vars]
        sizes = [int(np.prod(s)) for s in shapes]
        num_tasks = self.comm.Get_size()
        buf = np.zeros(sum(sizes), np.float32)
        countholder = [0]
        stat = tf.reduce_sum(grads_and_vars[0][1])

        def _collect_grads(flat_grad, np_stat):
            self.comm.Allreduce(flat_grad, buf, op=(MPI.SUM))
            np.divide(buf, (float(num_tasks)), out=buf)
            if countholder[0] % 100 == 0:
                check_synced(np_stat, self.comm)
            countholder[0] += 1
            return buf

        avg_flat_grad = tf.py_func(_collect_grads, [flat_grad, stat], tf.float32)
        avg_flat_grad.set_shape(flat_grad.shape)
        avg_grads = tf.split(avg_flat_grad, sizes, axis=0)
        avg_grads_and_vars = [(tf.reshape(g, v.shape), v) for g, (_, v) in zip(avg_grads, grads_and_vars)]
        return avg_grads_and_vars


def check_synced(localval, comm=None):
    """
    It's common to forget to initialize your variables to the same values, or
    (less commonly) if you update them in some other way than adam, to get them out of sync.
    This function checks that variables on all MPI workers are the same, and raises
    an AssertionError otherwise

    Arguments:
        comm: MPI communicator
        localval: list of local variables (list of variables on current worker to be compared with the other workers)
    """
    comm = comm or MPI.COMM_WORLD
    vals = comm.gather(localval)
    if comm.rank == 0:
        assert all((val == vals[0] for val in vals[1:]))


@with_mpi(timeout=5)
def test_nonfreeze():
    np.random.seed(0)
    tf.set_random_seed(0)
    a = tf.Variable(np.random.randn(3).astype('float32'))
    b = tf.Variable(np.random.randn(2, 5).astype('float32'))
    loss = tf.reduce_sum(tf.square(a)) + tf.reduce_sum(tf.sin(b))
    stepsize = 0.01
    config = tf.ConfigProto(inter_op_parallelism_threads=1)
    sess = U.get_session(config=config)
    update_op = MpiAdamOptimizer(comm=(MPI.COMM_WORLD), learning_rate=stepsize).minimize(loss)
    sess.run(tf.global_variables_initializer())
    losslist_ref = []
    for i in range(100):
        l, _ = sess.run([loss, update_op])
        print(i, l)
        losslist_ref.append(l)