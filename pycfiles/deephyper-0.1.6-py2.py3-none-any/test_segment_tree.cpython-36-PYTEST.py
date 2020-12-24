# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 2712 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from deephyper.search.nas.baselines.common.segment_tree import SumSegmentTree, MinSegmentTree

def test_tree_set():
    tree = SumSegmentTree(4)
    tree[2] = 1.0
    tree[3] = 3.0
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = @py_assert4()
    @py_assert8 = 4.0
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=12)
    if not @py_assert10:
        @py_format12 = 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}()\n}, %(py9)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 0
    @py_assert8 = 2
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 0.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=13)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 0
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 1.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=14)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 2
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 1.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=15)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 2
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert11 = @py_assert4(@py_assert6, @py_assert10)
    @py_assert13 = 1.0
    @py_assert15 = @py_assert1(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=16)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, -%(py9)s)\n}, %(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 2
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 4.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=17)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_tree_set_overlap():
    tree = SumSegmentTree(4)
    tree[2] = 1.0
    tree[2] = 3.0
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = @py_assert4()
    @py_assert8 = 3.0
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=26)
    if not @py_assert10:
        @py_format12 = 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}()\n}, %(py9)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 2
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 3.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=27)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 2
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert11 = @py_assert4(@py_assert6, @py_assert10)
    @py_assert13 = 3.0
    @py_assert15 = @py_assert1(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=28)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, -%(py9)s)\n}, %(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 2
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 3.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=29)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.sum
    @py_assert6 = 1
    @py_assert8 = 2
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 0.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=30)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_prefixsum_idx():
    tree = SumSegmentTree(4)
    tree[2] = 1.0
    tree[3] = 3.0
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 0.0
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=39)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 0.5
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=40)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 0.99
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=41)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 1.01
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=42)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 3.0
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=43)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 4.0
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=44)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_prefixsum_idx2():
    tree = SumSegmentTree(4)
    tree[0] = 0.5
    tree[1] = 1.0
    tree[2] = 1.0
    tree[3] = 3.0
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 0.0
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=55)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 0.55
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=56)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 0.99
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=57)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 1.51
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=58)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 3.0
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=59)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = tree.find_prefixsum_idx
    @py_assert3 = 5.5
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 3
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=60)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.find_prefixsum_idx\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_max_interval_tree():
    tree = MinSegmentTree(4)
    tree[0] = 1.0
    tree[2] = 0.5
    tree[3] = 3.0
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = @py_assert4()
    @py_assert8 = 0.5
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=70)
    if not @py_assert10:
        @py_format12 = 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}()\n}, %(py9)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 2
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 1.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=71)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 0.5
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=72)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert11 = @py_assert4(@py_assert6, @py_assert10)
    @py_assert13 = 0.5
    @py_assert15 = @py_assert1(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=73)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, -%(py9)s)\n}, %(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 2
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 0.5
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=74)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 3
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 3.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=75)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    tree[2] = 0.7
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = @py_assert4()
    @py_assert8 = 0.7
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=79)
    if not @py_assert10:
        @py_format12 = 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}()\n}, %(py9)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 2
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 1.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=80)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 0.7
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=81)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert11 = @py_assert4(@py_assert6, @py_assert10)
    @py_assert13 = 0.7
    @py_assert15 = @py_assert1(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=82)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, -%(py9)s)\n}, %(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 2
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 0.7
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=83)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 3
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 3.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=84)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    tree[2] = 4.0
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = @py_assert4()
    @py_assert8 = 1.0
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=88)
    if not @py_assert10:
        @py_format12 = 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}()\n}, %(py9)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 2
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 1.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=89)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 1.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=90)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 0
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert11 = @py_assert4(@py_assert6, @py_assert10)
    @py_assert13 = 1.0
    @py_assert15 = @py_assert1(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=91)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, -%(py9)s)\n}, %(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 2
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 3.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=92)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 2
    @py_assert8 = 3
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 4.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=93)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 2
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert11 = @py_assert4(@py_assert6, @py_assert10)
    @py_assert13 = 4.0
    @py_assert15 = @py_assert1(@py_assert11, @py_assert13)
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=94)
    if not @py_assert15:
        @py_format17 = 'assert %(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, -%(py9)s)\n}, %(py14)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = np.isclose
    @py_assert4 = tree.min
    @py_assert6 = 3
    @py_assert8 = 4
    @py_assert10 = @py_assert4(@py_assert6, @py_assert8)
    @py_assert12 = 3.0
    @py_assert14 = @py_assert1(@py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_segment_tree.py', lineno=95)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py3)s.min\n}(%(py7)s, %(py9)s)\n}, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tree) if 'tree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tree) else 'tree',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


if __name__ == '__main__':
    test_tree_set()
    test_tree_set_overlap()
    test_prefixsum_idx()
    test_prefixsum_idx2()
    test_max_interval_tree()