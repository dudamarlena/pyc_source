# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_graph_vertex.py
# Compiled at: 2016-08-31 21:57:00
"""
Test GraphVertex class.
"""
import unittest
from py_alg_dat import graph
from py_alg_dat import graph_edge
from py_alg_dat import graph_vertex

class TestGraphVertex(unittest.TestCase):
    """
    Test GraphVertex class.
    """

    def setUp(self):
        self.graph1 = graph.DirectedGraph(5)
        self.v1_g1 = graph_vertex.GraphVertex(self.graph1, 'S')
        self.v2_g1 = graph_vertex.GraphVertex(self.graph1, 'T')
        self.v3_g1 = graph_vertex.GraphVertex(self.graph1, 'X')
        self.v4_g1 = graph_vertex.GraphVertex(self.graph1, 'Y')
        self.v5_g1 = graph_vertex.GraphVertex(self.graph1, 'Z')
        self.graph1.add_vertex(self.v1_g1)
        self.graph1.add_vertex(self.v2_g1)
        self.graph1.add_vertex(self.v3_g1)
        self.graph1.add_vertex(self.v4_g1)
        self.graph1.add_vertex(self.v5_g1)
        self.e12 = graph_edge.DirectedGraphEdge(self.graph1, self.v1_g1, self.v2_g1)
        self.e14 = graph_edge.DirectedGraphEdge(self.graph1, self.v1_g1, self.v4_g1)
        self.e23 = graph_edge.DirectedGraphEdge(self.graph1, self.v2_g1, self.v3_g1)
        self.e24 = graph_edge.DirectedGraphEdge(self.graph1, self.v2_g1, self.v4_g1)
        self.e35 = graph_edge.DirectedGraphEdge(self.graph1, self.v3_g1, self.v5_g1)
        self.e42 = graph_edge.DirectedGraphEdge(self.graph1, self.v4_g1, self.v2_g1)
        self.e43 = graph_edge.DirectedGraphEdge(self.graph1, self.v4_g1, self.v3_g1)
        self.e45 = graph_edge.DirectedGraphEdge(self.graph1, self.v4_g1, self.v5_g1)
        self.e53 = graph_edge.DirectedGraphEdge(self.graph1, self.v5_g1, self.v3_g1)
        self.e51 = graph_edge.DirectedGraphEdge(self.graph1, self.v5_g1, self.v1_g1)
        self.graph1.add_edge(self.v1_g1, self.v2_g1)
        self.graph1.add_edge(self.v1_g1, self.v4_g1)
        self.graph1.add_edge(self.v2_g1, self.v3_g1)
        self.graph1.add_edge(self.v2_g1, self.v4_g1)
        self.graph1.add_edge(self.v3_g1, self.v5_g1)
        self.graph1.add_edge(self.v4_g1, self.v2_g1)
        self.graph1.add_edge(self.v4_g1, self.v3_g1)
        self.graph1.add_edge(self.v4_g1, self.v5_g1)
        self.graph1.add_edge(self.v5_g1, self.v3_g1)
        self.graph1.add_edge(self.v5_g1, self.v1_g1)

    def test_graph_vertex_equal(self):
        """
        Test operator "equal".
        """
        a_graph = graph.DirectedGraph(5)
        vertex1 = graph_vertex.GraphVertex(a_graph, 'S')
        vertex2 = graph_vertex.GraphVertex(a_graph, 'T')
        vertex3 = graph_vertex.GraphVertex(a_graph, 'X')
        vertex4 = graph_vertex.GraphVertex(a_graph, 'Y')
        vertex5 = graph_vertex.GraphVertex(a_graph, 'Z')
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_vertex(vertex5)
        self.assertTrue(vertex3 == self.v3_g1)

    def test_graph_vertex_not_equal(self):
        """
        Test operator "inequal".
        """
        self.assertTrue(self.v1_g1 != self.v2_g1)

    def test_graph_vertex_get_vertex_number(self):
        """
        Test method "get_vertex_number".
        """
        self.assertEqual(0, self.v1_g1.get_vertex_number())

    def test_graph_vertex_get_vertex_name(self):
        """
        Test method "get_vertex_name".
        """
        self.assertEqual('S', self.v1_g1.get_vertex_name())

    def test_graph_vertex_get_successors_v1(self):
        """
        Test method "get_successors".
        """
        ref = []
        res = []
        ref.append(self.v2_g1)
        ref.append(self.v4_g1)
        res = self.v1_g1.get_successors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_successors_v2(self):
        """
        Test method "get_successors".
        """
        ref = []
        res = []
        ref.append(self.v3_g1)
        ref.append(self.v4_g1)
        res = self.v2_g1.get_successors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_successors_v3(self):
        """
        Test method "get_successors".
        """
        ref = []
        res = []
        ref.append(self.v5_g1)
        res = self.v3_g1.get_successors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_successors_v4(self):
        """
        Test method "get_successors".
        """
        ref = []
        res = []
        ref.append(self.v2_g1)
        ref.append(self.v3_g1)
        ref.append(self.v5_g1)
        res = self.v4_g1.get_successors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_successors_v5(self):
        """
        Test method "get_successors".
        """
        ref = []
        res = []
        ref.append(self.v3_g1)
        ref.append(self.v1_g1)
        res = self.v5_g1.get_successors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_predecessors_v1(self):
        """
        Test method "get_predecessors".
        """
        ref = []
        res = []
        ref.append(self.v5_g1)
        res = self.v1_g1.get_predecessors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_predecessors_v2(self):
        """
        Test method "get_predecessors".
        """
        ref = []
        res = []
        ref.append(self.v1_g1)
        ref.append(self.v4_g1)
        res = self.v2_g1.get_predecessors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_predecessors_v3(self):
        """
        Test method "get_predecessors".
        """
        ref = []
        res = []
        ref.append(self.v2_g1)
        ref.append(self.v4_g1)
        ref.append(self.v5_g1)
        res = self.v3_g1.get_predecessors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_predecessors_v4(self):
        """
        Test method "get_predecessors".
        """
        ref = []
        res = []
        ref.append(self.v1_g1)
        ref.append(self.v2_g1)
        res = self.v4_g1.get_predecessors()
        self.assertEqual(ref, res)

    def test_graph_vertex_get_predecessors_v5(self):
        """
        Test method "get_predecessors".
        """
        ref = []
        res = []
        ref.append(self.v3_g1)
        ref.append(self.v4_g1)
        res = self.v5_g1.get_predecessors()
        self.assertEqual(ref, res)