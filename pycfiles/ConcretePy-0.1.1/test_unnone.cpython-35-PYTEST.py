# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_unnone.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 380 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import lun, dun, sun

def test_lun():
    @py_assert1 = []
    @py_assert3 = lun(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(lun) if 'lun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lun) else 'lun'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = [
     3]
    @py_assert3 = lun(@py_assert1)
    @py_assert6 = [3]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(lun) if 'lun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lun) else 'lun'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = None
    @py_assert3 = lun(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(lun) if 'lun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lun) else 'lun'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_dun():
    @py_assert2 = dict()
    @py_assert4 = dun(@py_assert2)
    @py_assert8 = dict()
    @py_assert6 = @py_assert4 == @py_assert8
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s()\n})\n} == %(py9)s\n{%(py9)s = %(py7)s()\n}',), (@py_assert4, @py_assert8)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(dun) if 'dun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dun) else 'dun', 'py7': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict', 'py1': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict', 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = 3
    @py_assert4 = dict(x=@py_assert2)
    @py_assert6 = dun(@py_assert4)
    @py_assert10 = 3
    @py_assert12 = dict(x=@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(x=%(py3)s)\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(x=%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py13': @pytest_ar._saferepr(@py_assert12), 'py0': @pytest_ar._saferepr(dun) if 'dun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dun) else 'dun', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = None
    @py_assert3 = dun(@py_assert1)
    @py_assert7 = dict()
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py8)s\n{%(py8)s = %(py6)s()\n}',), (@py_assert3, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(dun) if 'dun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dun) else 'dun', 'py6': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_sun():
    @py_assert2 = []
    @py_assert4 = set(@py_assert2)
    @py_assert6 = sun(@py_assert4)
    @py_assert10 = []
    @py_assert12 = set(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py13': @pytest_ar._saferepr(@py_assert12), 'py0': @pytest_ar._saferepr(sun) if 'sun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sun) else 'sun', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert2 = [
     3]
    @py_assert4 = set(@py_assert2)
    @py_assert6 = sun(@py_assert4)
    @py_assert10 = [3]
    @py_assert12 = set(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}',), (@py_assert6, @py_assert12)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py13': @pytest_ar._saferepr(@py_assert12), 'py0': @pytest_ar._saferepr(sun) if 'sun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sun) else 'sun', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = None
    @py_assert3 = sun(@py_assert1)
    @py_assert7 = []
    @py_assert9 = set(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}',), (@py_assert3, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(sun) if 'sun' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sun) else 'sun', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None