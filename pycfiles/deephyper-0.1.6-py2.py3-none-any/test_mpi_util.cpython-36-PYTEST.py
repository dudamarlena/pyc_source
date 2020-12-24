# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/test_mpi_util.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1006 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from deephyper.search.nas.baselines import logger
from deephyper.search.nas.baselines.common.tests.test_with_mpi import with_mpi
from deephyper.search.nas.baselines.common import mpi_util

@with_mpi()
def test_mpi_weighted_mean():
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    with logger.scoped_configure(comm=comm):
        if comm.rank == 0:
            name2valcount = {'a':(10, 2), 
             'b':(20, 3)}
        else:
            if comm.rank == 1:
                name2valcount = {'a':(19, 1), 
                 'c':(42, 3)}
            else:
                raise NotImplementedError
        d = mpi_util.mpi_weighted_mean(comm, name2valcount)
        correctval = {'a':13.0,  'b':20,  'c':42}
        if comm.rank == 0:
            @py_assert1 = d == correctval
            if @py_assert1 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/test_mpi_util.py', lineno=21)
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (d, correctval)) % {'py0':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py2':@pytest_ar._saferepr(correctval) if 'correctval' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(correctval) else 'correctval'}
                @py_format5 = (@pytest_ar._format_assertmsg('{} != {}'.format(d, correctval)) + '\n>assert %(py4)s') % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None
        for name, (val, count) in name2valcount.items():
            for _ in range(count):
                logger.logkv_mean(name, val)

        d2 = logger.dumpkvs()
        if comm.rank == 0:
            @py_assert1 = d2 == correctval
            if @py_assert1 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/test_mpi_util.py', lineno=28)
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (d2, correctval)) % {'py0':@pytest_ar._saferepr(d2) if 'd2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d2) else 'd2',  'py2':@pytest_ar._saferepr(correctval) if 'correctval' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(correctval) else 'correctval'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None