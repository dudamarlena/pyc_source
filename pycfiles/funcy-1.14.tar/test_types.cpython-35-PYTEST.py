# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_types.py
# Compiled at: 2014-03-21 04:56:57
# Size of source mod 2**32: 442 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from funcy.cross import xrange
from funcy.types import *

def test_iterable():
    @py_assert1 = []
    @py_assert3 = iterable(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = {}
    @py_assert3 = iterable(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = 'abc'
    @py_assert3 = iterable(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = []
    @py_assert4 = iter(@py_assert2)
    @py_assert6 = iterable(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = (x for x in range(10))
    @py_assert3 = iterable(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = 10
    @py_assert4 = xrange(@py_assert2)
    @py_assert6 = iterable(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(xrange) if 'xrange' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(xrange) else 'xrange', 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = iterable(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(iterable) if 'iterable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterable) else 'iterable'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_is_iter():
    @py_assert2 = []
    @py_assert4 = iter(@py_assert2)
    @py_assert6 = is_iter(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(is_iter) if 'is_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_iter) else 'is_iter'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = (x for x in range(10))
    @py_assert3 = is_iter(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(is_iter) if 'is_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_iter) else 'is_iter'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = []
    @py_assert3 = is_iter(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(is_iter) if 'is_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_iter) else 'is_iter'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = 10
    @py_assert4 = xrange(@py_assert2)
    @py_assert6 = is_iter(@py_assert4)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(xrange) if 'xrange' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(xrange) else 'xrange', 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(is_iter) if 'is_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_iter) else 'is_iter'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None