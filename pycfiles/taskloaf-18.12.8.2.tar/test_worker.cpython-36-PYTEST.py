# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_worker.py
# Compiled at: 2018-03-14 15:42:35
# Size of source mod 2**32: 2770 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest, asyncio, taskloaf.worker
from taskloaf.cluster import cluster
from taskloaf.mpi import mpiexisting, MPIComm, rank
from taskloaf.test_decorators import mpi_procs
from taskloaf.run import run
from fixtures import w
if __name__ == '__main__':
    test_log()

def test_shutdown(w):

    async def f(w):
        taskloaf.worker.shutdown(w)

    w.start(f)


def test_run_work():
    val = [
     0, 1]
    y = 2.0

    async def f(w):

        def g(w, x):
            val[0] = x

        w.run_work(g, y)

    run(f)
    @py_assert0 = val[0]
    @py_assert2 = @py_assert0 == y
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, y)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(y) if 'y' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y) else 'y'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_await_work():
    val = [
     0]

    async def f(w):

        def h(w, x):
            val[0] = x

        S = 'dang'
        await w.wait_for_work(h, S)
        @py_assert0 = val[0]
        @py_assert2 = @py_assert0 == S
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, S)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    run(f)


def test_run_output():

    async def f(w):
        return 1

    @py_assert2 = run(f)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(run) if 'run' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(run) else 'run',  'py1':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_exception():

    async def f(w):

        def count_except(w):
            if not hasattr(w, 'testcounter'):
                w.testcounter = 0
            else:
                w.testcounter += 1
                if w.testcounter % 2:
                    raise Exception('failed task!')
                if w.testcounter > 10:

                    def success(w):
                        w.wait_fut.set_result(None)

                    w.submit_work(0, success)

        for i in range(12):
            w.submit_work(1, count_except)

        w.wait_fut = asyncio.Future()
        await w.wait_fut

    cluster(2, f)


@mpi_procs(2)
def test_remote_work():

    async def f(w):
        if w.addr != 0:
            return

        async def g(w):
            @py_assert1 = w.addr
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.addr\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

            def h(w):
                @py_assert1 = w.addr
                @py_assert4 = 0
                @py_assert3 = @py_assert1 == @py_assert4
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.addr\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None
                taskloaf.worker.shutdown(w)

            w.submit_work(0, h)
            taskloaf.worker.shutdown(w)

        w.submit_work(1, g)
        while True:
            await asyncio.sleep(0)

    cluster(2, f, runner=mpiexisting)


def test_cluster_output():

    async def f(w):
        return 1

    @py_assert1 = 1
    @py_assert4 = cluster(@py_assert1, f)
    @py_assert7 = 1
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(cluster) if 'cluster' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cluster) else 'cluster',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


class FunnyException(Exception):
    pass


@mpi_procs(2)
def test_cluster_death_cleansup():

    def check(n, onoff):
        for i in range(n):
            path = '/dev/shm/taskloaf_' + str(i) + '_0'
            @py_assert1 = os.path
            @py_assert3 = @py_assert1.exists
            @py_assert6 = @py_assert3(path)
            @py_assert8 = @py_assert6 == onoff
            if not @py_assert8:
                @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py5)s)\n} == %(py9)s', ), (@py_assert6, onoff)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(onoff) if 'onoff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(onoff) else 'onoff'}
                @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None

    async def f(w):
        ptr = w.allocator.malloc(1)
        check(1, True)
        raise FunnyException()

    check(2, False)
    raises = False
    try:
        cluster(2, f, runner=mpiexisting)
    except FunnyException as e:
        raises = True

    @py_assert1 = []
    @py_assert3 = rank()
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    @py_assert0 = @py_assert5
    if not @py_assert5:
        @py_assert0 = raises
    if not @py_assert0:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2':@pytest_ar._saferepr(rank) if 'rank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rank) else 'rank',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = '%(py9)s' % {'py9': @py_format8}
        @py_assert1.append(@py_format10)
        if not @py_assert5:
            @py_format12 = '%(py11)s' % {'py11': @pytest_ar._saferepr(raises) if 'raises' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raises) else 'raises'}
            @py_assert1.append(@py_format12)
        @py_format13 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    import gc
    gc.collect()
    check(2, False)