# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_promise.py
# Compiled at: 2018-03-09 12:22:55
# Size of source mod 2**32: 2853 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, numpy as np
from taskloaf.promise import *
from taskloaf.test_decorators import mpi_procs
from taskloaf.run import null_comm_worker
from taskloaf.cluster import cluster

def test_task():

    async def f(w):
        w.abc = 0

        def here(w):
            w.abc = 1

        await task(w, here)
        @py_assert1 = w.abc
        @py_assert4 = 1
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.abc\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

        def here_args(w, x):
            w.abc = x

        await task(w, here_args, 17)
        @py_assert1 = w.abc
        @py_assert4 = 17
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.abc\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

        def there(w):
            @py_assert1 = w.addr
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.addr\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
            return 13

        @py_assert0 = await task(w, there, to=1)
        @py_assert3 = 13
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        thirteen = taskloaf.serialize.dumps(w, 13)

        def there2(w):
            @py_assert1 = w.addr
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.addr\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
            return thirteen

        @py_assert0 = await task(w, there2, to=1)
        @py_assert2 = @py_assert0 == thirteen
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, thirteen)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(thirteen) if 'thirteen' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(thirteen) else 'thirteen'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        there_ref = put(w, there)
        @py_assert0 = await task(w, there_ref, to=1)
        @py_assert3 = 13
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

        def f_with_args(w, a):
            return a

        f_ref = put(w, f_with_args)
        @py_assert0 = await task(w, f_ref, 14, to=1)
        @py_assert3 = 14
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        a_ref = put(w, 15)
        @py_assert0 = await task(w, f_ref, a_ref, to=1)
        @py_assert3 = 15
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    cluster(2, f)


def test_task_await_elsewhere():

    async def f(w):

        def g(w):
            return 71

        pr = task(w, g, to=1)

        async def h(w):
            a = await pr
            return a + 1

        pr2 = task(w, h, to=2)
        @py_assert0 = await pr2
        @py_assert3 = 72
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    cluster(3, f)


class Implosion(Exception):
    pass


def test_task_exception():

    async def f(w):

        def g(w):
            raise Implosion()

        with pytest.raises(Implosion):
            await task(w, g)
        with pytest.raises(Implosion):
            await task(w, g, to=1)

    cluster(2, f)


def test_then():

    async def f(w):
        y = await task(w, (lambda w: 10), to=1).then((lambda w, x: 2 * x), to=0)
        @py_assert2 = 20
        @py_assert1 = y == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (y, @py_assert2)) % {'py0':@pytest_ar._saferepr(y) if 'y' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y) else 'y',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    cluster(2, f)


def test_auto_unwrap():

    async def f(w):
        y = await task(w, (lambda w: 10), to=1).then((lambda w, x: task(w, lambda w: 2 * x)),
          to=0)
        @py_assert2 = 20
        @py_assert1 = y == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (y, @py_assert2)) % {'py0':@pytest_ar._saferepr(y) if 'y' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y) else 'y',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    cluster(2, f)


def test_when_all():

    async def f(w):
        y = await when_all([
         task(w, lambda w: 10),
         task(w, (lambda w: 5), to=1)]).then((lambda w, x: sum(x)),
          to=1)
        @py_assert2 = 15
        @py_assert1 = y == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (y, @py_assert2)) % {'py0':@pytest_ar._saferepr(y) if 'y' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y) else 'y',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    cluster(2, f)