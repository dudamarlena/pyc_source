# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 853 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from deephyper.search.nas.baselines.common.schedules import ConstantSchedule, PiecewiseSchedule

def test_piecewise_schedule():
    ps = PiecewiseSchedule([
     (-5, 100), (5, 200), (10, 50), (100, 50), (200, -50)],
      outside_value=500)
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 10
    @py_assert8 = -@py_assert6
    @py_assert9 = @py_assert4(@py_assert8)
    @py_assert11 = 500
    @py_assert13 = @py_assert1(@py_assert9, @py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=10)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py10)s\n{%(py10)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(-%(py7)s)\n}, %(py12)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 0
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 150
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=11)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 5
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 200
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=12)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 9
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 80
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=13)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 50
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 50
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=14)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 80
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 50
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=15)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 150
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 0
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=16)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 175
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 25
    @py_assert12 = -@py_assert10
    @py_assert13 = @py_assert1(@py_assert8, @py_assert12)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=17)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, -%(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 201
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 500
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=18)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 500
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 500
    @py_assert12 = @py_assert1(@py_assert8, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=19)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py7)s)\n}, %(py11)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = np.isclose
    @py_assert4 = ps.value
    @py_assert6 = 200
    @py_assert8 = 1e-10
    @py_assert10 = @py_assert6 - @py_assert8
    @py_assert11 = @py_assert4(@py_assert10)
    @py_assert13 = 50
    @py_assert15 = -@py_assert13
    @py_assert16 = @py_assert1(@py_assert11, @py_assert15)
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=21)
    if not @py_assert16:
        @py_format18 = 'assert %(py17)s\n{%(py17)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}((%(py7)s - %(py9)s))\n}, -%(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ps) if 'ps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ps) else 'ps',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_constant_schedule():
    cs = ConstantSchedule(5)
    for i in range(-100, 100):
        @py_assert1 = np.isclose
        @py_assert4 = cs.value
        @py_assert7 = @py_assert4(i)
        @py_assert9 = 5
        @py_assert11 = @py_assert1(@py_assert7, @py_assert9)
        if @py_assert11 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_schedules.py', lineno=27)
        if not @py_assert11:
            @py_format13 = 'assert %(py12)s\n{%(py12)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.value\n}(%(py6)s)\n}, %(py10)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(cs) if 'cs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cs) else 'cs',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None