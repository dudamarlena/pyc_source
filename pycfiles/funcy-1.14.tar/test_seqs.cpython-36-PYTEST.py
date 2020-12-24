# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_seqs.py
# Compiled at: 2018-10-03 08:49:11
# Size of source mod 2**32: 6622 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from operator import add
import pytest
from whatever import _
from funcy.compat import range, Iterator, PY3
from funcy import is_list
from funcy.seqs import *

def test_repeatedly():
    counter = count()
    c = lambda : next(counter)
    @py_assert1 = 2
    @py_assert5 = repeatedly(c)
    @py_assert7 = take(@py_assert1, @py_assert5)
    @py_assert10 = [
     0, 1]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(take) if 'take' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(take) else 'take',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(repeatedly) if 'repeatedly' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repeatedly) else 'repeatedly',  'py4':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_iterate():
    @py_assert1 = 4
    @py_assert5 = 2
    @py_assert7 = _ * @py_assert5
    @py_assert8 = 1
    @py_assert10 = iterate(@py_assert7, @py_assert8)
    @py_assert12 = take(@py_assert1, @py_assert10)
    @py_assert15 = [
     1, 2, 4, 8]
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py2)s, %(py11)s\n{%(py11)s = %(py3)s((%(py4)s * %(py6)s), %(py9)s)\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(take) if 'take' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(take) else 'take',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(iterate) if 'iterate' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterate) else 'iterate',  'py4':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_take():
    @py_assert1 = 2
    @py_assert3 = [
     3, 2, 1]
    @py_assert5 = take(@py_assert1, @py_assert3)
    @py_assert8 = [
     3, 2]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(take) if 'take' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(take) else 'take',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 2
    @py_assert4 = 7
    @py_assert6 = count(@py_assert4)
    @py_assert8 = take(@py_assert1, @py_assert6)
    @py_assert11 = [
     7, 8]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py2)s, %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(take) if 'take' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(take) else 'take',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_drop():
    dropped = drop(2, [5, 4, 3, 2])
    @py_assert3 = isinstance(dropped, Iterator)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(dropped) if 'dropped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dropped) else 'dropped',  'py2':@pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert2 = list(dropped)
    @py_assert5 = [
     3, 2]
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(dropped) if 'dropped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dropped) else 'dropped',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = 2
    @py_assert4 = 2
    @py_assert7 = count()
    @py_assert9 = drop(@py_assert4, @py_assert7)
    @py_assert11 = take(@py_assert1, @py_assert9)
    @py_assert14 = [
     2, 3]
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py2)s, %(py10)s\n{%(py10)s = %(py3)s(%(py5)s, %(py8)s\n{%(py8)s = %(py6)s()\n})\n})\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(take) if 'take' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(take) else 'take',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(drop) if 'drop' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(drop) else 'drop',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_first():
    @py_assert1 = 'xyz'
    @py_assert3 = first(@py_assert1)
    @py_assert6 = 'x'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(first) if 'first' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first) else 'first',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = 7
    @py_assert4 = count(@py_assert2)
    @py_assert6 = first(@py_assert4)
    @py_assert9 = 7
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(first) if 'first' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first) else 'first',  'py1':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = []
    @py_assert3 = first(@py_assert1)
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(first) if 'first' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first) else 'first',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_second():
    @py_assert1 = 'xyz'
    @py_assert3 = second(@py_assert1)
    @py_assert6 = 'y'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(second) if 'second' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(second) else 'second',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = 7
    @py_assert4 = count(@py_assert2)
    @py_assert6 = second(@py_assert4)
    @py_assert9 = 8
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(second) if 'second' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(second) else 'second',  'py1':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = 'x'
    @py_assert3 = second(@py_assert1)
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(second) if 'second' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(second) else 'second',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_last():
    @py_assert1 = 'xyz'
    @py_assert3 = last(@py_assert1)
    @py_assert6 = 'z'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(last) if 'last' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(last) else 'last',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = 1
    @py_assert4 = 10
    @py_assert6 = range(@py_assert2, @py_assert4)
    @py_assert8 = last(@py_assert6)
    @py_assert11 = 9
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(last) if 'last' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(last) else 'last',  'py1':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert1 = []
    @py_assert3 = last(@py_assert1)
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(last) if 'last' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(last) else 'last',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = (x for x in 'xyz')
    @py_assert3 = last(@py_assert1)
    @py_assert6 = 'z'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(last) if 'last' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(last) else 'last',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_nth():
    @py_assert1 = 0
    @py_assert3 = 'xyz'
    @py_assert5 = nth(@py_assert1, @py_assert3)
    @py_assert8 = 'x'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(nth) if 'nth' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nth) else 'nth',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 2
    @py_assert3 = 'xyz'
    @py_assert5 = nth(@py_assert1, @py_assert3)
    @py_assert8 = 'z'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(nth) if 'nth' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nth) else 'nth',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 3
    @py_assert3 = 'xyz'
    @py_assert5 = nth(@py_assert1, @py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(nth) if 'nth' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nth) else 'nth',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 3
    @py_assert4 = 7
    @py_assert6 = count(@py_assert4)
    @py_assert8 = nth(@py_assert1, @py_assert6)
    @py_assert11 = 10
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py2)s, %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(nth) if 'nth' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nth) else 'nth',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_butlast():
    @py_assert2 = 'xyz'
    @py_assert4 = butlast(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     'x', 'y']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(butlast) if 'butlast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(butlast) else 'butlast',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = []
    @py_assert4 = butlast(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = []
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(butlast) if 'butlast' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(butlast) else 'butlast',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_ilen():
    @py_assert1 = 'xyz'
    @py_assert3 = ilen(@py_assert1)
    @py_assert6 = 3
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ilen) if 'ilen' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ilen) else 'ilen',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = 10
    @py_assert4 = range(@py_assert2)
    @py_assert6 = ilen(@py_assert4)
    @py_assert9 = 10
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(ilen) if 'ilen' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ilen) else 'ilen',  'py1':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_lmap():
    @py_assert2 = 2
    @py_assert4 = _ * @py_assert2
    @py_assert5 = [
     2, 3]
    @py_assert7 = lmap(@py_assert4, @py_assert5)
    @py_assert10 = [
     4, 6]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s((%(py1)s * %(py3)s), %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = None
    @py_assert3 = [
     2, 3]
    @py_assert5 = lmap(@py_assert1, @py_assert3)
    @py_assert8 = [
     2, 3]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert3 = _ + _
    @py_assert4 = [
     1, 2]
    @py_assert6 = [
     4, 5]
    @py_assert8 = lmap(@py_assert3, @py_assert4, @py_assert6)
    @py_assert11 = [
     5, 7]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s((%(py1)s + %(py2)s), %(py5)s, %(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert1 = '\\d+'
    @py_assert3 = [
     'a2', '13b']
    @py_assert5 = lmap(@py_assert1, @py_assert3)
    @py_assert8 = [
     '2', '13']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = {'a':1,  'b':2}
    @py_assert3 = 'ab'
    @py_assert5 = lmap(@py_assert1, @py_assert3)
    @py_assert8 = [
     1, 2]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = [1, 2, 3]
    @py_assert4 = set(@py_assert2)
    @py_assert6 = [
     0, 1, 2]
    @py_assert8 = lmap(@py_assert4, @py_assert6)
    @py_assert11 = [
     False, True, True]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py1':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert1 = 1
    @py_assert3 = [
     'abc', '123']
    @py_assert5 = lmap(@py_assert1, @py_assert3)
    @py_assert8 = [
     'b', '2']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = 2
    @py_assert4 = slice(@py_assert2)
    @py_assert6 = [
     'abc', '123']
    @py_assert8 = lmap(@py_assert4, @py_assert6)
    @py_assert11 = [
     'ab', '12']
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py1':@pytest_ar._saferepr(slice) if 'slice' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(slice) else 'slice',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


@pytest.mark.skipif(PY3, reason="map(None, ...) doesn't work in python 3")
def test_map_multi():
    @py_assert1 = None
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = 'abc'
    @py_assert7 = lmap(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = [
     (1, 'a'), (2, 'b'), (3, 'c')]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@pytest.mark.skipif(PY3, reason="imap(None, ...) doesn't work in python 3")
def test_imap_strange():
    """
    Demonstrates funcy.imap and itertools.imap have behavior when given None as f.
    """
    @py_assert2 = None
    @py_assert4 = 'abc'
    @py_assert6 = map(@py_assert2, @py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     ('a', ), ('b', ), ('c', )]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_filter():
    @py_assert1 = None
    @py_assert3 = [
     2, 3, 0]
    @py_assert5 = lfilter(@py_assert1, @py_assert3)
    @py_assert8 = [
     2, 3]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = '\\d+'
    @py_assert3 = [
     'a2', '13b', 'c']
    @py_assert5 = lfilter(@py_assert1, @py_assert3)
    @py_assert8 = [
     'a2', '13b']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = [1, 2, 3]
    @py_assert4 = set(@py_assert2)
    @py_assert6 = [
     0, 1, 2, 4, 1]
    @py_assert8 = lfilter(@py_assert4, @py_assert6)
    @py_assert11 = [
     1, 2, 1]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py1':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_remove():
    @py_assert3 = 3
    @py_assert2 = _ > @py_assert3
    @py_assert8 = 10
    @py_assert10 = range(@py_assert8)
    @py_assert12 = lremove(@py_assert2, @py_assert10)
    @py_assert15 = [
     0, 1, 2, 3]
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (_, @py_assert3)) % {'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py6)s, %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(lremove) if 'lremove' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lremove) else 'lremove',  'py6':@py_format5,  'py7':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert3 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert1 = '^a'
    @py_assert3 = [
     'a', 'b', 'ba']
    @py_assert5 = lremove(@py_assert1, @py_assert3)
    @py_assert8 = [
     'b', 'ba']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lremove) if 'lremove' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lremove) else 'lremove',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_keep():
    @py_assert2 = 3
    @py_assert4 = _ % @py_assert2
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = lkeep(@py_assert4, @py_assert8)
    @py_assert13 = [
     1, 2, 1]
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s((%(py1)s %% %(py3)s), %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(lkeep) if 'lkeep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lkeep) else 'lkeep',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = 5
    @py_assert4 = range(@py_assert2)
    @py_assert6 = lkeep(@py_assert4)
    @py_assert9 = [
     1, 2, 3, 4]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(lkeep) if 'lkeep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lkeep) else 'lkeep',  'py1':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert4 = 4
    @py_assert6 = range(@py_assert4)
    @py_assert8 = mapcat(range, @py_assert6)
    @py_assert10 = lkeep(@py_assert8)
    @py_assert13 = [
     1, 1, 2]
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py2)s, %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(lkeep) if 'lkeep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lkeep) else 'lkeep',  'py1':@pytest_ar._saferepr(mapcat) if 'mapcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mapcat) else 'mapcat',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py3':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_concat():
    @py_assert1 = 'ab'
    @py_assert3 = 'cd'
    @py_assert5 = lconcat(@py_assert1, @py_assert3)
    @py_assert9 = 'abcd'
    @py_assert11 = list(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(lconcat) if 'lconcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lconcat) else 'lconcat',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert1 = lconcat()
    @py_assert4 = []
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(lconcat) if 'lconcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lconcat) else 'lconcat',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_cat():
    @py_assert1 = 'abcd'
    @py_assert3 = lcat(@py_assert1)
    @py_assert7 = 'abcd'
    @py_assert9 = list(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(lcat) if 'lcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lcat) else 'lcat',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = (range(x) for x in range(3))
    @py_assert3 = lcat(@py_assert1)
    @py_assert6 = [
     0, 0, 1]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lcat) if 'lcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lcat) else 'lcat',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_flatten():
    @py_assert1 = [
     1, [2, 3]]
    @py_assert3 = lflatten(@py_assert1)
    @py_assert6 = [
     1, 2, 3]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lflatten) if 'lflatten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lflatten) else 'lflatten',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [[1, 2], 3]
    @py_assert3 = lflatten(@py_assert1)
    @py_assert6 = [
     1, 2, 3]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lflatten) if 'lflatten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lflatten) else 'lflatten',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [(2, 3)]
    @py_assert3 = lflatten(@py_assert1)
    @py_assert6 = [
     2, 3]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lflatten) if 'lflatten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lflatten) else 'lflatten',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [iter([2, 3])]
    @py_assert3 = lflatten(@py_assert1)
    @py_assert6 = [
     2, 3]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lflatten) if 'lflatten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lflatten) else 'lflatten',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_flatten_follow():
    @py_assert1 = [
     1, [2, 3]]
    @py_assert4 = lflatten(@py_assert1, follow=is_list)
    @py_assert7 = [
     1, 2, 3]
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, follow=%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(lflatten) if 'lflatten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lflatten) else 'lflatten',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(is_list) if 'is_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_list) else 'is_list',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = [1, [(2, 3)]]
    @py_assert4 = lflatten(@py_assert1, follow=is_list)
    @py_assert7 = [
     1, (2, 3)]
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, follow=%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(lflatten) if 'lflatten' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lflatten) else 'lflatten',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(is_list) if 'is_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_list) else 'is_list',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_mapcat():
    @py_assert1 = lambda x: [
     x, x]
    @py_assert3 = 'abc'
    @py_assert5 = lmapcat(@py_assert1, @py_assert3)
    @py_assert9 = 'aabbcc'
    @py_assert11 = list(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(lmapcat) if 'lmapcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmapcat) else 'lmapcat',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_interleave():
    @py_assert2 = 'ab'
    @py_assert4 = 'cd'
    @py_assert6 = interleave(@py_assert2, @py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert12 = 'acbd'
    @py_assert14 = list(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(interleave) if 'interleave' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleave) else 'interleave',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert2 = 'ab_'
    @py_assert4 = 'cd'
    @py_assert6 = interleave(@py_assert2, @py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert12 = 'acbd'
    @py_assert14 = list(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(interleave) if 'interleave' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleave) else 'interleave',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_iterpose():
    @py_assert2 = '.'
    @py_assert4 = 'abc'
    @py_assert6 = interpose(@py_assert2, @py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert12 = 'a.b.c'
    @py_assert14 = list(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(interpose) if 'interpose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interpose) else 'interpose',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_takewhile():
    @py_assert2 = [
     1, 2, None, 3]
    @py_assert4 = takewhile(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(takewhile) if 'takewhile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(takewhile) else 'takewhile',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_distinct():
    @py_assert1 = 'abcbad'
    @py_assert3 = ldistinct(@py_assert1)
    @py_assert7 = 'abcd'
    @py_assert9 = list(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(ldistinct) if 'ldistinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ldistinct) else 'ldistinct',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = [{}, {}, {'a': 1}, {'b': 2}]
    @py_assert4 = ldistinct(@py_assert1, key=len)
    @py_assert7 = [{}, {'a': 1}]
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, key=%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(ldistinct) if 'ldistinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ldistinct) else 'ldistinct',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = ['ab', 'cb', 'ad']
    @py_assert3 = 0
    @py_assert5 = ldistinct(@py_assert1, key=@py_assert3)
    @py_assert8 = [
     'ab', 'cb']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, key=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(ldistinct) if 'ldistinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ldistinct) else 'ldistinct',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_split():
    @py_assert4 = 2
    @py_assert6 = _ % @py_assert4
    @py_assert8 = 5
    @py_assert10 = range(@py_assert8)
    @py_assert12 = split(@py_assert6, @py_assert10)
    @py_assert14 = lmap(list, @py_assert12)
    @py_assert17 = [
     [
      1, 3], [0, 2, 4]]
    @py_assert16 = @py_assert14 == @py_assert17
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py13)s\n{%(py13)s = %(py2)s((%(py3)s %% %(py5)s), %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n})\n})\n} == %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py3':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_lsplit():
    @py_assert2 = 2
    @py_assert4 = _ % @py_assert2
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = lsplit(@py_assert4, @py_assert8)
    @py_assert13 = (
     [
      1, 3], [0, 2, 4])
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s((%(py1)s %% %(py3)s), %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(lsplit) if 'lsplit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lsplit) else 'lsplit',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    with pytest.raises(TypeError):
        lsplit(2, range(5))


def test_split_at():
    @py_assert1 = 2
    @py_assert4 = 5
    @py_assert6 = range(@py_assert4)
    @py_assert8 = lsplit_at(@py_assert1, @py_assert6)
    @py_assert11 = (
     [
      0, 1], [2, 3, 4])
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py2)s, %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(lsplit_at) if 'lsplit_at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lsplit_at) else 'lsplit_at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_split_by():
    @py_assert2 = 2
    @py_assert4 = _ % @py_assert2
    @py_assert5 = [
     1, 2, 3]
    @py_assert7 = lsplit_by(@py_assert4, @py_assert5)
    @py_assert10 = (
     [
      1], [2, 3])
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s((%(py1)s %% %(py3)s), %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lsplit_by) if 'lsplit_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lsplit_by) else 'lsplit_by',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_group_by():
    @py_assert2 = 2
    @py_assert4 = _ % @py_assert2
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = group_by(@py_assert4, @py_assert8)
    @py_assert13 = {0:[
      0, 2, 4], 
     1:[1, 3]}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s((%(py1)s %% %(py3)s), %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(group_by) if 'group_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(group_by) else 'group_by',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = '\\d'
    @py_assert3 = [
     'a1', 'b2', 'c1']
    @py_assert5 = group_by(@py_assert1, @py_assert3)
    @py_assert8 = {'1':[
      'a1', 'c1'], 
     '2':['b2']}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(group_by) if 'group_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(group_by) else 'group_by',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_group_by_keys():
    @py_assert1 = '(\\d)(\\d)'
    @py_assert3 = [
     '12', '23']
    @py_assert5 = group_by_keys(@py_assert1, @py_assert3)
    @py_assert8 = {'1':[
      '12'], 
     '2':['12', '23'],  '3':['23']}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(group_by_keys) if 'group_by_keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(group_by_keys) else 'group_by_keys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_group_values():
    @py_assert1 = [
     'ab', 'ac', 'ba']
    @py_assert3 = group_values(@py_assert1)
    @py_assert6 = {'a':[
      'b', 'c'], 
     'b':['a']}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(group_values) if 'group_values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(group_values) else 'group_values',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_count_by():
    @py_assert2 = 2
    @py_assert4 = _ % @py_assert2
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = count_by(@py_assert4, @py_assert8)
    @py_assert13 = {0:3, 
     1:2}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s((%(py1)s %% %(py3)s), %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(count_by) if 'count_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count_by) else 'count_by',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = '\\d'
    @py_assert3 = [
     'a1', 'b2', 'c1']
    @py_assert5 = count_by(@py_assert1, @py_assert3)
    @py_assert8 = {'1':2, 
     '2':1}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(count_by) if 'count_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count_by) else 'count_by',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_count_by_is_defaultdict():
    cnts = count_by(len, [])
    @py_assert0 = cnts[1]
    @py_assert3 = 0
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_count_reps():
    @py_assert1 = [
     0, 1, 0]
    @py_assert3 = count_reps(@py_assert1)
    @py_assert6 = {0:2, 
     1:1}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(count_reps) if 'count_reps' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count_reps) else 'count_reps',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_partition():
    @py_assert1 = 2
    @py_assert3 = [
     0, 1, 2, 3, 4]
    @py_assert5 = lpartition(@py_assert1, @py_assert3)
    @py_assert8 = [
     [
      0, 1], [2, 3]]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lpartition) if 'lpartition' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition) else 'lpartition',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 2
    @py_assert3 = 1
    @py_assert5 = [
     0, 1, 2, 3]
    @py_assert7 = lpartition(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = [
     [
      0, 1], [1, 2], [2, 3]]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lpartition) if 'lpartition' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition) else 'lpartition',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 2
    @py_assert5 = 5
    @py_assert7 = range(@py_assert5)
    @py_assert9 = iter(@py_assert7)
    @py_assert11 = lpartition(@py_assert1, @py_assert9)
    @py_assert14 = [
     [
      0, 1], [2, 3]]
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py2)s, %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n})\n})\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(lpartition) if 'lpartition' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition) else 'lpartition',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter',  'py4':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    @py_assert3 = 2
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = lpartition(@py_assert3, @py_assert8)
    @py_assert12 = lmap(list, @py_assert10)
    @py_assert15 = [
     [
      0, 1], [2, 3]]
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py1)s, %(py11)s\n{%(py11)s = %(py2)s(%(py4)s, %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(lmap) if 'lmap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lmap) else 'lmap',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(lpartition) if 'lpartition' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition) else 'lpartition',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_chunks():
    @py_assert1 = 2
    @py_assert3 = [
     0, 1, 2, 3, 4]
    @py_assert5 = lchunks(@py_assert1, @py_assert3)
    @py_assert8 = [
     [
      0, 1], [2, 3], [4]]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lchunks) if 'lchunks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lchunks) else 'lchunks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 2
    @py_assert3 = 1
    @py_assert5 = [
     0, 1, 2, 3]
    @py_assert7 = lchunks(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = [
     [
      0, 1], [1, 2], [2, 3], [3]]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lchunks) if 'lchunks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lchunks) else 'lchunks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 3
    @py_assert3 = 1
    @py_assert7 = 3
    @py_assert9 = range(@py_assert7)
    @py_assert11 = iter(@py_assert9)
    @py_assert13 = lchunks(@py_assert1, @py_assert3, @py_assert11)
    @py_assert16 = [
     [
      0, 1, 2], [1, 2], [2]]
    @py_assert15 = @py_assert13 == @py_assert16
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py0)s(%(py2)s, %(py4)s, %(py12)s\n{%(py12)s = %(py5)s(%(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n})\n})\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(lchunks) if 'lchunks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lchunks) else 'lchunks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter',  'py6':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_partition_by():
    @py_assert1 = lambda x: x == 3
    @py_assert3 = [
     1, 2, 3, 4, 5]
    @py_assert5 = lpartition_by(@py_assert1, @py_assert3)
    @py_assert8 = [
     [
      1, 2], [3], [4, 5]]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lpartition_by) if 'lpartition_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition_by) else 'lpartition_by',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 'x'
    @py_assert3 = 'abxcd'
    @py_assert5 = lpartition_by(@py_assert1, @py_assert3)
    @py_assert8 = [
     [
      'a', 'b'], ['x'], ['c', 'd']]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lpartition_by) if 'lpartition_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition_by) else 'lpartition_by',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = '\\d'
    @py_assert3 = '1211'
    @py_assert5 = lpartition_by(@py_assert1, @py_assert3)
    @py_assert8 = [
     [
      '1'], ['2'], ['1', '1']]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lpartition_by) if 'lpartition_by' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpartition_by) else 'lpartition_by',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_with_prev():
    @py_assert3 = 3
    @py_assert5 = range(@py_assert3)
    @py_assert7 = with_prev(@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert12 = [
     (0, None), (1, 0), (2, 1)]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(with_prev) if 'with_prev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(with_prev) else 'with_prev',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_with_next():
    @py_assert3 = 3
    @py_assert5 = range(@py_assert3)
    @py_assert7 = with_next(@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert12 = [
     (0, 1), (1, 2), (2, None)]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(with_next) if 'with_next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(with_next) else 'with_next',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_pairwise():
    @py_assert3 = 3
    @py_assert5 = range(@py_assert3)
    @py_assert7 = pairwise(@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert12 = [
     (0, 1), (1, 2)]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(pairwise) if 'pairwise' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pairwise) else 'pairwise',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_reductions():
    @py_assert2 = []
    @py_assert4 = lreductions(add, @py_assert2)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(lreductions) if 'lreductions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lreductions) else 'lreductions',  'py1':@pytest_ar._saferepr(add) if 'add' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add) else 'add',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = [None]
    @py_assert4 = lreductions(add, @py_assert2)
    @py_assert7 = [
     None]
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(lreductions) if 'lreductions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lreductions) else 'lreductions',  'py1':@pytest_ar._saferepr(add) if 'add' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add) else 'add',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = [1, 2, 3, 4]
    @py_assert4 = lreductions(add, @py_assert2)
    @py_assert7 = [
     1, 3, 6, 10]
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(lreductions) if 'lreductions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lreductions) else 'lreductions',  'py1':@pytest_ar._saferepr(add) if 'add' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add) else 'add',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = lambda x, y: x + [y]
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = []
    @py_assert7 = lreductions(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = [
     [
      1], [1, 2], [1, 2, 3]]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lreductions) if 'lreductions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lreductions) else 'lreductions',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_sums():
    @py_assert1 = []
    @py_assert3 = lsums(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lsums) if 'lsums' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lsums) else 'lsums',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [1, 2, 3, 4]
    @py_assert3 = lsums(@py_assert1)
    @py_assert6 = [
     1, 3, 6, 10]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lsums) if 'lsums' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lsums) else 'lsums',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [[1], [2], [3]]
    @py_assert3 = lsums(@py_assert1)
    @py_assert6 = [
     [
      1], [1, 2], [1, 2, 3]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lsums) if 'lsums' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lsums) else 'lsums',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_without():
    @py_assert1 = []
    @py_assert3 = lwithout(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lwithout) if 'lwithout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lwithout) else 'lwithout',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [1, 2, 3, 4]
    @py_assert3 = lwithout(@py_assert1)
    @py_assert6 = [
     1, 2, 3, 4]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lwithout) if 'lwithout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lwithout) else 'lwithout',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [1, 2, 1, 0, 3, 1, 4]
    @py_assert3 = 0
    @py_assert5 = 1
    @py_assert7 = lwithout(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = [
     2, 3, 4]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(lwithout) if 'lwithout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lwithout) else 'lwithout',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None