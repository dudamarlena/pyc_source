# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_colls.py
# Compiled at: 2019-03-12 11:51:38
# Size of source mod 2**32: 8994 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from itertools import chain, count
from collections import defaultdict, namedtuple
from whatever import _
from funcy.compat import Iterator
from funcy.colls import *

def eq(a, b):
    return type(a) is type(b) and (a == b and (a.default_factory == b.default_factory if isinstance(a, defaultdict) else True))


def S(*args):
    """"Set literal" for the poor python 2.6"""
    return set(args)


def inc(x):
    return x + 1


def hinc(xs):
    return map(inc, xs)


def test_empty():
    @py_assert2 = {'a': 1}
    @py_assert4 = empty(@py_assert2)
    @py_assert6 = {}
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=27)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert4 = defaultdict(int)
    @py_assert6 = empty(@py_assert4)
    @py_assert10 = defaultdict(int)
    @py_assert12 = eq(@py_assert6, @py_assert10)
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=28)
    if not @py_assert12:
        @py_format14 = ('' + 'assert %(py13)s\n{%(py13)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n})\n}, %(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n})\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py1': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py2': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py13': @pytest_ar._saferepr(@py_assert12), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py3': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert4 = @py_assert6 = @py_assert10 = @py_assert12 = None
    @py_assert3 = defaultdict(int)
    @py_assert5 = empty(@py_assert3)
    @py_assert7 = @py_assert5.default_factory
    @py_assert12 = defaultdict(int)
    @py_assert14 = @py_assert12.default_factory
    @py_assert9 = @py_assert7 == @py_assert14
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=29)
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n}.default_factory\n} == %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py10)s(%(py11)s)\n}.default_factory\n}',), (@py_assert7, @py_assert14)) % {'py15': @pytest_ar._saferepr(@py_assert14), 'py10': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py11': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py13': @pytest_ar._saferepr(@py_assert12)}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_empty_iter():
    it = empty(iter([]))
    @py_assert3 = isinstance(it, Iterator)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=33)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py2': @pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert2 = list(it)
    @py_assert5 = []
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=34)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_empty_quirks():

    class A:
        FLAG = 1

    @py_assert2 = A.__dict__
    @py_assert4 = empty(@py_assert2)
    @py_assert7 = {}
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=39)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.__dict__\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(A) if 'A' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(A) else 'A', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = {}
    @py_assert3 = @py_assert1.keys
    @py_assert5 = @py_assert3()
    @py_assert7 = empty(@py_assert5)
    @py_assert10 = []
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=40)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.keys\n}()\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = {}
    @py_assert3 = @py_assert1.values
    @py_assert5 = @py_assert3()
    @py_assert7 = empty(@py_assert5)
    @py_assert10 = []
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=41)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.values\n}()\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = {}
    @py_assert3 = @py_assert1.items
    @py_assert5 = @py_assert3()
    @py_assert7 = empty(@py_assert5)
    @py_assert10 = []
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=42)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.items\n}()\n})\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(empty) if 'empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty) else 'empty', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_iteritems():
    @py_assert2 = [
     1, 2]
    @py_assert4 = iteritems(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=46)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(iteritems) if 'iteritems' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iteritems) else 'iteritems', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = (1, 2)
    @py_assert4 = iteritems(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=47)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(iteritems) if 'iteritems' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iteritems) else 'iteritems', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = {'a': 1}
    @py_assert4 = iteritems(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     ('a', 1)]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=48)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(iteritems) if 'iteritems' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iteritems) else 'iteritems', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_itervalues():
    @py_assert2 = [
     1, 2]
    @py_assert4 = itervalues(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=51)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(itervalues) if 'itervalues' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(itervalues) else 'itervalues', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = (1, 2)
    @py_assert4 = itervalues(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=52)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(itervalues) if 'itervalues' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(itervalues) else 'itervalues', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = {'a': 1}
    @py_assert4 = itervalues(@py_assert2)
    @py_assert6 = list(@py_assert4)
    @py_assert9 = [
     1]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=53)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(itervalues) if 'itervalues' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(itervalues) else 'itervalues', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_merge():
    @py_assert2 = {1: 2}
    @py_assert4 = {3: 4}
    @py_assert6 = merge(@py_assert2, @py_assert4)
    @py_assert8 = {1: 2, 3: 4}
    @py_assert10 = eq(@py_assert6, @py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=57)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n}, %(py9)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(merge) if 'merge' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge) else 'merge', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_join():
    @py_assert1 = []
    @py_assert3 = join(@py_assert1)
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=60)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py7)s',), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    with pytest.raises(TypeError):
        join([1])
    @py_assert2 = [
     'ab', '', 'cd']
    @py_assert4 = join(@py_assert2)
    @py_assert6 = 'abcd'
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=62)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = [['a', 'b'], 'c']
    @py_assert4 = join(@py_assert2)
    @py_assert7 = 'abc'
    @py_assert9 = list(@py_assert7)
    @py_assert11 = eq(@py_assert4, @py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=63)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n})\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py6': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert2 = [('a', 'b'), ('c',)]
    @py_assert4 = join(@py_assert2)
    @py_assert7 = 'abc'
    @py_assert9 = tuple(@py_assert7)
    @py_assert11 = eq(@py_assert4, @py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=64)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n})\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py6': @pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple', 'py12': @pytest_ar._saferepr(@py_assert11), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert2 = [{'a': 1}, {'b': 2}]
    @py_assert4 = join(@py_assert2)
    @py_assert6 = {'a': 1, 'b': 2}
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=65)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = [{'a': 1}, {'a': 2}]
    @py_assert4 = join(@py_assert2)
    @py_assert6 = {'a': 2}
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=66)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = [S(1, 2), S(3)]
    @py_assert4 = join(@py_assert2)
    @py_assert7 = 1
    @py_assert9 = 2
    @py_assert11 = 3
    @py_assert13 = S(@py_assert7, @py_assert9, @py_assert11)
    @py_assert15 = eq(@py_assert4, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=67)
    if not @py_assert15:
        @py_format17 = ('' + 'assert %(py16)s\n{%(py16)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py14)s\n{%(py14)s = %(py6)s(%(py8)s, %(py10)s, %(py12)s)\n})\n}') % {'py16': @pytest_ar._saferepr(@py_assert15), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py6': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py14': @pytest_ar._saferepr(@py_assert13), 'py12': @pytest_ar._saferepr(@py_assert11), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    it1 = (x for x in range(2))
    it2 = (x for x in range(5, 7))
    joined = join([it1, it2])
    @py_assert1 = []
    @py_assert5 = isinstance(joined, Iterator)
    @py_assert0 = @py_assert5
    if @py_assert5:
        @py_assert10 = list(joined)
        @py_assert13 = [
         0, 1, 5, 6]
        @py_assert12 = @py_assert10 == @py_assert13
        @py_assert0 = @py_assert12
    if @py_assert0 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=72)
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator', 'py3': @pytest_ar._saferepr(joined) if 'joined' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(joined) else 'joined'}
        @py_assert1.append(@py_format7)
        if @py_assert5:
            @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py14': @pytest_ar._saferepr(@py_assert13), 'py9': @pytest_ar._saferepr(joined) if 'joined' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(joined) else 'joined', 'py11': @pytest_ar._saferepr(@py_assert10), 'py8': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
            @py_format17 = '%(py16)s' % {'py16': @py_format15}
            @py_assert1.append(@py_format17)
        @py_format18 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert13 = None
    dd1 = defaultdict(int, a=1)
    dd2 = defaultdict(int, b=2)
    @py_assert2 = [dd1, dd2]
    @py_assert4 = join(@py_assert2)
    @py_assert8 = 1
    @py_assert10 = 2
    @py_assert12 = defaultdict(int, a=@py_assert8, b=@py_assert10)
    @py_assert14 = eq(@py_assert4, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=76)
    if not @py_assert14:
        @py_format16 = ('' + 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py13)s\n{%(py13)s = %(py6)s(%(py7)s, a=%(py9)s, b=%(py11)s)\n})\n}') % {'py15': @pytest_ar._saferepr(@py_assert14), 'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py6': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_join_iter():
    @py_assert2 = 'abc'
    @py_assert4 = iter(@py_assert2)
    @py_assert6 = join(@py_assert4)
    @py_assert9 = 'abc'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=79)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s',), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py1': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = [[1], [2]]
    @py_assert4 = iter(@py_assert2)
    @py_assert6 = join(@py_assert4)
    @py_assert9 = [
     1, 2]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=80)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s',), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py1': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert3 = [{'a': 1}, {'b': 2}]
    @py_assert5 = iter(@py_assert3)
    @py_assert7 = join(@py_assert5)
    @py_assert9 = {'a': 1, 'b': 2}
    @py_assert11 = eq(@py_assert7, @py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=81)
    if not @py_assert11:
        @py_format13 = ('' + 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n}, %(py10)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert3 = [S(1, 2), S(3)]
    @py_assert5 = iter(@py_assert3)
    @py_assert7 = join(@py_assert5)
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = 3
    @py_assert16 = S(@py_assert10, @py_assert12, @py_assert14)
    @py_assert18 = eq(@py_assert7, @py_assert16)
    if @py_assert18 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=82)
    if not @py_assert18:
        @py_format20 = ('' + 'assert %(py19)s\n{%(py19)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n}, %(py17)s\n{%(py17)s = %(py9)s(%(py11)s, %(py13)s, %(py15)s)\n})\n}') % {'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py13': @pytest_ar._saferepr(@py_assert12), 'py17': @pytest_ar._saferepr(@py_assert16), 'py1': @pytest_ar._saferepr(join) if 'join' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join) else 'join', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py15': @pytest_ar._saferepr(@py_assert14), 'py19': @pytest_ar._saferepr(@py_assert18), 'py2': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py9': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    it1 = (x for x in range(2))
    it2 = (x for x in range(5, 7))
    chained = join(iter([it1, it2]))
    @py_assert1 = []
    @py_assert5 = isinstance(chained, Iterator)
    @py_assert0 = @py_assert5
    if @py_assert5:
        @py_assert10 = list(chained)
        @py_assert13 = [
         0, 1, 5, 6]
        @py_assert12 = @py_assert10 == @py_assert13
        @py_assert0 = @py_assert12
    if @py_assert0 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=87)
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator', 'py3': @pytest_ar._saferepr(chained) if 'chained' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chained) else 'chained'}
        @py_assert1.append(@py_format7)
        if @py_assert5:
            @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py14': @pytest_ar._saferepr(@py_assert13), 'py9': @pytest_ar._saferepr(chained) if 'chained' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chained) else 'chained', 'py11': @pytest_ar._saferepr(@py_assert10), 'py8': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
            @py_format17 = '%(py16)s' % {'py16': @py_format15}
            @py_assert1.append(@py_format17)
        @py_format18 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_merge_with():
    @py_assert2 = {1: 1}
    @py_assert4 = {1: 10, 2: 2}
    @py_assert6 = merge_with(list, @py_assert2, @py_assert4)
    @py_assert9 = {1: [1, 10], 2: [2]}
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=91)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(merge_with) if 'merge_with' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge_with) else 'merge_with', 'py1': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = {1: 1}
    @py_assert4 = {1: 10, 2: 2}
    @py_assert6 = merge_with(sum, @py_assert2, @py_assert4)
    @py_assert9 = {1: 11, 2: 2}
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=92)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(merge_with) if 'merge_with' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge_with) else 'merge_with', 'py1': @pytest_ar._saferepr(sum) if 'sum' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sum) else 'sum', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = {1: 1}
    @py_assert4 = {1: 10, 2: 2}
    @py_assert6 = @py_assert4.items
    @py_assert8 = @py_assert6()
    @py_assert10 = merge_with(sum, @py_assert2, @py_assert8)
    @py_assert13 = {1: 11, 2: 2}
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=94)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py1)s, %(py3)s, %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.items\n}()\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py14': @pytest_ar._saferepr(@py_assert13), 'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(merge_with) if 'merge_with' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merge_with) else 'merge_with', 'py1': @pytest_ar._saferepr(sum) if 'sum' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sum) else 'sum', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_join_with():
    @py_assert2 = ({n % 3: n} for n in range(5))
    @py_assert4 = join_with(sum, @py_assert2)
    @py_assert7 = {0: 3, 1: 5, 2: 2}
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=97)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(sum) if 'sum' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sum) else 'sum', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(join_with) if 'join_with' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join_with) else 'join_with', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_walk():
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = walk(inc, @py_assert3)
    @py_assert7 = [
     2, 3, 4]
    @py_assert9 = eq(@py_assert5, @py_assert7)
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=101)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, %(py4)s)\n}, %(py8)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert3 = (1, 2, 3)
    @py_assert5 = walk(inc, @py_assert3)
    @py_assert7 = (
     2, 3, 4)
    @py_assert9 = eq(@py_assert5, @py_assert7)
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=102)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, %(py4)s)\n}, %(py8)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert4 = 1
    @py_assert6 = 2
    @py_assert8 = 3
    @py_assert10 = S(@py_assert4, @py_assert6, @py_assert8)
    @py_assert12 = walk(inc, @py_assert10)
    @py_assert15 = 2
    @py_assert17 = 3
    @py_assert19 = 4
    @py_assert21 = S(@py_assert15, @py_assert17, @py_assert19)
    @py_assert23 = eq(@py_assert12, @py_assert21)
    if @py_assert23 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=103)
    if not @py_assert23:
        @py_format25 = ('' + 'assert %(py24)s\n{%(py24)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s(%(py2)s, %(py11)s\n{%(py11)s = %(py3)s(%(py5)s, %(py7)s, %(py9)s)\n})\n}, %(py22)s\n{%(py22)s = %(py14)s(%(py16)s, %(py18)s, %(py20)s)\n})\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py24': @pytest_ar._saferepr(@py_assert23), 'py13': @pytest_ar._saferepr(@py_assert12), 'py14': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py22': @pytest_ar._saferepr(@py_assert21), 'py20': @pytest_ar._saferepr(@py_assert19), 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py16': @pytest_ar._saferepr(@py_assert15), 'py2': @pytest_ar._saferepr(inc) if 'inc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inc) else 'inc', 'py18': @pytest_ar._saferepr(@py_assert17), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = None
    @py_assert3 = {1: 1, 2: 2, 3: 3}
    @py_assert5 = walk(hinc, @py_assert3)
    @py_assert7 = {2: 2, 3: 3, 4: 4}
    @py_assert9 = eq(@py_assert5, @py_assert7)
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=104)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, %(py4)s)\n}, %(py8)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(hinc) if 'hinc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hinc) else 'hinc'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_walk_iter():
    it = walk(inc, chain([0], [1, 2]))
    @py_assert1 = []
    @py_assert5 = isinstance(it, Iterator)
    @py_assert0 = @py_assert5
    if @py_assert5:
        @py_assert10 = list(it)
        @py_assert13 = [
         1, 2, 3]
        @py_assert12 = @py_assert10 == @py_assert13
        @py_assert0 = @py_assert12
    if @py_assert0 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=108)
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator', 'py3': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it'}
        @py_assert1.append(@py_format7)
        if @py_assert5:
            @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py14': @pytest_ar._saferepr(@py_assert13), 'py9': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py11': @pytest_ar._saferepr(@py_assert10), 'py8': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
            @py_format17 = '%(py16)s' % {'py16': @py_format15}
            @py_assert1.append(@py_format17)
        @py_format18 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert13 = None
    it = walk(inc, (i for i in [0, 1, 2]))
    @py_assert1 = []
    @py_assert5 = isinstance(it, Iterator)
    @py_assert0 = @py_assert5
    if @py_assert5:
        @py_assert10 = list(it)
        @py_assert13 = [
         1, 2, 3]
        @py_assert12 = @py_assert10 == @py_assert13
        @py_assert0 = @py_assert12
    if @py_assert0 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=111)
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator', 'py3': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it'}
        @py_assert1.append(@py_format7)
        if @py_assert5:
            @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py14': @pytest_ar._saferepr(@py_assert13), 'py9': @pytest_ar._saferepr(it) if 'it' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(it) else 'it', 'py11': @pytest_ar._saferepr(@py_assert10), 'py8': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
            @py_format17 = '%(py16)s' % {'py16': @py_format15}
            @py_assert1.append(@py_format17)
        @py_format18 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_walk_extended():
    @py_assert1 = None
    @py_assert4 = 2
    @py_assert6 = 3
    @py_assert8 = S(@py_assert4, @py_assert6)
    @py_assert10 = walk(@py_assert1, @py_assert8)
    @py_assert14 = 2
    @py_assert16 = 3
    @py_assert18 = S(@py_assert14, @py_assert16)
    @py_assert12 = @py_assert10 == @py_assert18
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=114)
    if not @py_assert12:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py2)s, %(py9)s\n{%(py9)s = %(py3)s(%(py5)s, %(py7)s)\n})\n} == %(py19)s\n{%(py19)s = %(py13)s(%(py15)s, %(py17)s)\n}',), (@py_assert10, @py_assert18)) % {'py17': @pytest_ar._saferepr(@py_assert16), 'py7': @pytest_ar._saferepr(@py_assert6), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py13': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py15': @pytest_ar._saferepr(@py_assert14), 'py19': @pytest_ar._saferepr(@py_assert18), 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = '\\d+'
    @py_assert4 = 'a2'
    @py_assert6 = '13b'
    @py_assert8 = S(@py_assert4, @py_assert6)
    @py_assert10 = walk(@py_assert1, @py_assert8)
    @py_assert14 = '2'
    @py_assert16 = '13'
    @py_assert18 = S(@py_assert14, @py_assert16)
    @py_assert12 = @py_assert10 == @py_assert18
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=115)
    if not @py_assert12:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py2)s, %(py9)s\n{%(py9)s = %(py3)s(%(py5)s, %(py7)s)\n})\n} == %(py19)s\n{%(py19)s = %(py13)s(%(py15)s, %(py17)s)\n}',), (@py_assert10, @py_assert18)) % {'py17': @pytest_ar._saferepr(@py_assert16), 'py7': @pytest_ar._saferepr(@py_assert6), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py13': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py15': @pytest_ar._saferepr(@py_assert14), 'py19': @pytest_ar._saferepr(@py_assert18), 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = {'a': '1', 'b': '2'}
    @py_assert3 = 'ab'
    @py_assert5 = walk(@py_assert1, @py_assert3)
    @py_assert8 = '12'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=116)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = 1
    @py_assert4 = 2
    @py_assert6 = 3
    @py_assert8 = S(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = (
     0, 1, 2)
    @py_assert12 = walk(@py_assert8, @py_assert10)
    @py_assert15 = (
     False, True, True)
    @py_assert14 = @py_assert12 == @py_assert15
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=117)
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n}, %(py11)s)\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(walk) if 'walk' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk) else 'walk', 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_walk_keys():
    @py_assert2 = str.upper
    @py_assert4 = {'a': 1, 'b': 2}
    @py_assert6 = walk_keys(@py_assert2, @py_assert4)
    @py_assert9 = {'A': 1, 'B': 2}
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=120)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.upper\n}, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(walk_keys) if 'walk_keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk_keys) else 'walk_keys', 'py1': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = '\\d'
    @py_assert3 = {'a1': 1, 'b2': 2}
    @py_assert5 = walk_keys(@py_assert1, @py_assert3)
    @py_assert8 = {'1': 1, '2': 2}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=121)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(walk_keys) if 'walk_keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk_keys) else 'walk_keys'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_walk_values():
    @py_assert2 = 2
    @py_assert4 = _ * @py_assert2
    @py_assert5 = {'a': 1, 'b': 2}
    @py_assert7 = walk_values(@py_assert4, @py_assert5)
    @py_assert10 = {'a': 2, 'b': 4}
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=124)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s((%(py1)s * %(py3)s), %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(walk_values) if 'walk_values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk_values) else 'walk_values', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '\\d'
    @py_assert3 = {1: 'a1', 2: 'b2'}
    @py_assert5 = walk_values(@py_assert1, @py_assert3)
    @py_assert8 = {1: '1', 2: '2'}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=125)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(walk_values) if 'walk_values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walk_values) else 'walk_values'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_walk_values_defaultdict():
    dd = defaultdict(lambda : 'hey', {1: 'a', 2: 'ab'})
    walked_dd = walk_values(len, dd)
    @py_assert2 = {1: 1, 2: 2}
    @py_assert1 = walked_dd == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=130)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (walked_dd, @py_assert2)) % {'py0': @pytest_ar._saferepr(walked_dd) if 'walked_dd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(walked_dd) else 'walked_dd', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = walked_dd[0]
    @py_assert3 = 3
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=132)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_select():
    @py_assert4 = 1
    @py_assert3 = _ > @py_assert4
    @py_assert8 = [
     1, 2, 3]
    @py_assert10 = select(@py_assert3, @py_assert8)
    @py_assert12 = [
     2, 3]
    @py_assert14 = eq(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=136)
    if not @py_assert14:
        @py_format6 = @pytest_ar._call_reprcompare(('>',), (@py_assert3,), ('%(py2)s > %(py5)s',), (_, @py_assert4)) % {'py2': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format16 = ('' + 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py11)s\n{%(py11)s = %(py1)s(%(py7)s, %(py9)s)\n}, %(py13)s)\n}') % {'py15': @pytest_ar._saferepr(@py_assert14), 'py7': @py_format6, 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select', 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert4 = 1
    @py_assert3 = _ > @py_assert4
    @py_assert8 = (
     1, 2, 3)
    @py_assert10 = select(@py_assert3, @py_assert8)
    @py_assert12 = (
     2, 3)
    @py_assert14 = eq(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=137)
    if not @py_assert14:
        @py_format6 = @pytest_ar._call_reprcompare(('>',), (@py_assert3,), ('%(py2)s > %(py5)s',), (_, @py_assert4)) % {'py2': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format16 = ('' + 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py11)s\n{%(py11)s = %(py1)s(%(py7)s, %(py9)s)\n}, %(py13)s)\n}') % {'py15': @pytest_ar._saferepr(@py_assert14), 'py7': @py_format6, 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select', 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert4 = 1
    @py_assert3 = _ > @py_assert4
    @py_assert9 = 1
    @py_assert11 = 2
    @py_assert13 = 3
    @py_assert15 = S(@py_assert9, @py_assert11, @py_assert13)
    @py_assert17 = select(@py_assert3, @py_assert15)
    @py_assert20 = 2
    @py_assert22 = 3
    @py_assert24 = S(@py_assert20, @py_assert22)
    @py_assert26 = eq(@py_assert17, @py_assert24)
    if @py_assert26 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=138)
    if not @py_assert26:
        @py_format6 = @pytest_ar._call_reprcompare(('>',), (@py_assert3,), ('%(py2)s > %(py5)s',), (_, @py_assert4)) % {'py2': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format28 = ('' + 'assert %(py27)s\n{%(py27)s = %(py0)s(%(py18)s\n{%(py18)s = %(py1)s(%(py7)s, %(py16)s\n{%(py16)s = %(py8)s(%(py10)s, %(py12)s, %(py14)s)\n})\n}, %(py25)s\n{%(py25)s = %(py19)s(%(py21)s, %(py23)s)\n})\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py8': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py14': @pytest_ar._saferepr(@py_assert13), 'py18': @pytest_ar._saferepr(@py_assert17), 'py23': @pytest_ar._saferepr(@py_assert22), 'py25': @pytest_ar._saferepr(@py_assert24), 'py19': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py7': @py_format6, 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py27': @pytest_ar._saferepr(@py_assert26), 'py1': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select', 'py16': @pytest_ar._saferepr(@py_assert15), 'py21': @pytest_ar._saferepr(@py_assert20)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert3 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = @py_assert24 = @py_assert26 = None
    @py_assert2 = _[1]
    @py_assert5 = 1
    @py_assert4 = @py_assert2 > @py_assert5
    @py_assert9 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert11 = select(@py_assert4, @py_assert9)
    @py_assert13 = {'b': 2, 'c': 3}
    @py_assert15 = eq(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=139)
    if not @py_assert15:
        @py_format7 = @pytest_ar._call_reprcompare(('>',), (@py_assert4,), ('%(py3)s > %(py6)s',), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format17 = ('' + 'assert %(py16)s\n{%(py16)s = %(py0)s(%(py12)s\n{%(py12)s = %(py1)s(%(py8)s, %(py10)s)\n}, %(py14)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @py_format7, 'py1': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select', 'py16': @pytest_ar._saferepr(@py_assert15), 'py14': @pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = _[1]
    @py_assert4 = 1
    @py_assert3 = @py_assert1 > @py_assert4
    @py_assert10 = defaultdict(int)
    @py_assert12 = select(@py_assert3, @py_assert10)
    @py_assert15 = {}
    @py_assert14 = @py_assert12 == @py_assert15
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=140)
    if not @py_assert14:
        @py_format6 = @pytest_ar._call_reprcompare(('>',), (@py_assert3,), ('%(py2)s > %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py7)s, %(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n})\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py7': @py_format6, 'py0': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select', 'py8': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py13': @pytest_ar._saferepr(@py_assert12), 'py11': @pytest_ar._saferepr(@py_assert10)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_select_extended():
    @py_assert1 = None
    @py_assert3 = [
     2, 3, 0]
    @py_assert5 = select(@py_assert1, @py_assert3)
    @py_assert8 = [
     2, 3]
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=143)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = '\\d'
    @py_assert3 = 'a23bn45'
    @py_assert5 = select(@py_assert1, @py_assert3)
    @py_assert8 = '2345'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=144)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert2 = 1
    @py_assert4 = 2
    @py_assert6 = 3
    @py_assert8 = S(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = (
     0, 1, 2, 4, 1)
    @py_assert12 = select(@py_assert8, @py_assert10)
    @py_assert15 = (
     1, 2, 1)
    @py_assert14 = @py_assert12 == @py_assert15
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=145)
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n}, %(py11)s)\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(select) if 'select' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select) else 'select', 'py13': @pytest_ar._saferepr(@py_assert12), 'py1': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_select_keys():
    @py_assert1 = _[0]
    @py_assert4 = 'a'
    @py_assert3 = @py_assert1 == @py_assert4
    @py_assert8 = {'a': 1, 'b': 2, 'ab': 3}
    @py_assert10 = select_keys(@py_assert3, @py_assert8)
    @py_assert13 = {'a': 1, 'ab': 3}
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=148)
    if not @py_assert12:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py7)s, %(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @py_format6, 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(select_keys) if 'select_keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select_keys) else 'select_keys'}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = '^a'
    @py_assert3 = {'a': 1, 'b': 2, 'ab': 3, 'ba': 4}
    @py_assert5 = select_keys(@py_assert1, @py_assert3)
    @py_assert8 = {'a': 1, 'ab': 3}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=149)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(select_keys) if 'select_keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select_keys) else 'select_keys'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_select_values():
    @py_assert2 = 2
    @py_assert4 = _ % @py_assert2
    @py_assert5 = {'a': 1, 'b': 2}
    @py_assert7 = select_values(@py_assert4, @py_assert5)
    @py_assert10 = {'a': 1}
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=152)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s((%(py1)s %% %(py3)s), %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(select_values) if 'select_values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select_values) else 'select_values', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 'a'
    @py_assert3 = {1: 'a', 2: 'b'}
    @py_assert5 = select_values(@py_assert1, @py_assert3)
    @py_assert8 = {1: 'a'}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=153)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(select_values) if 'select_values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(select_values) else 'select_values'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_compact():
    @py_assert2 = [
     0, 1, None, 3]
    @py_assert4 = compact(@py_assert2)
    @py_assert6 = [
     1, 3]
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=157)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(compact) if 'compact' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compact) else 'compact', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = (0, 1, None, 3)
    @py_assert4 = compact(@py_assert2)
    @py_assert6 = (1, 3)
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=158)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(compact) if 'compact' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compact) else 'compact', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = {'a': None, 'b': 0, 'c': 1}
    @py_assert4 = compact(@py_assert2)
    @py_assert6 = {'c': 1}
    @py_assert8 = eq(@py_assert4, @py_assert6)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=159)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}, %(py7)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py1': @pytest_ar._saferepr(compact) if 'compact' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compact) else 'compact', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_is_distinct():
    @py_assert1 = 'abc'
    @py_assert3 = is_distinct(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=163)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(is_distinct) if 'is_distinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_distinct) else 'is_distinct'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = 'aba'
    @py_assert3 = is_distinct(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=164)
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(is_distinct) if 'is_distinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_distinct) else 'is_distinct'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = ['a', 'ab', 'abc']
    @py_assert4 = is_distinct(@py_assert1, key=len)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=165)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, key=%(py3)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(is_distinct) if 'is_distinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_distinct) else 'is_distinct', 'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    @py_assert1 = ['ab', 'cb', 'ad']
    @py_assert3 = 0
    @py_assert5 = is_distinct(@py_assert1, key=@py_assert3)
    @py_assert7 = not @py_assert5
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=166)
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, key=%(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(is_distinct) if 'is_distinct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_distinct) else 'is_distinct'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_all():
    @py_assert1 = [
     1, 2, 3]
    @py_assert3 = all(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=170)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [1, 2, '']
    @py_assert3 = all(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=171)
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = [abs, open, int]
    @py_assert4 = all(callable, @py_assert2)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=172)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py1': @pytest_ar._saferepr(callable) if 'callable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(callable) else 'callable', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all', 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert3 = 3
    @py_assert2 = _ < @py_assert3
    @py_assert7 = [
     1, 2, 5]
    @py_assert9 = all(@py_assert2, @py_assert7)
    @py_assert11 = not @py_assert9
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=173)
    if not @py_assert11:
        @py_format5 = @pytest_ar._call_reprcompare(('<', ), (@py_assert2,), ('%(py1)s < %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format12 = ('' + 'assert not %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_all_extended():
    @py_assert1 = None
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = all(@py_assert1, @py_assert3)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=176)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = None
    @py_assert3 = [
     1, 2, '']
    @py_assert5 = all(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=177)
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = '\\d'
    @py_assert3 = '125'
    @py_assert5 = all(@py_assert1, @py_assert3)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=178)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = '\\d'
    @py_assert3 = '12.5'
    @py_assert5 = all(@py_assert1, @py_assert3)
    @py_assert7 = not @py_assert5
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=179)
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}') % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_any():
    @py_assert1 = [
     0, False, 3, '']
    @py_assert3 = any(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=182)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(any) if 'any' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any) else 'any'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [0, False, '']
    @py_assert3 = any(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=183)
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(any) if 'any' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any) else 'any'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert3 = 0
    @py_assert2 = _ > @py_assert3
    @py_assert7 = [
     1, 2, 0]
    @py_assert9 = any(@py_assert2, @py_assert7)
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=184)
    if not @py_assert9:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(any) if 'any' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any) else 'any', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = None
    @py_assert3 = 0
    @py_assert2 = _ < @py_assert3
    @py_assert7 = [
     1, 2, 0]
    @py_assert9 = any(@py_assert2, @py_assert7)
    @py_assert11 = not @py_assert9
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=185)
    if not @py_assert11:
        @py_format5 = @pytest_ar._call_reprcompare(('<', ), (@py_assert2,), ('%(py1)s < %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format12 = ('' + 'assert not %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(any) if 'any' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any) else 'any', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_one():
    @py_assert1 = [
     0, False, 3, '']
    @py_assert3 = one(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=188)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(one) if 'one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one) else 'one'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [0, False, '']
    @py_assert3 = one(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=189)
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(one) if 'one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one) else 'one'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = [1, False, 'a']
    @py_assert3 = one(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=190)
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(one) if 'one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one) else 'one'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert3 = 0
    @py_assert2 = _ > @py_assert3
    @py_assert7 = [
     0, 1]
    @py_assert9 = one(@py_assert2, @py_assert7)
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=191)
    if not @py_assert9:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(one) if 'one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one) else 'one', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = None
    @py_assert3 = 0
    @py_assert2 = _ < @py_assert3
    @py_assert7 = [
     0, 1, 2]
    @py_assert9 = one(@py_assert2, @py_assert7)
    @py_assert11 = not @py_assert9
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=192)
    if not @py_assert11:
        @py_format5 = @pytest_ar._call_reprcompare(('<', ), (@py_assert2,), ('%(py1)s < %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format12 = ('' + 'assert not %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(one) if 'one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one) else 'one', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert3 = 0
    @py_assert2 = _ > @py_assert3
    @py_assert7 = [
     0, 1, 2]
    @py_assert9 = one(@py_assert2, @py_assert7)
    @py_assert11 = not @py_assert9
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=193)
    if not @py_assert11:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format12 = ('' + 'assert not %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(one) if 'one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(one) else 'one', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_none():
    @py_assert1 = [
     0, False]
    @py_assert3 = none(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=196)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(none) if 'none' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none) else 'none'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = 0
    @py_assert2 = _ < @py_assert3
    @py_assert7 = [
     0, -1]
    @py_assert9 = none(@py_assert2, @py_assert7)
    @py_assert11 = not @py_assert9
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=197)
    if not @py_assert11:
        @py_format5 = @pytest_ar._call_reprcompare(('<', ), (@py_assert2,), ('%(py1)s < %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format12 = ('' + 'assert not %(py10)s\n{%(py10)s = %(py0)s(%(py6)s, %(py8)s)\n}') % {'py6': @py_format5, 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(none) if 'none' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none) else 'none', 'py8': @pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_some():
    @py_assert1 = [
     0, '', 2, 3]
    @py_assert3 = some(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=200)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(some) if 'some' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(some) else 'some'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert3 = 3
    @py_assert2 = _ > @py_assert3
    @py_assert8 = 10
    @py_assert10 = range(@py_assert8)
    @py_assert12 = some(@py_assert2, @py_assert10)
    @py_assert15 = 4
    @py_assert14 = @py_assert12 == @py_assert15
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=201)
    if not @py_assert14:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (_, @py_assert3)) % {'py1': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py6)s, %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py16': @pytest_ar._saferepr(@py_assert15), 'py7': @pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range', 'py0': @pytest_ar._saferepr(some) if 'some' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(some) else 'some', 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @py_format5, 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert3 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_zipdict():
    @py_assert1 = [
     1, 2]
    @py_assert3 = 'ab'
    @py_assert5 = zipdict(@py_assert1, @py_assert3)
    @py_assert8 = {1: 'a', 2: 'b'}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=205)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(zipdict) if 'zipdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipdict) else 'zipdict'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 'ab'
    @py_assert4 = count()
    @py_assert6 = zipdict(@py_assert1, @py_assert4)
    @py_assert9 = {'a': 0, 'b': 1}
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=206)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py2)s, %(py5)s\n{%(py5)s = %(py3)s()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(zipdict) if 'zipdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zipdict) else 'zipdict', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_flip():
    @py_assert1 = {'a': 1, 'b': 2}
    @py_assert3 = flip(@py_assert1)
    @py_assert6 = {1: 'a', 2: 'b'}
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=209)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(flip) if 'flip' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(flip) else 'flip'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_project():
    @py_assert1 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert3 = 'ac'
    @py_assert5 = project(@py_assert1, @py_assert3)
    @py_assert8 = {'a': 1, 'c': 3}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=212)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(project) if 'project' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(project) else 'project'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    dd = defaultdict(int, {'a': 1, 'b': 2, 'c': 3})
    @py_assert3 = 'ac'
    @py_assert5 = project(dd, @py_assert3)
    @py_assert9 = {'a': 1, 'c': 3}
    @py_assert11 = defaultdict(int, @py_assert9)
    @py_assert13 = eq(@py_assert5, @py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=214)
    if not @py_assert13:
        @py_format15 = ('' + 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, %(py4)s)\n}, %(py12)s\n{%(py12)s = %(py7)s(%(py8)s, %(py10)s)\n})\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py7': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py1': @pytest_ar._saferepr(project) if 'project' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(project) else 'project', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(dd) if 'dd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dd) else 'dd', 'py14': @pytest_ar._saferepr(@py_assert13), 'py12': @pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert3 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_omit():
    @py_assert1 = {'a': 1, 'b': 2, 'c': 3}
    @py_assert3 = 'ac'
    @py_assert5 = omit(@py_assert1, @py_assert3)
    @py_assert8 = {'b': 2}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=217)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(omit) if 'omit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(omit) else 'omit'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    dd = defaultdict(int, {'a': 1, 'b': 2, 'c': 3})
    @py_assert3 = 'ac'
    @py_assert5 = omit(dd, @py_assert3)
    @py_assert9 = {'b': 2}
    @py_assert11 = defaultdict(int, @py_assert9)
    @py_assert13 = eq(@py_assert5, @py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=219)
    if not @py_assert13:
        @py_format15 = ('' + 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, %(py4)s)\n}, %(py12)s\n{%(py12)s = %(py7)s(%(py8)s, %(py10)s)\n})\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py7': @pytest_ar._saferepr(defaultdict) if 'defaultdict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(defaultdict) else 'defaultdict', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(eq) if 'eq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(eq) else 'eq', 'py8': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py1': @pytest_ar._saferepr(omit) if 'omit' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(omit) else 'omit', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(dd) if 'dd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dd) else 'dd', 'py14': @pytest_ar._saferepr(@py_assert13), 'py12': @pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert3 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_zip_values():
    @py_assert2 = {1: 10}
    @py_assert4 = {1: 20, 2: 30}
    @py_assert6 = zip_values(@py_assert2, @py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     (10, 20)]
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=222)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(zip_values) if 'zip_values' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zip_values) else 'zip_values', 'py9': @pytest_ar._saferepr(@py_assert8), 'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    with pytest.raises(TypeError):
        list(zip_values())


def test_zip_dicts():
    @py_assert2 = {1: 10}
    @py_assert4 = {1: 20, 2: 30}
    @py_assert6 = zip_dicts(@py_assert2, @py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     (1, (10, 20))]
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=226)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py1)s(%(py3)s, %(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(zip_dicts) if 'zip_dicts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(zip_dicts) else 'zip_dicts', 'py9': @pytest_ar._saferepr(@py_assert8), 'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    with pytest.raises(TypeError):
        list(zip_dicts())


def test_get_in():
    d = {'a': {'b': 'c', 
           'd': 'e', 
           'f': {'g': 'h'}}, 
     
     'i': 'j'}
    @py_assert2 = [
     'm']
    @py_assert4 = get_in(d, @py_assert2)
    @py_assert7 = None
    @py_assert6 = @py_assert4 is @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=241)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = ['m', 'n']
    @py_assert4 = 'foo'
    @py_assert6 = get_in(d, @py_assert2, @py_assert4)
    @py_assert9 = 'foo'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=242)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in', 'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = ['i']
    @py_assert4 = get_in(d, @py_assert2)
    @py_assert7 = 'j'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=243)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = ['a', 'b']
    @py_assert4 = get_in(d, @py_assert2)
    @py_assert7 = 'c'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=244)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = ['a', 'f', 'g']
    @py_assert4 = get_in(d, @py_assert2)
    @py_assert7 = 'h'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=245)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_get_in_list():
    @py_assert1 = [
     1, 2]
    @py_assert3 = [
     0]
    @py_assert5 = get_in(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=249)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [1, 2]
    @py_assert3 = [
     3]
    @py_assert5 = get_in(@py_assert1, @py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=250)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = {'x': [1, 2]}
    @py_assert3 = [
     'x', 1]
    @py_assert5 = get_in(@py_assert1, @py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=251)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(get_in) if 'get_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_in) else 'get_in'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_set_in():
    d = {'a': {'b': 1, 
           'c': 2}, 
     
     'd': 5}
    d2 = set_in(d, ['a', 'c'], 7)
    @py_assert0 = d['a']['c']
    @py_assert3 = 2
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=264)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = d2['a']['c']
    @py_assert3 = 7
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=265)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    d3 = set_in(d, ['e', 'f'], 42)
    @py_assert0 = d3['e']
    @py_assert3 = {'f': 42}
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=268)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = d3['a']
    @py_assert3 = d['a']
    @py_assert2 = @py_assert0 is @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=269)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_set_in_list():
    l = [{}, 1]
    l2 = set_in(l, [1], 7)
    @py_assert2 = [{}, 7]
    @py_assert1 = l2 == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=275)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (l2, @py_assert2)) % {'py0': @pytest_ar._saferepr(l2) if 'l2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l2) else 'l2', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = l2[0]
    @py_assert3 = l[0]
    @py_assert2 = @py_assert0 is @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=276)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_update_in():
    d = {'c': []}
    @py_assert2 = [
     'c']
    @py_assert5 = update_in(d, @py_assert2, len)
    @py_assert8 = {'c': 0}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=282)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py1)s, %(py3)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py4': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py0': @pytest_ar._saferepr(update_in) if 'update_in' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(update_in) else 'update_in', 'py1': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert8 = None
    d2 = update_in(d, ['a', 'b'], inc, default=0)
    @py_assert0 = d2['a']['b']
    @py_assert3 = 1
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=285)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = d2['c']
    @py_assert3 = d['c']
    @py_assert2 = @py_assert0 is @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=286)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_where():
    data = [
     {'a': 1, 'b': 2}, {'a': 10, 'b': 2}]
    @py_assert3 = 1
    @py_assert5 = where(data, a=@py_assert3)
    @py_assert8 = isinstance(@py_assert5, Iterator)
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=291)
    if not @py_assert8:
        @py_format10 = ('' + 'assert %(py9)s\n{%(py9)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, a=%(py4)s)\n}, %(py7)s)\n}') % {'py7': @pytest_ar._saferepr(Iterator) if 'Iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Iterator) else 'Iterator', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py1': @pytest_ar._saferepr(where) if 'where' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(where) else 'where', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py9': @pytest_ar._saferepr(@py_assert8)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert8 = None
    @py_assert3 = 1
    @py_assert5 = where(data, a=@py_assert3)
    @py_assert7 = list(@py_assert5)
    @py_assert10 = [
     {'a': 1, 'b': 2}]
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=292)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, a=%(py4)s)\n})\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(where) if 'where' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(where) else 'where', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_lwhere():
    data = [
     {'a': 1, 'b': 2}, {'a': 10, 'b': 2}]
    @py_assert2 = 1
    @py_assert4 = 2
    @py_assert6 = lwhere(data, a=@py_assert2, b=@py_assert4)
    @py_assert9 = [
     {'a': 1, 'b': 2}]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=296)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py1)s, a=%(py3)s, b=%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(lwhere) if 'lwhere' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lwhere) else 'lwhere', 'py1': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = 2
    @py_assert4 = lwhere(data, b=@py_assert2)
    @py_assert6 = @py_assert4 == data
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=297)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, b=%(py3)s)\n} == %(py7)s', ), (@py_assert4, data)) % {'py1': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py0': @pytest_ar._saferepr(lwhere) if 'lwhere' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lwhere) else 'lwhere', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = 1
    @py_assert4 = lwhere(data, c=@py_assert2)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=300)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, c=%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(lwhere) if 'lwhere' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lwhere) else 'lwhere', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_pluck():
    data = [
     {'a': 1, 'b': 2}, {'a': 10, 'b': 2}]
    @py_assert1 = 'a'
    @py_assert4 = lpluck(@py_assert1, data)
    @py_assert7 = [
     1, 10]
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=304)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(lpluck) if 'lpluck' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpluck) else 'lpluck', 'py3': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_pluck_attr():
    TestObj = namedtuple('TestObj', ('id', 'name'))
    objs = [TestObj(1, 'test1'), TestObj(5, 'test2'), TestObj(10, 'test3')]
    @py_assert1 = 'id'
    @py_assert4 = lpluck_attr(@py_assert1, objs)
    @py_assert7 = [
     1, 5, 10]
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=309)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(lpluck_attr) if 'lpluck_attr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lpluck_attr) else 'lpluck_attr', 'py3': @pytest_ar._saferepr(objs) if 'objs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(objs) else 'objs'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_invoke():
    @py_assert1 = [
     'abc', 'def', 'b']
    @py_assert3 = 'find'
    @py_assert5 = 'b'
    @py_assert7 = linvoke(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = [
     1, -1, 0]
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_colls.py', lineno=312)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(linvoke) if 'linvoke' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linvoke) else 'linvoke', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None