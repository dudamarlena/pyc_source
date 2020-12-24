# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/types/test_dict.py
# Compiled at: 2013-12-08 17:19:04
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises
from operator import itemgetter
from itertools import permutations
from mio.errors import KeyError

def test_null(mio):
    @py_assert3 = mio.eval
    @py_assert5 = 'Dict'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = iter(@py_assert7)
    @py_assert11 = dict(@py_assert9)
    @py_assert14 = {}
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py1)s(%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.eval\n}(%(py6)s)\n})\n})\n} == %(py15)s',), (@py_assert11, @py_assert14)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict', 'py1': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py2': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py15': @pytest_ar._saferepr(@py_assert14), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    return


def test_clone(mio):
    @py_assert1 = mio.eval
    @py_assert3 = 'Dict clone()'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = {}
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_hash(mio):
    l = mio.eval('Dict clone()')
    l.__hash__() is None
    return


def test_clone_dict(mio):
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'Dict clone(Dict clone() __setitem__("a", 1))'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    return


def test_repr(mio):
    @py_assert2 = mio.eval
    @py_assert4 = 'Dict'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = repr(@py_assert6)
    @py_assert11 = '{}'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_repr2(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert2 = mio.eval
    @py_assert4 = 'd'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = repr(@py_assert6)
    @py_assert11 = [ '{' + (', ').join(p) + '}' for p in permutations(['u"a": 1', 'u"b": 2', 'u"c": 3']) ]
    @py_assert10 = @py_assert8 in @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('in', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} in %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_setitem(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd __setitem__("d", 4)'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    return


def test_getitem(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'd __getitem__("a")'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_getitem_KeyError(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    with raises(KeyError):
        mio.eval('d __getitem__("d")', reraise=True)
    return


def test_delitem(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd __delitem__("a")'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    return


def test_len(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'd len'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_len2(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'd __len__()'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_len3(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = mio.eval
    @py_assert4 = 'd'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 3
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_keys(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = mio.eval
    @py_assert4 = 'd keys'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = sorted(@py_assert6)
    @py_assert11 = ['a', 'b', 'c']
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_values(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = mio.eval
    @py_assert4 = 'd values'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = sorted(@py_assert6)
    @py_assert11 = [1, 2, 3]
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_items(mio):
    mio.eval('d = Dict clone()')
    mio.eval('d __setitem__("a", 1)')
    mio.eval('d __setitem__("b", 2)')
    mio.eval('d __setitem__("c", 3)')
    @py_assert1 = mio.frommio
    @py_assert4 = mio.eval
    @py_assert6 = 'd'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.frommio\n}(%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.eval\n}(%(py7)s)\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = mio.frommio
    @py_assert5 = mio.eval
    @py_assert7 = 'd items'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert2(@py_assert9)
    @py_assert14 = 0
    @py_assert16 = itemgetter(@py_assert14)
    @py_assert18 = sorted(@py_assert11, key=@py_assert16)
    @py_assert21 = [['a', 1], ['b', 2], ['c', 3]]
    @py_assert20 = @py_assert18 == @py_assert21
    if not @py_assert20:
        @py_format23 = @pytest_ar._call_reprcompare(('==',), (@py_assert20,), ('%(py19)s\n{%(py19)s = %(py0)s(%(py12)s\n{%(py12)s = %(py3)s\n{%(py3)s = %(py1)s.frommio\n}(%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.eval\n}(%(py8)s)\n})\n}, key=%(py17)s\n{%(py17)s = %(py13)s(%(py15)s)\n})\n} == %(py22)s',), (@py_assert18, @py_assert21)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py19': @pytest_ar._saferepr(@py_assert18), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py4': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py17': @pytest_ar._saferepr(@py_assert16), 'py6': @pytest_ar._saferepr(@py_assert5), 'py15': @pytest_ar._saferepr(@py_assert14), 'py12': @pytest_ar._saferepr(@py_assert11), 'py22': @pytest_ar._saferepr(@py_assert21), 'py13': @pytest_ar._saferepr(itemgetter) if 'itemgetter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(itemgetter) else 'itemgetter'}
        @py_format25 = 'assert %(py24)s' % {'py24': @py_format23}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert21 = None
    return