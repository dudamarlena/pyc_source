# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_tree.py
# Compiled at: 2018-10-03 08:49:11
# Size of source mod 2**32: 619 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from whatever import _
from funcy import rest
from funcy.tree import *

def test_tree_leaves():
    @py_assert1 = [
     1, 2, [3, [4]], 5]
    @py_assert3 = ltree_leaves(@py_assert1)
    @py_assert6 = [
     1, 2, 3, 4, 5]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=8)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(ltree_leaves) if 'ltree_leaves' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_leaves) else 'ltree_leaves'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = ltree_leaves(@py_assert1)
    @py_assert6 = [
     1]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=9)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(ltree_leaves) if 'ltree_leaves' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_leaves) else 'ltree_leaves'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 3
    @py_assert5 = 1
    @py_assert4 = _ > @py_assert5
    @py_assert10 = ltree_leaves(@py_assert1, follow=@py_assert4, children=range)
    @py_assert13 = [
     0, 1, 0, 1]
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=11)
    if not @py_assert12:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s > %(py6)s', ), (_, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_'}
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py2)s, follow=%(py8)s, children=%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(ltree_leaves) if 'ltree_leaves' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_leaves) else 'ltree_leaves', 'py8': @py_format7, 'py14': @pytest_ar._saferepr(@py_assert13), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range'}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = [1, [2, [3, 4], 5], 6]
    @py_assert4 = ltree_leaves(@py_assert1, children=rest)
    @py_assert7 = [
     4, 5, 6]
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=12)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, children=%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(ltree_leaves) if 'ltree_leaves' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_leaves) else 'ltree_leaves', 'py3': @pytest_ar._saferepr(rest) if 'rest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rest) else 'rest'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_tree_nodes():
    @py_assert1 = [
     1, 2, [3, [4]], 5]
    @py_assert3 = ltree_nodes(@py_assert1)
    @py_assert6 = [
     [
      1, 2, [3, [4]], 5], 1, 2, [3, [4]], 3, [4], 4, 5]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=16)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(ltree_nodes) if 'ltree_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_nodes) else 'ltree_nodes'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = ltree_nodes(@py_assert1)
    @py_assert6 = [
     1]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=22)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(ltree_nodes) if 'ltree_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_nodes) else 'ltree_nodes'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 3
    @py_assert5 = 1
    @py_assert4 = _ > @py_assert5
    @py_assert10 = ltree_nodes(@py_assert1, follow=@py_assert4, children=range)
    @py_assert13 = [
     3, 0, 1, 2, 0, 1]
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_tree.py', lineno=23)
    if not @py_assert12:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s > %(py6)s', ), (_, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(_) if '_' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_) else '_'}
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py2)s, follow=%(py8)s, children=%(py9)s)\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(ltree_nodes) if 'ltree_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ltree_nodes) else 'ltree_nodes', 'py8': @py_format7, 'py14': @pytest_ar._saferepr(@py_assert13), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range'}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert13 = None