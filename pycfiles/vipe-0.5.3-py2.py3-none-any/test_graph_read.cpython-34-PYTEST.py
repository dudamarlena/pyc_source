# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/simplified_dot_graph/test/test_graph_read.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 1845 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.common.utils import read_as_string
from vipe.graphviz.simplified_dot_graph.graph import SimplifiedDotGraph
from vipe.graphviz.simplified_dot_graph.connection import Connection

def test_simple():
    check('data/simple.dot', create_simple_graph())


def test_no_digraph_wrapping():
    check('data/no_digraph_wrapping.dot', create_simple_graph())


def test_nodes_not_defined_explicitly():
    check('data/nodes_not_defined_explicitly.dot', create_simple_graph())


def test_html_node():
    check('data/html_node.dot', SimplifiedDotGraph({
     'node1', 'node2'}, {
     Connection('node1', None, 'node2', None)}))


def create_simple_graph():
    return SimplifiedDotGraph({
     'node1', 'node2', 'node3'}, {
     Connection('node1', 'p1', 'node2', 'p21'),
     Connection('node3', 'p3', 'node2', 'p23'),
     Connection('node2', None, 'node3', None),
     Connection('node2', 'p2', 'node1', None)})


def check(relative_input_path, expected_graph):
    input_dot = read_as_string(__name__, relative_input_path)
    actual_graph = SimplifiedDotGraph.from_dot(input_dot)
    @py_assert1 = expected_graph == actual_graph
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_graph, actual_graph)) % {'py0': @pytest_ar._saferepr(expected_graph) if 'expected_graph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_graph) else 'expected_graph',  'py2': @pytest_ar._saferepr(actual_graph) if 'actual_graph' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_graph) else 'actual_graph'}
        @py_format5 = (@pytest_ar._format_assertmsg('{} != {}'.format(expected_graph, actual_graph)) + '\n>assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None