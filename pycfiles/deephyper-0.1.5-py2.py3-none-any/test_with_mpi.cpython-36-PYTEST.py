# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_with_mpi.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 950 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys, subprocess, cloudpickle, base64, pytest
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

def with_mpi(nproc=2, timeout=30, skip_if_no_mpi=True):

    def outer_thunk(fn):

        def thunk(*args, **kwargs):
            serialized_fn = base64.b64encode(cloudpickle.dumps(lambda : fn(*args, **kwargs)))
            subprocess.check_call([
             'mpiexec', '-n', str(nproc),
             sys.executable,
             '-m', 'baselines.common.tests.test_with_mpi',
             serialized_fn],
              env=(os.environ),
              timeout=timeout)

        if skip_if_no_mpi:
            return pytest.mark.skipif((MPI is None), reason='MPI not present')(thunk)
        else:
            return thunk

    return outer_thunk


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fn = cloudpickle.loads(base64.b64decode(sys.argv[1]))
        @py_assert2 = callable(fn)
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_with_mpi.py', lineno=35)
        if not @py_assert2:
            @py_format4 = 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(callable) if 'callable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(callable) else 'callable',  'py1':@pytest_ar._saferepr(fn) if 'fn' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fn) else 'fn',  'py3':@pytest_ar._saferepr(@py_assert2)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert2 = None
        fn()