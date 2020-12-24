# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_funcmakers.py
# Compiled at: 2018-10-03 08:49:11
# Size of source mod 2**32: 993 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from collections import defaultdict
import pytest
from funcy.funcmakers import *

def test_callable():
    @py_assert1 = lambda x: x + 42
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = 0
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 42
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=8)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_int():
    @py_assert1 = 0
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = 'abc'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 'a'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=12)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 2
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = [
     1, 2, 3]
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=13)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 1
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = {1: 'a'}
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 'a'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=14)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    with pytest.raises(IndexError):
        make_func(1)('a')
    with pytest.raises(TypeError):
        make_func(1)(42)


def test_slice():
    @py_assert2 = 1
    @py_assert4 = None
    @py_assert6 = slice(@py_assert2, @py_assert4)
    @py_assert8 = make_func(@py_assert6)
    @py_assert10 = 'abc'
    @py_assert12 = @py_assert8(@py_assert10)
    @py_assert15 = 'bc'
    @py_assert14 = @py_assert12 == @py_assert15
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=20)
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n}(%(py11)s)\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(slice) if 'slice' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(slice) else 'slice', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_str():
    @py_assert1 = '\\d+'
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = 'ab42c'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = '42'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=24)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '\\d+'
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = 'abc'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=25)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '\\d+'
    @py_assert3 = make_pred(@py_assert1)
    @py_assert5 = 'ab42c'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = True
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=26)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_pred) if 'make_pred' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_pred) else 'make_pred', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '\\d+'
    @py_assert3 = make_pred(@py_assert1)
    @py_assert5 = 'abc'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = False
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=27)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_pred) if 'make_pred' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_pred) else 'make_pred', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_dict():
    @py_assert1 = {1: 'a'}
    @py_assert3 = make_func(@py_assert1)
    @py_assert5 = 1
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 'a'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=31)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    with pytest.raises(KeyError):
        make_func({1: 'a'})(2)
    d = defaultdict(int, a=42)
    @py_assert2 = make_func(d)
    @py_assert4 = 'a'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = 42
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=35)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = make_func(d)
    @py_assert4 = 'b'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=36)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_set():
    s = set([1, 2, 3])
    @py_assert2 = make_func(s)
    @py_assert4 = 1
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = True
    @py_assert8 = @py_assert6 is @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=41)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = make_func(s)
    @py_assert4 = 4
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_funcmakers.py', lineno=42)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(make_func) if 'make_func' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_func) else 'make_func', 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None