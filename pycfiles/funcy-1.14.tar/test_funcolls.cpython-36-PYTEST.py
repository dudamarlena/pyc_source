# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_funcolls.py
# Compiled at: 2018-10-03 08:49:11
# Size of source mod 2**32: 647 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from whatever import _
from funcy.compat import lfilter
from funcy.funcolls import *

def test_all_fn():
    @py_assert4 = 3
    @py_assert3 = _ > @py_assert4
    @py_assert9 = 2
    @py_assert11 = _ % @py_assert9
    @py_assert12 = all_fn(@py_assert3, @py_assert11)
    @py_assert15 = 10
    @py_assert17 = range(@py_assert15)
    @py_assert19 = lfilter(@py_assert12, @py_assert17)
    @py_assert22 = [
     5, 7, 9]
    @py_assert21 = @py_assert19 == @py_assert22
    if not @py_assert21:
        @py_format6 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s > %(py5)s', ), (_, @py_assert4)) % {'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert21,), ('%(py20)s\n{%(py20)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s(%(py7)s, (%(py8)s %% %(py10)s))\n}, %(py18)s\n{%(py18)s = %(py14)s(%(py16)s)\n})\n} == %(py23)s', ), (@py_assert19, @py_assert22)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py1':@pytest_ar._saferepr(all_fn) if 'all_fn' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all_fn) else 'all_fn',  'py7':@py_format6,  'py8':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert3 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = None


def test_any_fn():
    @py_assert4 = 3
    @py_assert3 = _ > @py_assert4
    @py_assert9 = 2
    @py_assert11 = _ % @py_assert9
    @py_assert12 = any_fn(@py_assert3, @py_assert11)
    @py_assert15 = 10
    @py_assert17 = range(@py_assert15)
    @py_assert19 = lfilter(@py_assert12, @py_assert17)
    @py_assert22 = [
     1, 3, 4, 5, 6, 7, 8, 9]
    @py_assert21 = @py_assert19 == @py_assert22
    if not @py_assert21:
        @py_format6 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s > %(py5)s', ), (_, @py_assert4)) % {'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert21,), ('%(py20)s\n{%(py20)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s(%(py7)s, (%(py8)s %% %(py10)s))\n}, %(py18)s\n{%(py18)s = %(py14)s(%(py16)s)\n})\n} == %(py23)s', ), (@py_assert19, @py_assert22)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py1':@pytest_ar._saferepr(any_fn) if 'any_fn' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any_fn) else 'any_fn',  'py7':@py_format6,  'py8':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert3 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = None


def test_none_fn():
    @py_assert4 = 3
    @py_assert3 = _ > @py_assert4
    @py_assert9 = 2
    @py_assert11 = _ % @py_assert9
    @py_assert12 = none_fn(@py_assert3, @py_assert11)
    @py_assert15 = 10
    @py_assert17 = range(@py_assert15)
    @py_assert19 = lfilter(@py_assert12, @py_assert17)
    @py_assert22 = [
     0, 2]
    @py_assert21 = @py_assert19 == @py_assert22
    if not @py_assert21:
        @py_format6 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s > %(py5)s', ), (_, @py_assert4)) % {'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert21,), ('%(py20)s\n{%(py20)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s(%(py7)s, (%(py8)s %% %(py10)s))\n}, %(py18)s\n{%(py18)s = %(py14)s(%(py16)s)\n})\n} == %(py23)s', ), (@py_assert19, @py_assert22)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py1':@pytest_ar._saferepr(none_fn) if 'none_fn' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_fn) else 'none_fn',  'py7':@py_format6,  'py8':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert3 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = None


def test_one_fn():
    @py_assert4 = 3
    @py_assert3 = _ > @py_assert4
    @py_assert9 = 2
    @py_assert11 = _ % @py_assert9
    @py_assert12 = one_fn(@py_assert3, @py_assert11)
    @py_assert15 = 10
    @py_assert17 = range(@py_assert15)
    @py_assert19 = lfilter(@py_assert12, @py_assert17)
    @py_assert22 = [
     1, 3, 4, 6, 8]
    @py_assert21 = @py_assert19 == @py_assert22
    if not @py_assert21:
        @py_format6 = @pytest_ar._call_reprcompare(('>', ), (@py_assert3,), ('%(py2)s > %(py5)s', ), (_, @py_assert4)) % {'py2':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert21,), ('%(py20)s\n{%(py20)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s(%(py7)s, (%(py8)s %% %(py10)s))\n}, %(py18)s\n{%(py18)s = %(py14)s(%(py16)s)\n})\n} == %(py23)s', ), (@py_assert19, @py_assert22)) % {'py0':@pytest_ar._saferepr(lfilter) if 'lfilter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lfilter) else 'lfilter',  'py1':@pytest_ar._saferepr(one_fn) if 'one_fn' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one_fn) else 'one_fn',  'py7':@py_format6,  'py8':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert3 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = None


def test_some_fn():
    @py_assert2 = 1
    @py_assert4 = _ - @py_assert2
    @py_assert6 = 0
    @py_assert8 = _ * @py_assert6
    @py_assert10 = 1
    @py_assert12 = _ + @py_assert10
    @py_assert14 = 2
    @py_assert16 = _ * @py_assert14
    @py_assert17 = some_fn(@py_assert4, @py_assert8, @py_assert12, @py_assert16)
    @py_assert19 = 1
    @py_assert21 = @py_assert17(@py_assert19)
    @py_assert24 = 2
    @py_assert23 = @py_assert21 == @py_assert24
    if not @py_assert23:
        @py_format26 = @pytest_ar._call_reprcompare(('==',), (@py_assert23,), ('%(py22)s\n{%(py22)s = %(py18)s\n{%(py18)s = %(py0)s((%(py1)s - %(py3)s), (%(py5)s * %(py7)s), (%(py9)s + %(py11)s), (%(py13)s * %(py15)s))\n}(%(py20)s)\n} == %(py25)s',), (@py_assert21, @py_assert24)) % {'py0':@pytest_ar._saferepr(some_fn) if 'some_fn' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(some_fn) else 'some_fn',  'py1':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_',  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py25':@pytest_ar._saferepr(@py_assert24)}
        @py_format28 = ('' + 'assert %(py27)s') % {'py27': @py_format26}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert24 = None


def test_extended_fns():
    f = any_fn(None, set([1, 2, 0]))
    @py_assert1 = 1
    @py_assert3 = f(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = 0
    @py_assert3 = f(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = 10
    @py_assert3 = f(@py_assert1)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = ''
    @py_assert3 = f(@py_assert1)
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py0':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None