# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_funcs.py
# Compiled at: 2018-10-03 08:49:11
# Size of source mod 2**32: 4503 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from operator import __add__, __sub__
import pytest
from whatever import _
from funcy.py2 import map, merge_with
from funcy.funcs import *
from funcy.seqs import keep

def test_caller():
    @py_assert1 = [
     1, 2]
    @py_assert3 = caller(@py_assert1)
    @py_assert6 = @py_assert3(sum)
    @py_assert9 = 3
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(caller) if 'caller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caller) else 'caller',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(sum) if 'sum' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sum) else 'sum',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_constantly():
    @py_assert1 = 42
    @py_assert3 = constantly(@py_assert1)
    @py_assert5 = @py_assert3()
    @py_assert8 = 42
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(constantly) if 'constantly' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(constantly) else 'constantly',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 42
    @py_assert3 = constantly(@py_assert1)
    @py_assert5 = 'hi'
    @py_assert7 = 'there'
    @py_assert9 = 'shout'
    @py_assert11 = @py_assert3(@py_assert5, @py_assert7, volume=@py_assert9)
    @py_assert14 = 42
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s, %(py8)s, volume=%(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(constantly) if 'constantly' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(constantly) else 'constantly',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_partial():
    @py_assert2 = 10
    @py_assert4 = partial(__add__, @py_assert2)
    @py_assert6 = 1
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 11
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(partial) if 'partial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(partial) else 'partial',  'py1':@pytest_ar._saferepr(__add__) if '__add__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__add__) else '__add__',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = 'abra'
    @py_assert4 = partial(__add__, @py_assert2)
    @py_assert6 = 'cadabra'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 'abracadabra'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(partial) if 'partial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(partial) else 'partial',  'py1':@pytest_ar._saferepr(__add__) if '__add__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__add__) else '__add__',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    merge = lambda a=None, b=None: a + b
    @py_assert2 = 'abra'
    @py_assert4 = partial(merge, a=@py_assert2)
    @py_assert6 = 'cadabra'
    @py_assert8 = @py_assert4(b=@py_assert6)
    @py_assert11 = 'abracadabra'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, a=%(py3)s)\n}(b=%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(partial) if 'partial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(partial) else 'partial',  'py1':@pytest_ar._saferepr(merge) if 'merge' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge) else 'merge',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = 'abra'
    @py_assert4 = partial(merge, b=@py_assert2)
    @py_assert6 = 'cadabra'
    @py_assert8 = @py_assert4(a=@py_assert6)
    @py_assert11 = 'cadabraabra'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, b=%(py3)s)\n}(a=%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(partial) if 'partial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(partial) else 'partial',  'py1':@pytest_ar._saferepr(merge) if 'merge' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge) else 'merge',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_func_partial():

    class A(object):
        f = func_partial(lambda x, self: x + 1, 10)

    @py_assert1 = A()
    @py_assert3 = @py_assert1.f
    @py_assert5 = @py_assert3()
    @py_assert8 = 11
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s()\n}.f\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(A) if 'A' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(A) else 'A',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_back_partial():
    @py_assert2 = 10
    @py_assert4 = rpartial(__sub__, @py_assert2)
    @py_assert6 = 1
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 9
    @py_assert13 = -@py_assert11
    @py_assert10 = @py_assert8 == @py_assert13
    if not @py_assert10:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}(%(py7)s)\n} == -%(py12)s', ), (@py_assert8, @py_assert13)) % {'py0':@pytest_ar._saferepr(rpartial) if 'rpartial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rpartial) else 'rpartial',  'py1':@pytest_ar._saferepr(__sub__) if '__sub__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__sub__) else '__sub__',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = None
    @py_assert2 = 2
    @py_assert4 = 85
    @py_assert6 = rpartial(pow, @py_assert2, @py_assert4)
    @py_assert8 = 10
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert13 = 15
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s)\n}(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(rpartial) if 'rpartial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rpartial) else 'rpartial',  'py1':@pytest_ar._saferepr(pow) if 'pow' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pow) else 'pow',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_curry():
    @py_assert1 = lambda : 42
    @py_assert3 = curry(@py_assert1)
    @py_assert5 = @py_assert3()
    @py_assert8 = 42
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = 2
    @py_assert4 = _ * @py_assert2
    @py_assert5 = curry(@py_assert4)
    @py_assert7 = 21
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert12 = 42
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py0)s((%(py1)s * %(py3)s))\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert3 = _ * _
    @py_assert4 = curry(@py_assert3)
    @py_assert6 = 6
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 7
    @py_assert12 = @py_assert8(@py_assert10)
    @py_assert15 = 42
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s((%(py1)s * %(py2)s))\n}(%(py7)s)\n}(%(py11)s)\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert2 = 2
    @py_assert4 = curry(__add__, @py_assert2)
    @py_assert6 = 10
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 1
    @py_assert12 = @py_assert8(@py_assert10)
    @py_assert15 = 11
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}(%(py7)s)\n}(%(py11)s)\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py1':@pytest_ar._saferepr(__add__) if '__add__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__add__) else '__add__',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert2 = curry(__add__)
    @py_assert4 = 10
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = 1
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert13 = 11
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n}(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py1':@pytest_ar._saferepr(__add__) if '__add__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__add__) else '__add__',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = lambda x, y, z: x + y + z
    @py_assert3 = curry(@py_assert1)
    @py_assert5 = 'a'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = 'b'
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert13 = 'c'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert18 = 'abc'
    @py_assert17 = @py_assert15 == @py_assert18
    if not @py_assert17:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n}(%(py10)s)\n}(%(py14)s)\n} == %(py19)s', ), (@py_assert15, @py_assert18)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert18 = None


def test_curry_funcy():
    @py_assert2 = curry(map)
    @py_assert5 = @py_assert2(int)
    @py_assert7 = '123'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert12 = [
     1, 2, 3]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py4)s)\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py1':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert2 = curry(merge_with)
    @py_assert5 = @py_assert2(sum)
    @py_assert7 = {1: 1}
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert12 = {1: 1}
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py4)s)\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(curry) if 'curry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(curry) else 'curry',  'py1':@pytest_ar._saferepr(merge_with) if 'merge_with' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge_with) else 'merge_with',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(sum) if 'sum' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sum) else 'sum',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_rcurry():
    @py_assert2 = 2
    @py_assert4 = rcurry(__sub__, @py_assert2)
    @py_assert6 = 10
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = 1
    @py_assert12 = @py_assert8(@py_assert10)
    @py_assert15 = 9
    @py_assert17 = -@py_assert15
    @py_assert14 = @py_assert12 == @py_assert17
    if not @py_assert14:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}(%(py7)s)\n}(%(py11)s)\n} == -%(py16)s', ), (@py_assert12, @py_assert17)) % {'py0':@pytest_ar._saferepr(rcurry) if 'rcurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rcurry) else 'rcurry',  'py1':@pytest_ar._saferepr(__sub__) if '__sub__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__sub__) else '__sub__',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = None
    @py_assert1 = lambda x, y, z: x + y + z
    @py_assert3 = rcurry(@py_assert1)
    @py_assert5 = 'a'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = 'b'
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert13 = 'c'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert18 = 'cba'
    @py_assert17 = @py_assert15 == @py_assert18
    if not @py_assert17:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n}(%(py10)s)\n}(%(py14)s)\n} == %(py19)s', ), (@py_assert15, @py_assert18)) % {'py0':@pytest_ar._saferepr(rcurry) if 'rcurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rcurry) else 'rcurry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert18 = None


def test_autocurry():
    at = autocurry(lambda a, b, c: (a, b, c))
    @py_assert1 = 1
    @py_assert3 = at(@py_assert1)
    @py_assert5 = 2
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = 3
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert14 = (1, 2, 3)
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n}(%(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    @py_assert1 = 1
    @py_assert3 = 2
    @py_assert5 = at(@py_assert1, @py_assert3)
    @py_assert7 = 3
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert12 = (1, 2, 3)
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 1
    @py_assert3 = at(@py_assert1)
    @py_assert5 = 2
    @py_assert7 = 3
    @py_assert9 = @py_assert3(@py_assert5, @py_assert7)
    @py_assert12 = (1, 2, 3)
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 1
    @py_assert3 = 2
    @py_assert5 = 3
    @py_assert7 = at(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = (1, 2, 3)
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    with pytest.raises(TypeError):
        at(1, 2, 3, 4)
    with pytest.raises(TypeError):
        at(1, 2)(3, 4)
    @py_assert1 = 1
    @py_assert3 = 2
    @py_assert5 = 3
    @py_assert7 = at(a=@py_assert1, b=@py_assert3, c=@py_assert5)
    @py_assert10 = (1, 2, 3)
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(a=%(py2)s, b=%(py4)s, c=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 3
    @py_assert3 = at(c=@py_assert1)
    @py_assert5 = 1
    @py_assert7 = 2
    @py_assert9 = @py_assert3(@py_assert5, @py_assert7)
    @py_assert12 = (1, 2, 3)
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py0)s(c=%(py2)s)\n}(%(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 4
    @py_assert3 = at(c=@py_assert1)
    @py_assert5 = 3
    @py_assert7 = @py_assert3(c=@py_assert5)
    @py_assert9 = 1
    @py_assert11 = 2
    @py_assert13 = @py_assert7(@py_assert9, @py_assert11)
    @py_assert16 = (1, 2, 3)
    @py_assert15 = @py_assert13 == @py_assert16
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(c=%(py2)s)\n}(c=%(py6)s)\n}(%(py10)s, %(py12)s)\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None
    with pytest.raises(TypeError):
        at(a=1)(1, 2, 3)


def test_autocurry_named():
    at = autocurry(lambda a, b, c=9: (a, b, c))
    @py_assert1 = 1
    @py_assert3 = at(@py_assert1)
    @py_assert5 = 2
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = (1, 2, 9)
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 1
    @py_assert3 = at(@py_assert1)
    @py_assert5 = 2
    @py_assert7 = 3
    @py_assert9 = @py_assert3(@py_assert5, @py_assert7)
    @py_assert12 = (1, 2, 3)
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 1
    @py_assert3 = at(a=@py_assert1)
    @py_assert5 = 2
    @py_assert7 = @py_assert3(b=@py_assert5)
    @py_assert10 = (1, 2, 9)
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(a=%(py2)s)\n}(b=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 3
    @py_assert3 = at(c=@py_assert1)
    @py_assert5 = 1
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = 2
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert14 = (1, 2, 3)
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(c=%(py2)s)\n}(%(py6)s)\n}(%(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(at) if 'at' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(at) else 'at',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_autocurry_builtin():
    @py_assert2 = autocurry(complex)
    @py_assert4 = 1
    @py_assert6 = @py_assert2(imag=@py_assert4)
    @py_assert8 = 0
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert13 = complex(0.0, 1.0)
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(imag=%(py5)s)\n}(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(autocurry) if 'autocurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(autocurry) else 'autocurry',  'py1':@pytest_ar._saferepr(complex) if 'complex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complex) else 'complex',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = autocurry(map)
    @py_assert5 = 1
    @py_assert7 = _ + @py_assert5
    @py_assert8 = @py_assert2(@py_assert7)
    @py_assert10 = [
     1, 2]
    @py_assert12 = @py_assert8(@py_assert10)
    @py_assert15 = [
     2, 3]
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}((%(py4)s + %(py6)s))\n}(%(py11)s)\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(autocurry) if 'autocurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(autocurry) else 'autocurry',  'py1':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert2 = autocurry(int)
    @py_assert4 = 12
    @py_assert6 = @py_assert2(base=@py_assert4)
    @py_assert8 = '100'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert13 = 144
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(base=%(py5)s)\n}(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(autocurry) if 'autocurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(autocurry) else 'autocurry',  'py1':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_autocurry_hard():

    def required_star(f, *seqs):
        return map(f, *seqs)

    @py_assert2 = autocurry(required_star)
    @py_assert5 = @py_assert2(__add__)
    @py_assert7 = '12'
    @py_assert9 = 'ab'
    @py_assert11 = @py_assert5(@py_assert7, @py_assert9)
    @py_assert14 = [
     '1a', '2b']
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py4)s)\n}(%(py8)s, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(autocurry) if 'autocurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(autocurry) else 'autocurry',  'py1':@pytest_ar._saferepr(required_star) if 'required_star' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(required_star) else 'required_star',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(__add__) if '__add__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__add__) else '__add__',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    _iter = autocurry(iter)
    @py_assert2 = [1, 2]
    @py_assert4 = _iter(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(_iter) if '_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_iter) else '_iter',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = [0, 1, 2]
    @py_assert4 = @py_assert2.pop
    @py_assert6 = _iter(@py_assert4)
    @py_assert8 = 0
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = list(@py_assert10)
    @py_assert15 = [
     2, 1]
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py1)s(%(py5)s\n{%(py5)s = %(py3)s.pop\n})\n}(%(py9)s)\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(_iter) if '_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_iter) else '_iter',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    _keep = autocurry(keep)
    @py_assert2 = '01'
    @py_assert4 = _keep(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     '0', '1']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(_keep) if '_keep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_keep) else '_keep',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert3 = _keep(int)
    @py_assert5 = '01'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert12 = [
     1]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n}(%(py6)s)\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(_keep) if '_keep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_keep) else '_keep',  'py2':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    with pytest.raises(TypeError):
        _keep(1, 2, 3)


def test_autocurry_class():

    class A:

        def __init__(self, x, y=0):
            self.x, self.y = x, y

    @py_assert2 = autocurry(A)
    @py_assert4 = 1
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = @py_assert6.__dict__
    @py_assert11 = {'x':1, 
     'y':0}
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n}.__dict__\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(autocurry) if 'autocurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(autocurry) else 'autocurry',  'py1':@pytest_ar._saferepr(A) if 'A' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(A) else 'A',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None

    class B:
        pass

    autocurry(B)()

    class I(int):
        pass

    @py_assert2 = autocurry(int)
    @py_assert4 = 12
    @py_assert6 = @py_assert2(base=@py_assert4)
    @py_assert8 = '100'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert13 = 144
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(base=%(py5)s)\n}(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(autocurry) if 'autocurry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(autocurry) else 'autocurry',  'py1':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_compose():
    double = _ * 2
    inc = _ + 1
    @py_assert1 = compose()
    @py_assert3 = 10
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 10
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(compose) if 'compose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compose) else 'compose',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = compose(double)
    @py_assert4 = 10
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = 20
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(compose) if 'compose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compose) else 'compose',  'py1':@pytest_ar._saferepr(double) if 'double' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double) else 'double',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert3 = compose(inc, double)
    @py_assert5 = 10
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 21
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(compose) if 'compose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compose) else 'compose',  'py1':@pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc',  'py2':@pytest_ar._saferepr(double) if 'double' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double) else 'double',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert4 = compose(str, inc, double)
    @py_assert6 = 10
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = '21'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py2)s, %(py3)s)\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(compose) if 'compose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compose) else 'compose',  'py1':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py2':@pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc',  'py3':@pytest_ar._saferepr(double) if 'double' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double) else 'double',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = '\\d+'
    @py_assert4 = compose(int, @py_assert2)
    @py_assert6 = 'abc1234xy'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 1234
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(compose) if 'compose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compose) else 'compose',  'py1':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_rcompose():
    double = _ * 2
    inc = _ + 1
    @py_assert1 = rcompose()
    @py_assert3 = 10
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 10
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(rcompose) if 'rcompose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rcompose) else 'rcompose',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = rcompose(double)
    @py_assert4 = 10
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = 20
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(rcompose) if 'rcompose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rcompose) else 'rcompose',  'py1':@pytest_ar._saferepr(double) if 'double' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double) else 'double',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert3 = rcompose(inc, double)
    @py_assert5 = 10
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 22
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(rcompose) if 'rcompose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rcompose) else 'rcompose',  'py1':@pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc',  'py2':@pytest_ar._saferepr(double) if 'double' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double) else 'double',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert3 = rcompose(double, inc)
    @py_assert5 = 10
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert10 = 21
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}(%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(rcompose) if 'rcompose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rcompose) else 'rcompose',  'py1':@pytest_ar._saferepr(double) if 'double' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(double) else 'double',  'py2':@pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_complement():
    @py_assert2 = complement(identity)
    @py_assert4 = 0
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = True
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py1':@pytest_ar._saferepr(identity) if 'identity' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identity) else 'identity',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = complement(identity)
    @py_assert4 = [
     1, 2]
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py1':@pytest_ar._saferepr(identity) if 'identity' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(identity) else 'identity',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_juxt():
    @py_assert3 = ljuxt(__add__, __sub__)
    @py_assert5 = 10
    @py_assert7 = 2
    @py_assert9 = @py_assert3(@py_assert5, @py_assert7)
    @py_assert12 = [
     12, 8]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}(%(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(ljuxt) if 'ljuxt' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ljuxt) else 'ljuxt',  'py1':@pytest_ar._saferepr(__add__) if '__add__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__add__) else '__add__',  'py2':@pytest_ar._saferepr(__sub__) if '__sub__' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(__sub__) else '__sub__',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert3 = 1
    @py_assert5 = _ + @py_assert3
    @py_assert7 = 1
    @py_assert9 = _ - @py_assert7
    @py_assert10 = ljuxt(@py_assert5, @py_assert9)
    @py_assert12 = [
     2, 3]
    @py_assert14 = map(@py_assert10, @py_assert12)
    @py_assert17 = [
     [
      3, 1], [4, 2]]
    @py_assert16 = @py_assert14 == @py_assert17
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py11)s\n{%(py11)s = %(py1)s((%(py2)s + %(py4)s), (%(py6)s - %(py8)s))\n}, %(py13)s)\n} == %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(ljuxt) if 'ljuxt' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ljuxt) else 'ljuxt',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_iffy():
    @py_assert3 = 2
    @py_assert5 = _ % @py_assert3
    @py_assert7 = 2
    @py_assert9 = _ * @py_assert7
    @py_assert11 = 2
    @py_assert13 = _ / @py_assert11
    @py_assert14 = iffy(@py_assert5, @py_assert9, @py_assert13)
    @py_assert16 = [
     1, 2, 3, 4]
    @py_assert18 = map(@py_assert14, @py_assert16)
    @py_assert21 = [
     2, 1, 6, 2]
    @py_assert20 = @py_assert18 == @py_assert21
    if not @py_assert20:
        @py_format23 = @pytest_ar._call_reprcompare(('==',), (@py_assert20,), ('%(py19)s\n{%(py19)s = %(py0)s(%(py15)s\n{%(py15)s = %(py1)s((%(py2)s %% %(py4)s), (%(py6)s * %(py8)s), (%(py10)s / %(py12)s))\n}, %(py17)s)\n} == %(py22)s',), (@py_assert18, @py_assert21)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18),  'py22':@pytest_ar._saferepr(@py_assert21)}
        @py_format25 = ('' + 'assert %(py24)s') % {'py24': @py_format23}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert21 = None
    @py_assert3 = 2
    @py_assert5 = _ % @py_assert3
    @py_assert7 = 2
    @py_assert9 = _ * @py_assert7
    @py_assert10 = iffy(@py_assert5, @py_assert9)
    @py_assert12 = [
     1, 2, 3, 4]
    @py_assert14 = map(@py_assert10, @py_assert12)
    @py_assert17 = [
     2, 2, 6, 4]
    @py_assert16 = @py_assert14 == @py_assert17
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py11)s\n{%(py11)s = %(py1)s((%(py2)s %% %(py4)s), (%(py6)s * %(py8)s))\n}, %(py13)s)\n} == %(py18)s',), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None
    @py_assert3 = 2
    @py_assert5 = _ * @py_assert3
    @py_assert6 = iffy(@py_assert5)
    @py_assert8 = [
     21, '', None]
    @py_assert10 = map(@py_assert6, @py_assert8)
    @py_assert13 = [
     42, '', None]
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s((%(py2)s * %(py4)s))\n}, %(py9)s)\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert3 = 2
    @py_assert5 = _ % @py_assert3
    @py_assert7 = 2
    @py_assert9 = _ * @py_assert7
    @py_assert10 = None
    @py_assert12 = iffy(@py_assert5, @py_assert9, @py_assert10)
    @py_assert14 = [
     1, 2, 3, 4]
    @py_assert16 = map(@py_assert12, @py_assert14)
    @py_assert19 = [
     2, None, 6, None]
    @py_assert18 = @py_assert16 == @py_assert19
    if not @py_assert18:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert18,), ('%(py17)s\n{%(py17)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s((%(py2)s %% %(py4)s), (%(py6)s * %(py8)s), %(py11)s)\n}, %(py15)s)\n} == %(py20)s',), (@py_assert16, @py_assert19)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert19 = None
    @py_assert3 = 1
    @py_assert5 = _ + @py_assert3
    @py_assert6 = 1
    @py_assert8 = iffy(@py_assert5, default=@py_assert6)
    @py_assert10 = [
     1, None, 2]
    @py_assert12 = map(@py_assert8, @py_assert10)
    @py_assert15 = [
     2, 1, 3]
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s((%(py2)s + %(py4)s), default=%(py7)s)\n}, %(py11)s)\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert3 = [1, 4, 5]
    @py_assert5 = set(@py_assert3)
    @py_assert8 = 2
    @py_assert10 = _ * @py_assert8
    @py_assert11 = iffy(@py_assert5, @py_assert10)
    @py_assert13 = [
     1, 2, 3, 4]
    @py_assert15 = map(@py_assert11, @py_assert13)
    @py_assert18 = [
     2, 2, 3, 8]
    @py_assert17 = @py_assert15 == @py_assert18
    if not @py_assert17:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py0)s(%(py12)s\n{%(py12)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n}, (%(py7)s * %(py9)s))\n}, %(py14)s)\n} == %(py19)s',), (@py_assert15, @py_assert18)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert18 = None
    @py_assert2 = '\\d+'
    @py_assert5 = str.upper
    @py_assert7 = iffy(@py_assert2, @py_assert5)
    @py_assert9 = [
     'a2', 'c']
    @py_assert11 = map(@py_assert7, @py_assert9)
    @py_assert14 = [
     'A2', 'c']
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py3)s, %(py6)s\n{%(py6)s = %(py4)s.upper\n})\n}, %(py10)s)\n} == %(py15)s',), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    @py_assert3 = [1, 4, 5]
    @py_assert5 = set(@py_assert3)
    @py_assert7 = iffy(@py_assert5)
    @py_assert9 = [
     False, 2, 4]
    @py_assert11 = map(@py_assert7, @py_assert9)
    @py_assert14 = [
     False, False, True]
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n}, %(py10)s)\n} == %(py15)s',), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py2':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    @py_assert2 = None
    @py_assert4 = iffy(@py_assert2)
    @py_assert6 = [
     False, 2, 3, 4]
    @py_assert8 = map(@py_assert4, @py_assert6)
    @py_assert11 = [
     False, 2, 3, 4]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n} == %(py12)s',), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map',  'py1':@pytest_ar._saferepr(iffy) if 'iffy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iffy) else 'iffy',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None