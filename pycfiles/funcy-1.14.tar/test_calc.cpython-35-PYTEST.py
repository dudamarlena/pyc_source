# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_calc.py
# Compiled at: 2017-08-18 00:10:47
# Size of source mod 2**32: 2750 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from math import sin, cos
import pytest
from funcy.calc import *

def test_memoize():

    @memoize
    def inc(x):
        calls.append(x)
        return x + 1

    calls = []
    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = [0, 1]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = 0
    @py_assert3 = inc(x=@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(x=%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = inc(x=@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(x=%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 0
    @py_assert3 = inc(x=@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(x=%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = [0, 1, 0, 1]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_memoize_args_kwargs():

    @memoize
    def mul(x, by=1):
        calls.append((x, by))
        return x * by

    calls = []
    @py_assert1 = 0
    @py_assert3 = mul(@py_assert1)
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mul) if 'mul' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mul) else 'mul'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = mul(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mul) if 'mul' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mul) else 'mul'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 0
    @py_assert3 = mul(@py_assert1)
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mul) if 'mul' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mul) else 'mul'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = [(0, 1), (1, 1)]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = 0
    @py_assert3 = 1
    @py_assert5 = mul(@py_assert1, @py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mul) if 'mul' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mul) else 'mul'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 1
    @py_assert3 = 1
    @py_assert5 = mul(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mul) if 'mul' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mul) else 'mul'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 0
    @py_assert3 = 1
    @py_assert5 = mul(@py_assert1, @py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(mul) if 'mul' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mul) else 'mul'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = [(0, 1), (1, 1), (0, 1), (1, 1)]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_memoize_memory():

    @memoize
    def inc(x):
        calls.append(x)
        return x + 1

    calls = []
    inc(0)
    inc.memory.clear()
    inc(0)
    @py_assert2 = [0, 0]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_memoize_key_func():

    @memoize(key_func=len)
    def inc(s):
        calls.append(s)
        return s * 2

    calls = []
    @py_assert1 = 'a'
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 'aa'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'b'
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 'aa'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    inc('ab')
    @py_assert2 = ['a', 'ab']
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_make_lookuper():

    @make_lookuper
    def letter_index():
        return ((c, i) for i, c in enumerate('abcdefghij'))

    @py_assert1 = 'c'
    @py_assert3 = letter_index(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(letter_index) if 'letter_index' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(letter_index) else 'letter_index'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    with pytest.raises(LookupError):
        letter_index('_')


def test_make_lookuper_nested():
    tables_built = [
     0]

    @make_lookuper
    def function_table(f):
        tables_built[0] += 1
        return ((x, f(x)) for x in range(10))

    @py_assert2 = function_table(sin)
    @py_assert4 = 5
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert10 = 5
    @py_assert12 = sin(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py9': @pytest_ar._saferepr(sin) if 'sin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sin) else 'sin', 'py1': @pytest_ar._saferepr(sin) if 'sin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sin) else 'sin', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(function_table) if 'function_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_table) else 'function_table', 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert2 = function_table(cos)
    @py_assert4 = 3
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert10 = 3
    @py_assert12 = cos(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py9': @pytest_ar._saferepr(cos) if 'cos' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cos) else 'cos', 'py1': @pytest_ar._saferepr(cos) if 'cos' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cos) else 'cos', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(function_table) if 'function_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_table) else 'function_table', 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert2 = function_table(sin)
    @py_assert4 = 3
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert10 = 3
    @py_assert12 = sin(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py9': @pytest_ar._saferepr(sin) if 'sin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sin) else 'sin', 'py1': @pytest_ar._saferepr(sin) if 'sin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sin) else 'sin', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(function_table) if 'function_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_table) else 'function_table', 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert0 = tables_built[0]
    @py_assert3 = 2
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    with pytest.raises(LookupError):
        function_table(cos)(-1)


def test_silent_lookuper():

    @silent_lookuper
    def letter_index():
        return ((c, i) for i, c in enumerate('abcdefghij'))

    @py_assert1 = 'c'
    @py_assert3 = letter_index(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(letter_index) if 'letter_index' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(letter_index) else 'letter_index'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '_'
    @py_assert3 = letter_index(@py_assert1)
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(letter_index) if 'letter_index' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(letter_index) else 'letter_index'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_silnent_lookuper_nested():

    @silent_lookuper
    def function_table(f):
        return ((x, f(x)) for x in range(10))

    @py_assert2 = function_table(sin)
    @py_assert4 = 5
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert10 = 5
    @py_assert12 = sin(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py9': @pytest_ar._saferepr(sin) if 'sin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sin) else 'sin', 'py1': @pytest_ar._saferepr(sin) if 'sin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sin) else 'sin', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(function_table) if 'function_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_table) else 'function_table', 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert2 = function_table(cos)
    @py_assert4 = 1
    @py_assert6 = -@py_assert4
    @py_assert7 = @py_assert2(@py_assert6)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(-%(py5)s)\n} is %(py11)s',), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(cos) if 'cos' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cos) else 'cos', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(function_table) if 'function_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_table) else 'function_table', 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_cache():
    calls = []

    @cache(timeout=60)
    def inc(x):
        calls.append(x)
        return x + 1

    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    inc.invalidate(0)
    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = [0, 1, 0]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_cache_timedout():
    calls = []

    @cache(timeout=0)
    def inc(x):
        calls.append(x)
        return x + 1

    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 0
    @py_assert3 = inc(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = [0, 0]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None