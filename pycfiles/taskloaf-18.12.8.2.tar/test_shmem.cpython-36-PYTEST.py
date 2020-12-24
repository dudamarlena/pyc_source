# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_shmem.py
# Compiled at: 2018-02-01 00:20:10
# Size of source mod 2**32: 2646 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, time, numpy as np, multiprocessing
from taskloaf.shmem import alloc_shmem, Shmem
from taskloaf.timer import Timer

def sum_shmem(filepath):
    with Shmem(filepath) as (sm):
        return np.sum(np.frombuffer(sm.mem))


def test_shmem():
    A = np.random.rand(100)
    with alloc_shmem(A.nbytes, 'test') as (filepath):
        with Shmem(filepath) as (sm):
            sm.mem[:] = A.data.cast('B')
            out = multiprocessing.Pool(1).map(sum_shmem, [sm.filepath])[0]
            @py_assert4 = sm.filepath
            @py_assert6 = sum_shmem(@py_assert4)
            @py_assert1 = out == @py_assert6
            if not @py_assert1:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py2)s(%(py5)s\n{%(py5)s = %(py3)s.filepath\n})\n}', ), (out, @py_assert6)) % {'py0':@pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out',  'py2':@pytest_ar._saferepr(sum_shmem) if 'sum_shmem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sum_shmem) else 'sum_shmem',  'py3':@pytest_ar._saferepr(sm) if 'sm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sm) else 'sm',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert4 = @py_assert6 = None


def shmem_zeros(filepath):
    with Shmem(filepath) as (sm):
        np.frombuffer(sm.mem)[:] = 0


def test_shmem_edit():
    A = np.random.rand(100)
    with alloc_shmem(A.nbytes, 'test') as (filepath):
        with Shmem(filepath) as (sm):
            sm.mem[:] = A.data.cast('B')
            out = multiprocessing.Pool(1).map(shmem_zeros, [sm.filepath])[0]
            np.testing.assert_almost_equal(np.frombuffer(sm.mem), 0.0)


def benchmark_shmem():
    t = Timer()
    A = np.random.rand(int(100000000.0)) - 0.5
    t.report('build A')
    print('sum', np.sum(A))
    t.report('sum')
    b = A.copy()
    t.report('baseline copy')
    with alloc_shmem(A) as (sm):
        t.report('alloc fillled shmem')
        del sm.mem
    t.restart()
    with alloc_shmem(A.nbytes) as (sm):
        f = open((sm.fd), 'r+b', closefd=False)
        f.seek(0)
        f.write(A)
        f.close()
        t.report('alloc empty, write to file')
        del sm.mem
    t.restart()
    with alloc_shmem(A.nbytes) as (sm):
        np.frombuffer(sm.mem)[:] = A
        t.report('alloc empty shmem and fill')
        del sm.mem
    with alloc_shmem(A) as (sm):
        t.restart()
        print('sum2', np.sum(np.frombuffer(sm.mem)))
        t.report('read and sum')
        del sm.mem


if __name__ == '__main__':
    benchmark_shmem()