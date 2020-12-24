# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/simplified_dot_graph/test/test_line_parser.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 4733 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.graphviz.simplified_dot_graph.line_parser import LineParser
from vipe.graphviz.simplified_dot_graph.connection import Connection

def test_node_simple():
    check_node('"citation_matching" [label="cit"]', 'citation_matching')


def test_node_with_hyphen():
    check_node('"citation-matching-node" [label=""]', 'citation-matching-node')


def test_node_with_non_alpha_numeric_characters():
    check_node('"${workingDir}/citationmatching_chain/citation" [label="sf"]', '${workingDir}/citationmatching_chain/citation')


def test_node_extended():
    check_node('"citationmatching_chain" [label="" fillcolor=cyan,style=filled shape=box fixedsize=true width=0.1 height=0.1]', 'citationmatching_chain')
    check_node('"citationmatching_chain"[label="" fillcolor=cyan,style=filled shape=box fixedsize=true width=0.1 height=0.1]', 'citationmatching_chain')


def test_node_wrong_line():
    check_node('"node1" -> "node2"', None)
    check_node('"node1":"port1" -> "node2":"port2"', None)
    check_node('"node1" -> "node2" [label="something"]', None)
    check_node('      <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">', None)
    check_node('digraph {', None)
    check_node('rankdir=LR', None)


def test_connection_simple():
    check_connection('"node1" -> "node2"', Connection('node1', None, 'node2', None))
    check_connection('"node1":"port1" -> "node2":"port2"', Connection('node1', 'port1', 'node2', 'port2'))
    check_connection('"node1" -> "node2" [label="something"]', Connection('node1', None, 'node2', None))
    check_connection('"node1"  ->\t"node2" [label="something"]', Connection('node1', None, 'node2', None))


def test_connection_mixed_ports():
    check_connection('"node1":"document" -> "node2"', Connection('node1', 'document', 'node2', None))
    check_connection('"node1" -> "node2":"document"', Connection('node1', None, 'node2', 'document'))


def test_connection_with_hyphen():
    check_connection('"node-1" -> "my-node_here":"port-1"', Connection('node-1', None, 'my-node_here', 'port-1'))


def test_connection_with_non_alpha_numeric_characters():
    check_connection('"documentsclassification_main":"output_document_to_document_classes" -> "${workingDir}/documentsclassification_main/document_to_document_classes"', Connection('documentsclassification_main', 'output_document_to_document_classes', '${workingDir}/documentsclassification_main/document_to_document_classes', None))
    check_connection('"${workingDir}/citationmatching_chain/citation" -> "transformers_statistics":"input_citation"', Connection('${workingDir}/citationmatching_chain/citation', None, 'transformers_statistics', 'input_citation'))


def test_connection_wrong_line():
    check_connection('"citation_matching" [label="cit"]', None)
    check_connection('"citationmatching_chain" [label="" fillcolor=cyan,style=filled shape=box fixedsize=true width=0.1 height=0.1]', None)
    check_connection('"citationmatching_chain"[label="" fillcolor=cyan]', None)
    check_connection('digraph {', None)
    check_connection('rankdir=LR', None)


def check_node(line, expected_node):
    actual_node = LineParser.parse_node(line)
    if expected_node is None:
        @py_assert2 = None
        @py_assert1 = actual_node is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (actual_node, @py_assert2)) % {'py0': @pytest_ar._saferepr(actual_node) if 'actual_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_node) else 'actual_node',  'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = expected_node == actual_node
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_node, actual_node)) % {'py0': @pytest_ar._saferepr(expected_node) if 'expected_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_node) else 'expected_node',  'py2': @pytest_ar._saferepr(actual_node) if 'actual_node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_node) else 'actual_node'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


def check_connection(line, expected_connection):
    actual_connection = LineParser.parse_connection(line)
    if expected_connection is None:
        @py_assert2 = None
        @py_assert1 = actual_connection is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (actual_connection, @py_assert2)) % {'py0': @pytest_ar._saferepr(actual_connection) if 'actual_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_connection) else 'actual_connection',  'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = expected_connection == actual_connection
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_connection, actual_connection)) % {'py0': @pytest_ar._saferepr(expected_connection) if 'expected_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_connection) else 'expected_connection',  'py2': @pytest_ar._saferepr(actual_connection) if 'actual_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_connection) else 'actual_connection'}
            @py_format5 = (@pytest_ar._format_assertmsg('{} != {}'.format(expected_connection, actual_connection)) + '\n>assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None