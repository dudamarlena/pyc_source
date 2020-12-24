# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 23881 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from paleomix.common.formats.newick import GraphError, Newick, NewickError, NewickParseError

def test_newick__constructor__name():
    node = Newick(name='AbC')
    @py_assert1 = node.name
    @py_assert4 = 'AbC'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=39)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_newick__constructor__children_set_in_internal_nodes():
    node = Newick(name='Leaf')
    top_node = Newick(children=[node])
    @py_assert1 = top_node.children
    @py_assert4 = (
     node,)
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=45)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.children\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_newick__constructor__children_not_set_in_leaf_nodes():
    node = Newick(name='Leaf')
    @py_assert1 = node.children
    @py_assert4 = ()
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=50)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.children\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_newick__constructor__is_leaf_true_for_leaf_nodes():
    node = Newick(name='Another Leaf')
    @py_assert1 = node.is_leaf
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=55)
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s.is_leaf\n}' % {'py0':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def test_newick__constructor__is_leaf_false_for_internal_nodes():
    node = Newick(name='Leaf')
    top_node = Newick(children=[node])
    @py_assert1 = top_node.is_leaf
    @py_assert3 = not @py_assert1
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=61)
    if not @py_assert3:
        @py_format4 = 'assert not %(py2)s\n{%(py2)s = %(py0)s.is_leaf\n}' % {'py0':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


def test_newick__constuctor__leaf_nodes_must_have_name_or_length():
    with pytest.raises(NewickError):
        Newick(children=None)


def test_newick__constructor__internal_nodes_must_have_children():
    with pytest.raises(NewickError):
        Newick(children=[])


def test_newick__constructor__children_must_be_newick():
    with pytest.raises(TypeError):
        Newick(children=['A', 'B'])


def test_newick__get_leaf_nodes__leaf_returns_self():
    node = Newick(name='Leaf')
    @py_assert2 = node.get_leaf_nodes
    @py_assert4 = @py_assert2()
    @py_assert6 = list(@py_assert4)
    @py_assert10 = [
     node]
    @py_assert12 = list(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=86)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get_leaf_nodes\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_newick__get_leaf_nodes__internal_node_returns_leaf_nodes():
    node_a = Newick(name='Leaf A')
    node_b = Newick(name='Leaf B')
    top_node = Newick(children=[node_a, node_b])
    @py_assert2 = top_node.get_leaf_nodes
    @py_assert4 = @py_assert2()
    @py_assert6 = list(@py_assert4)
    @py_assert10 = [
     node_a, node_b]
    @py_assert12 = list(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=93)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get_leaf_nodes\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_newick__get_leaf_nodes__complex_case():
    node_a = Newick(name='Leaf A')
    node_b = Newick(name='Leaf B')
    node_c = Newick(name='Leaf C')
    sub_a = Newick(children=[node_b, node_c])
    top_node = Newick(children=[node_a, sub_a])
    @py_assert2 = top_node.get_leaf_nodes
    @py_assert4 = @py_assert2()
    @py_assert6 = list(@py_assert4)
    @py_assert10 = [
     node_a, node_b, node_c]
    @py_assert12 = list(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=102)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get_leaf_nodes\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_newick__get_leaf_names__leaf_returns_self():
    node = Newick(name='Leaf')
    @py_assert2 = node.get_leaf_names
    @py_assert4 = @py_assert2()
    @py_assert6 = list(@py_assert4)
    @py_assert10 = [
     'Leaf']
    @py_assert12 = list(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=112)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get_leaf_names\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_newick__get_leaf_names__internal_node_returns_leaf_nodes():
    node_a = Newick(name='Leaf A')
    node_b = Newick(name='Leaf B')
    top_node = Newick(children=[node_a, node_b])
    @py_assert2 = top_node.get_leaf_names
    @py_assert4 = @py_assert2()
    @py_assert6 = list(@py_assert4)
    @py_assert10 = [
     'Leaf A', 'Leaf B']
    @py_assert12 = list(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=119)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get_leaf_names\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_newick__get_leaf_names__complex_case():
    node_a = Newick(name='Leaf A')
    node_b = Newick(name='Leaf B')
    node_c = Newick(name='Leaf C')
    sub_a = Newick(children=[node_b, node_c])
    top_node = Newick(children=[node_a, sub_a])
    @py_assert2 = top_node.get_leaf_names
    @py_assert4 = @py_assert2()
    @py_assert6 = list(@py_assert4)
    @py_assert10 = [
     'Leaf A', 'Leaf B', 'Leaf C']
    @py_assert12 = list(@py_assert10)
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=128)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.get_leaf_names\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_newick__reroot_on_taxa__single_taxa():
    source = Newick.from_string('((A,B),C);')
    expected = Newick.from_string('((B,C),A);')
    @py_assert3 = source.reroot_on_taxa
    @py_assert5 = 'A'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = expected == @py_assert7
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=139)
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.reroot_on_taxa\n}(%(py6)s)\n}', ), (expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__reroot_on_taxa__single_taxa_with_branch_lengths():
    source = Newick.from_string('((A:4,B:3):2,C:1);')
    expected = Newick.from_string('((B:3,C:3.0):2.0,A:2.0);')
    @py_assert3 = source.reroot_on_taxa
    @py_assert5 = 'A'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = expected == @py_assert7
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=145)
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.reroot_on_taxa\n}(%(py6)s)\n}', ), (expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__reroot_on_taxa__multiple_taxa__clade():
    source = Newick.from_string('((A,(B,C)),(D,E));')
    expected = Newick.from_string('(((D,E),A),(B,C));')
    @py_assert3 = source.reroot_on_taxa
    @py_assert5 = ('B', 'C')
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = expected == @py_assert7
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=151)
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.reroot_on_taxa\n}(%(py6)s)\n}', ), (expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__reroot_on_taxa__multiple_taxa__paraphylogeny():
    source = Newick.from_string('((B,C),((D,E),A));')
    expected = Newick.from_string('(((B,C),A),(D,E));')
    @py_assert3 = source.reroot_on_taxa
    @py_assert5 = ('A', 'C')
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = expected == @py_assert7
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=157)
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.reroot_on_taxa\n}(%(py6)s)\n}', ), (expected, @py_assert7)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__reroot_on_taxa__no_taxa():
    source = Newick.from_string('((B,C),((D,E),A));')
    with pytest.raises(ValueError):
        source.reroot_on_taxa(())


def test_newick__reroot_on_taxa__unknown_taxa():
    source = Newick.from_string('((B,C),((D,E),A));')
    with pytest.raises(ValueError):
        source.reroot_on_taxa(('A', 'Z'))


def test_newick__reroot_on_taxa__no_non_root_taxa():
    source = Newick.from_string('((B,C),((D,E),A));')
    with pytest.raises(ValueError):
        source.reroot_on_taxa(('A', 'B', 'C', 'D', 'E'))


def test_newick__reroot_on_midpoint__single_node():
    source = Newick.from_string('(A:3.0);')
    expected = Newick.from_string('(A:3.0);')
    @py_assert3 = source.reroot_on_midpoint
    @py_assert5 = @py_assert3()
    @py_assert1 = expected == @py_assert5
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=186)
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.reroot_on_midpoint\n}()\n}', ), (expected, @py_assert5)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_newick__reroot_on_midpoint__two_nodes():
    source = Newick.from_string('(A:3.0,B:8.0);')
    rerooted = source.reroot_on_midpoint()
    expected = Newick.from_string('(A:5.5,B:5.5);')
    @py_assert1 = expected == rerooted
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=193)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, rerooted)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(rerooted) if 'rerooted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rerooted) else 'rerooted'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__reroot_on_midpoint__two_clades():
    source = Newick.from_string('((A:7,B:2):1,(C:1,D:0.5):2);')
    rerooted = source.reroot_on_midpoint()
    expected = Newick.from_string('(((C:1,D:0.5):3.0,B:2):1.5,A:5.5);')
    @py_assert1 = expected == rerooted
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=200)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, rerooted)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(rerooted) if 'rerooted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rerooted) else 'rerooted'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__reroot_on_midpoint__nested_clades():
    source = Newick.from_string('((A:2,(B:2,C:3):4):1,(D:1,E:0.5):2);')
    rerooted = source.reroot_on_midpoint()
    expected = Newick.from_string('(((D:1,E:0.5):3.0,A:2):1.5,(B:2,C:3):2.5);')
    @py_assert1 = expected == rerooted
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=207)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, rerooted)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(rerooted) if 'rerooted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rerooted) else 'rerooted'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__reroot_on_midpoint__reroot_on_internal_node():
    source = Newick.from_string('((A:5.0,B:1.0)C:2.0,D:3.0);')
    rerooted = source.reroot_on_midpoint()
    expected = Newick.from_string('(A:5.0,B:1.0,D:5.0)C;')
    @py_assert1 = expected == rerooted
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=214)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, rerooted)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(rerooted) if 'rerooted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rerooted) else 'rerooted'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


_INVALID_BRANCH_LENGTHS = ('(A,B);', '(A:7,B);', '(A:7,(B:3));', '(A:7,(B:3):-1);',
                           '(A:7,B:-1);')

@pytest.mark.parametrize('newick', _INVALID_BRANCH_LENGTHS)
def test_newick__reroot_on_midpoint__invalid_branch_lengths(newick):
    source = Newick.from_string(newick)
    with pytest.raises(GraphError):
        source.reroot_on_midpoint()


def test_newick__add_support__no_trees():
    main_tree = Newick.from_string('(((A,B),C),D);')
    expected = Newick.from_string('(((A,B)0,C)0,D);')
    result = main_tree.add_support([])
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=242)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__single_identical_tree():
    main_tree = Newick.from_string('(((A,B),C),D);')
    bootstraps = [Newick.from_string('(((A,B),C),D);')]
    expected = Newick.from_string('(((A,B)1,C)1,D);')
    result = main_tree.add_support(bootstraps)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=250)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__single_identical_tree__different_rooting():
    main_tree = Newick.from_string('(((A,B),C),D);')
    bootstraps = [Newick.from_string('(((C,D),B),A);')]
    expected = Newick.from_string('(((A,B)1,C)1,D);')
    result = main_tree.add_support(bootstraps)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=258)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__multiple_trees__different_topologies():
    main_tree = Newick.from_string('(((A,B),C),D);')
    bootstraps = [
     Newick.from_string('(((C,B),D),A);'),
     Newick.from_string('(((A,D),B),C);')]
    expected = Newick.from_string('(((A,B)0,C)2,D);')
    result = main_tree.add_support(bootstraps)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=269)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__multiple_trees__partially_different_topologies():
    main_tree = Newick.from_string('(((A,B),C),D);')
    bootstraps = [
     Newick.from_string('(((C,D),A),B);'),
     Newick.from_string('(((A,D),B),C);')]
    expected = Newick.from_string('(((A,B)1,C)2,D);')
    result = main_tree.add_support(bootstraps)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=280)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__multiple_trees__two_cladees():
    main_tree = Newick.from_string('((A,B),(C,(D,E)));')
    bootstraps = [
     Newick.from_string('((((C,E),D),A),B);'),
     Newick.from_string('(((A,(C,D)),B),E);')]
    expected = Newick.from_string('((A,B)1,(C,(D,E)0)1);')
    result = main_tree.add_support(bootstraps)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=291)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__differing_leaf_names():
    main_tree = Newick.from_string('(((A,B),C),D);')
    bootstraps = [Newick.from_string('(((C,E),B),A);')]
    with pytest.raises(NewickError):
        main_tree.add_support(bootstraps)


_ADD_SUPPORT_FORMATTING = (('{Support}', '(((A,B)1,C)3,D);'), ('{Percentage:.0f}', '(((A,B)33,C)100,D);'),
                           ('{Fraction:.2f}', '(((A,B)0.33,C)1.00,D);'))

@pytest.mark.parametrize('fmt, expected', _ADD_SUPPORT_FORMATTING)
def test_newick__add_support__formatting(fmt, expected):
    main_tree = Newick.from_string('(((A,B),C),D);')
    bootstraps = [
     Newick.from_string('(((C,D),A),B);'),
     Newick.from_string('(((C,B),A),D);'),
     Newick.from_string('(((A,D),B),C);')]
    expected = Newick.from_string(expected)
    result = main_tree.add_support(bootstraps, fmt)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=318)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__add_support__unique_names_required():
    main_tree = Newick.from_string('(((A,B),C),A);')
    bootstraps = [Newick.from_string('(((A,B),C),A);')]
    with pytest.raises(NewickError):
        main_tree.add_support(bootstraps)


def test_newick__parse__minimal_newick__name_only():
    top_node = Newick(name='A')
    @py_assert1 = Newick.from_string
    @py_assert3 = 'A;'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=335)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__parse__single_taxa():
    child_node = Newick(name='Ab')
    top_node = Newick(children=[child_node])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(Ab);'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=341)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__parse__two_taxa():
    child_node_1 = Newick(name='A')
    child_node_2 = Newick(name='Bc')
    top_node = Newick(children=[child_node_1, child_node_2])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,Bc);'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=348)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__parse__three_taxa():
    child_node_1 = Newick(name='A')
    child_node_2 = Newick(name='Bc')
    child_node_3 = Newick(name='DeF')
    top_node = Newick(children=[child_node_1, child_node_2, child_node_3])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,Bc,DeF);'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=356)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__parse__ignore_whitespace():
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,B);'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = Newick.from_string
    @py_assert11 = '(A, B);'
    @py_assert13 = @py_assert9(@py_assert11)
    @py_assert7 = @py_assert5 == @py_assert13
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=360)
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py14)s\n{%(py14)s = %(py10)s\n{%(py10)s = %(py8)s.from_string\n}(%(py12)s)\n}', ), (@py_assert5, @py_assert13)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_newick__parse__missing_semicolon():
    with pytest.raises(NewickParseError):
        Newick.from_string('()')


def test_newick__parse__subnode__single_taxa():
    child_node_1 = Newick(name='A')
    child_node_2a = Newick(name='B')
    child_node_2 = Newick(children=[child_node_2a])
    top_node = Newick(children=[child_node_1, child_node_2])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,(B));'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=373)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__parse__subnode__two_taxa():
    child_node_1 = Newick(name='A')
    child_node_2a = Newick(name='B')
    child_node_2b = Newick(name='C')
    child_node_2 = Newick(children=[child_node_2a, child_node_2b])
    top_node = Newick(children=[child_node_1, child_node_2])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,(B,C));'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=382)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__cmp__identical():
    node_a = Newick(name='A', length=13, children=[Newick(name='B')])
    node_b = Newick(name='A', length=13, children=[Newick(name='B')])
    @py_assert1 = node_a == node_b
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=393)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (node_a, node_b)) % {'py0':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a',  'py2':@pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__cmp__identical_for_empty_string_length():
    node_a = Newick(name='A', length='', children=[Newick(name='B')])
    node_b = Newick(name='A', length=None, children=[Newick(name='B')])
    @py_assert1 = node_a == node_b
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=399)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (node_a, node_b)) % {'py0':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a',  'py2':@pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__cmp__identical_for_empty_string_name():
    node_a = Newick(name='', length=13, children=[Newick(name='B')])
    node_b = Newick(name=None, length=13, children=[Newick(name='B')])
    @py_assert1 = node_a == node_b
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=405)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (node_a, node_b)) % {'py0':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a',  'py2':@pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


_CMP_NOT_IDENTICAL = (
 Newick(name='B', length=13, children=[Newick(name='B')]),
 Newick(name='A', length=14, children=[Newick(name='B')]),
 Newick(name='A', length=13, children=[]),
 Newick(name='A', length=13, children=[Newick(name='C')]),
 Newick(name='B', length=14, children=[Newick(name='C')]))

@pytest.mark.parametrize('node_b', _CMP_NOT_IDENTICAL)
def test_newick__cmp__not_identical(node_b):
    node_a = Newick(name='A', length=13, children=[Newick(name='B')])
    @py_assert1 = node_a != node_b
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=420)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (node_a, node_b)) % {'py0':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a',  'py2':@pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_newick__hash__identical():
    node_a = Newick(name='A', length=13, children=[Newick(name='B')])
    node_b = Newick(name='A', length=13, children=[Newick(name='B')])
    @py_assert2 = hash(node_a)
    @py_assert7 = hash(node_b)
    @py_assert4 = @py_assert2 == @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=431)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None


_HASH_NOT_IDENTICAL = (
 Newick(name='B', length=13, children=[Newick(name='B')]),
 Newick(name='A', length=14, children=[Newick(name='B')]),
 Newick(name='A', length=13, children=[]),
 Newick(name='A', length=13, children=[Newick(name='C')]),
 Newick(name='B', length=14, children=[Newick(name='C')]))

@pytest.mark.parametrize('node_b', _CMP_NOT_IDENTICAL)
def test_newick__hash__not_identical(node_b):
    node_a = Newick(name='A', length=13, children=[Newick(name='B')])
    @py_assert2 = hash(node_a)
    @py_assert7 = hash(node_b)
    @py_assert4 = @py_assert2 != @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=446)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} != %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None


def test_newick__hash__hashable():
    key_a = Newick(name='A', length=13.7, children=[Newick(name='F')])
    key_b = Newick(name='A', length=13.7, children=[Newick(name='F')])
    @py_assert2 = {key_a: True}
    @py_assert1 = key_b in @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=452)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (key_b, @py_assert2)) % {'py0':@pytest_ar._saferepr(key_b) if 'key_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key_b) else 'key_b',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_newick__malformed__unbalanced_parantheses():
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B,C);')


def test_newick__malformed__mismatched_parantheses():
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B,C();')


def test_newick__malformed__missing_parantheses():
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B,C))')


def test_newick__malformed__missing_length():
    with pytest.raises(NewickParseError):
        Newick.from_string('(A:,(B,C));')
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B:,C));')
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B,C:));')
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B,C):);')
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,(B,C)):;')


def test_newick__malformed__multiple_lengths():
    with pytest.raises(NewickParseError):
        Newick.from_string('(A:1:2);')


def test_newick__parse__first_taxa_unnamed():
    with pytest.raises(NewickError):
        Newick.from_string('(,A);')


def test_newick__parse__second_taxa_unnamed():
    with pytest.raises(NewickError):
        Newick.from_string('(A,);')


def test_newick__parse__two_taxa_unnamed():
    with pytest.raises(NewickError):
        Newick.from_string('(,);')


def test_newick__parse__three_taxa_unnamed():
    with pytest.raises(NewickError):
        Newick.from_string('(,,);')


def test_newick__parse__minimal_newick__implicit_nodes():
    with pytest.raises(NewickParseError):
        Newick.from_string('();')


def test_newick__parse__subnode__empty():
    with pytest.raises(NewickParseError):
        Newick.from_string('(A,());')


def test_newick__wikipedia_example_1():
    with pytest.raises(NewickError):
        Newick.from_string('(,,(,));')


def test_newick__wikipedia_example_2():
    taxa_d = Newick(name='D')
    taxa_c = Newick(name='C')
    taxa_sub = Newick(children=[taxa_c, taxa_d])
    taxa_b = Newick(name='B')
    taxa_a = Newick(name='A')
    top_node = Newick(children=[taxa_a, taxa_b, taxa_sub])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,B,(C,D));'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=553)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__wikipedia_example_3():
    taxa_d = Newick(name='D')
    taxa_c = Newick(name='C')
    taxa_sub = Newick(children=[taxa_c, taxa_d], name='E')
    taxa_b = Newick(name='B')
    taxa_a = Newick(name='A')
    top_node = Newick(children=[taxa_a, taxa_b, taxa_sub], name='F')
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A,B,(C,D)E)F;'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=564)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__wikipedia_example_4():
    taxa_d = Newick(length='0.4')
    taxa_c = Newick(length='0.3')
    taxa_sub = Newick(children=[taxa_c, taxa_d], length='0.5')
    taxa_b = Newick(length='0.2')
    taxa_a = Newick(length='0.1')
    top_node = Newick(children=[taxa_a, taxa_b, taxa_sub])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(:0.1,:0.2,(:0.3,:0.4):0.5);'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=575)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__wikipedia_example_5():
    taxa_d = Newick(length='0.4')
    taxa_c = Newick(length='0.3')
    taxa_sub = Newick(children=[taxa_c, taxa_d], length='0.5')
    taxa_b = Newick(length='0.2')
    taxa_a = Newick(length='0.1')
    top_node = Newick(children=[taxa_a, taxa_b, taxa_sub], length='0.0')
    @py_assert1 = Newick.from_string
    @py_assert3 = '(:0.1,:0.2,(:0.3,:0.4):0.5):0.0;'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=586)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__wikipedia_example_6():
    taxa_d = Newick(length='0.4', name='D')
    taxa_c = Newick(length='0.3', name='C')
    taxa_sub = Newick(children=[taxa_c, taxa_d], length='0.5')
    taxa_b = Newick(length='0.2', name='B')
    taxa_a = Newick(length='0.1', name='A')
    top_node = Newick(children=[taxa_a, taxa_b, taxa_sub])
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=597)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__wikipedia_example_7():
    taxa_d = Newick(length='0.4', name='D')
    taxa_c = Newick(length='0.3', name='C')
    taxa_sub = Newick(children=[taxa_c, taxa_d], length='0.5', name='E')
    taxa_b = Newick(length='0.2', name='B')
    taxa_a = Newick(length='0.1', name='A')
    top_node = Newick(children=[taxa_a, taxa_b, taxa_sub], name='F')
    @py_assert1 = Newick.from_string
    @py_assert3 = '(A:0.1,B:0.2,(C:0.3,D:0.4)E:0.5)F;'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == top_node
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=608)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, top_node)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__wikipedia_example_8():
    taxa_b = Newick(length='0.2', name='B')
    taxa_c = Newick(length='0.3', name='C')
    taxa_d = Newick(length='0.4', name='D')
    node_e = Newick(length='0.5', name='E', children=[taxa_c, taxa_d])
    node_f = Newick(length='0.1', name='F', children=[taxa_b, node_e])
    node_a = Newick(name='A', children=[node_f])
    @py_assert1 = Newick.from_string
    @py_assert3 = '((B:0.2,(C:0.3,D:0.4)E:0.5)F:0.1)A;'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == node_a
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=619)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_string\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, node_a)) % {'py0':@pytest_ar._saferepr(Newick) if 'Newick' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Newick) else 'Newick',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_newick__str__non_string_name():
    node = Newick(children=[Newick(name=17, length='1.3')])
    @py_assert2 = str(node)
    @py_assert5 = '(17:1.3);'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=629)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_newick__str__non_string_length():
    node = Newick(children=[Newick(name='Foo', length=1.3)])
    @py_assert2 = str(node)
    @py_assert5 = '(Foo:1.3);'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=634)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_newick__str__repr_equal_to_str():
    node_a = Newick(name='A', length='123')
    node_b = Newick(name='B', length='4567')
    top_node = Newick(children=[node_a, node_b])
    @py_assert2 = str(top_node)
    @py_assert5 = '(A:123,B:4567);'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=641)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_newick__str__single_leaf_should_not_be_followed_by_comma():
    node = Newick(name='A')
    top_node = Newick(children=[node])
    @py_assert2 = str(top_node)
    @py_assert5 = '(A);'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=647)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(top_node) if 'top_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(top_node) else 'top_node',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


_STR_EQUALITY = ('(A,B,(C,D));', '(A,B,(C,D)E)F;', '(:0.1,:0.2,(:0.3,:0.4):0.5);',
                 '(:0.1,:0.2,(:0.3,:0.4):0.5):0.0;', '(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);',
                 '(A:0.1,B:0.2,(C:0.3,D:0.4)E:0.5)F;')

@pytest.mark.parametrize('nwk_str', _STR_EQUALITY)
def test_newick__wikipedia_examples__str_equality(nwk_str):
    nodes = Newick.from_string(nwk_str)
    result = str(nodes)
    @py_assert1 = result == nwk_str
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/newick_test.py', lineno=670)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, nwk_str)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(nwk_str) if 'nwk_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nwk_str) else 'nwk_str'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


_PROPERTIES_ARE_IMMUTABLE = (
 ('name', 'foo'),
 ('length', '13'),
 (
  'children', []),
 ('foobar', True))

@pytest.mark.parametrize('name, value', _PROPERTIES_ARE_IMMUTABLE)
def test_newick__properties_are_immutable(name, value):
    node = Newick(name='A', length=3, children=[Newick(name='B')])
    with pytest.raises(NotImplementedError):
        setattr(node, name, value)


@pytest.mark.parametrize('name', ('name', 'length', 'children', 'foobar'))
def test_newick__properties_cannot_be_deleted(name):
    node = Newick(name='A', length=3, children=[Newick(name='B')])
    with pytest.raises(NotImplementedError):
        delattr(node, name)