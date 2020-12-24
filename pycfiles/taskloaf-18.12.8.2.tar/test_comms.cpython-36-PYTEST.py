# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_comms.py
# Compiled at: 2018-03-30 16:02:19
# Size of source mod 2**32: 2073 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, cloudpickle
from multiprocessing import Process, Queue
from mpi4py import MPI
from taskloaf.local import LocalComm
from taskloaf.mpi import MPIComm
from taskloaf.zmq import ZMQComm, zmqrun
from taskloaf.test_decorators import mpi_procs
test_cfg = dict()

def queue_test_helper(q):
    q.put(123)


def test_queue():
    q = Queue()
    p = Process(target=queue_test_helper, args=(q,))
    p.start()
    @py_assert1 = q.get
    @py_assert3 = @py_assert1()
    @py_assert6 = 123
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(q) if 'q' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(q) else 'q',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    p.join()


def test_local_comm():
    qs = [
     Queue(), Queue()]
    c0 = LocalComm(qs, 0)
    c1 = LocalComm(qs, 1)
    c0.send(1, cloudpickle.dumps(456))
    go = True
    while go:
        val = c1.recv()
        if val is not None:
            @py_assert1 = cloudpickle.loads
            @py_assert4 = @py_assert1(val)
            @py_assert7 = 456
            @py_assert6 = @py_assert4 == @py_assert7
            if not @py_assert6:
                @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loads\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(cloudpickle) if 'cloudpickle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cloudpickle) else 'cloudpickle',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
            go = False


def test_empty_recv():
    c = MPIComm()
    @py_assert1 = c.recv
    @py_assert3 = @py_assert1()
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.recv\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_tcp():
    pass


def wait_for(c, val, get=lambda x: x):
    stop = False
    while not stop:
        msg = c.recv()
        if msg is not None:
            @py_assert1 = cloudpickle.loads
            @py_assert4 = @py_assert1(msg)
            @py_assert9 = get(val)
            @py_assert6 = @py_assert4 == @py_assert9
            if not @py_assert6:
                @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loads\n}(%(py3)s)\n} == %(py10)s\n{%(py10)s = %(py7)s(%(py8)s)\n}', ), (@py_assert4, @py_assert9)) % {'py0':@pytest_ar._saferepr(cloudpickle) if 'cloudpickle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cloudpickle) else 'cloudpickle',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(get) if 'get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get) else 'get',  'py8':@pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val',  'py10':@pytest_ar._saferepr(@py_assert9)}
                @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = None
        stop = True


def test_zmq():
    n_workers = 4
    leader = 1

    def f(c):
        if c.addr == leader:
            for i in range(n_workers):
                if i == c.addr:
                    pass
                else:
                    c.send(i, cloudpickle.dumps('OHI!'))

            for i in range(n_workers - 1):
                wait_for(c, 'OYAY')

        else:
            wait_for(c, 'OHI!')
            c.send(leader, cloudpickle.dumps('OYAY'))
        c.barrier()

    zmqrun(n_workers, f, test_cfg)


def data_send(c):
    if c.addr == 0:
        c.send(1, cloudpickle.dumps(123))
    if c.addr == 1:
        wait_for(c, 123)


def fnc_send(c):
    if c.addr == 0:
        x = 13
        c.send(1, cloudpickle.dumps(lambda : x ** 2))
    if c.addr == 1:
        wait_for(c, 169, lambda x: x())


def test_zmq_data_send():
    zmqrun(2, data_send, test_cfg)


def test_zmq_fnc_send():
    zmqrun(2, fnc_send, test_cfg)


@mpi_procs(2)
def test_zmq_data_send():
    data_send(MPIComm())


@mpi_procs(2)
def test_zmq_fnc_send():
    fnc_send(MPIComm())