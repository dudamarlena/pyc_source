# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_directed_graph.py
# Compiled at: 2016-08-31 21:57:00
__doc__ = '\nTest directed graph.\n'
import unittest, copy
from py_alg_dat import dfs_edge_classification
from py_alg_dat import graph
from py_alg_dat import graph_edge
from py_alg_dat import graph_vertex
from py_alg_dat import vertex_visitor

class TestDirectedGraph(unittest.TestCase):
    """
    Test directed graph.
    """

    def setUp(self):
        self.graph1 = graph.DirectedGraph(5)
        self.v1_g1 = graph_vertex.UnWeightedGraphVertex(self.graph1, 'S')
        self.v2_g1 = graph_vertex.UnWeightedGraphVertex(self.graph1, 'T')
        self.v3_g1 = graph_vertex.UnWeightedGraphVertex(self.graph1, 'X')
        self.v4_g1 = graph_vertex.UnWeightedGraphVertex(self.graph1, 'Y')
        self.v5_g1 = graph_vertex.UnWeightedGraphVertex(self.graph1, 'Z')
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
        self.graph2 = graph.DirectedGraph(9)
        self.v0_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'a')
        self.v1_g1_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'b')
        self.v2_g1_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'c')
        self.v3_g1_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'd')
        self.v4_g1_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'e')
        self.v5_g1_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'f')
        self.v6_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'g')
        self.v7_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'h')
        self.v8_g2 = graph_vertex.UnWeightedGraphVertex(self.graph2, 'i')
        self.graph2.add_vertex(self.v0_g2)
        self.graph2.add_vertex(self.v1_g1_g2)
        self.graph2.add_vertex(self.v2_g1_g2)
        self.graph2.add_vertex(self.v3_g1_g2)
        self.graph2.add_vertex(self.v4_g1_g2)
        self.graph2.add_vertex(self.v5_g1_g2)
        self.graph2.add_vertex(self.v6_g2)
        self.graph2.add_vertex(self.v7_g2)
        self.graph2.add_vertex(self.v8_g2)
        self.e01_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v0_g2, self.v1_g1_g2)
        self.e02_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v0_g2, self.v2_g1_g2)
        self.e04_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v0_g2, self.v4_g1_g2)
        self.e13_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v1_g1_g2, self.v3_g1_g2)
        self.e14_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v1_g1_g2, self.v4_g1_g2)
        self.e27_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v2_g1_g2, self.v7_g2)
        self.e25_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v2_g1_g2, self.v5_g1_g2)
        self.e36_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v3_g1_g2, self.v6_g2)
        self.e46_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v4_g1_g2, self.v6_g2)
        self.e48_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v4_g1_g2, self.v8_g2)
        self.e47_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v4_g1_g2, self.v7_g2)
        self.e57_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v5_g1_g2, self.v7_g2)
        self.e68_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v6_g2, self.v8_g2)
        self.e78_g2 = graph_edge.DirectedGraphEdge(self.graph2, self.v7_g2, self.v8_g2)
        self.graph2.add_edge(self.v0_g2, self.v1_g1_g2)
        self.graph2.add_edge(self.v0_g2, self.v2_g1_g2)
        self.graph2.add_edge(self.v0_g2, self.v4_g1_g2)
        self.graph2.add_edge(self.v1_g1_g2, self.v3_g1_g2)
        self.graph2.add_edge(self.v1_g1_g2, self.v4_g1_g2)
        self.graph2.add_edge(self.v2_g1_g2, self.v7_g2)
        self.graph2.add_edge(self.v2_g1_g2, self.v5_g1_g2)
        self.graph2.add_edge(self.v3_g1_g2, self.v6_g2)
        self.graph2.add_edge(self.v4_g1_g2, self.v6_g2)
        self.graph2.add_edge(self.v4_g1_g2, self.v8_g2)
        self.graph2.add_edge(self.v4_g1_g2, self.v7_g2)
        self.graph2.add_edge(self.v5_g1_g2, self.v7_g2)
        self.graph2.add_edge(self.v6_g2, self.v8_g2)
        self.graph2.add_edge(self.v7_g2, self.v8_g2)

    def test_directed_graph_copy(self):
        """
        Test operator "copy".
        """
        graph1 = graph.DirectedGraph(5)
        vertex1 = graph_vertex.UnWeightedGraphVertex(graph1, 'A')
        vertex2 = graph_vertex.UnWeightedGraphVertex(graph1, 'B')
        vertex3 = graph_vertex.UnWeightedGraphVertex(graph1, 'C')
        vertex4 = graph_vertex.UnWeightedGraphVertex(graph1, 'D')
        vertex5 = graph_vertex.UnWeightedGraphVertex(graph1, 'E')
        graph1.add_vertex(vertex1)
        graph1.add_vertex(vertex2)
        graph1.add_vertex(vertex3)
        graph1.add_vertex(vertex4)
        graph1.add_vertex(vertex5)
        graph1.add_edge(vertex1, vertex2)
        graph1.add_edge(vertex1, vertex3)
        graph1.add_edge(vertex1, vertex4)
        graph1.add_edge(vertex1, vertex5)
        graph1.add_edge(vertex2, vertex3)
        graph1.add_edge(vertex2, vertex4)
        graph1.add_edge(vertex2, vertex5)
        graph1.add_edge(vertex3, vertex4)
        graph1.add_edge(vertex3, vertex5)
        graph1.add_edge(vertex4, vertex5)
        ref = copy.copy(graph1)
        self.assertEqual(graph1, ref)

    def test_directed_graph_len(self):
        """
        Test operator "len".
        """
        self.assertEqual(5, len(self.graph1))

    def test_directed_graph_get_item(self):
        """
        Test operator "get_item".
        """
        self.assertEqual(self.graph1.get_vertex_at_index(3), self.graph1[3])

    def test_directed_graph_get_number_of_vertices(self):
        """
        Test method "get_number_of_vertices".
        """
        self.assertEqual(5, self.graph1.get_number_of_vertices())

    def test_directed_graph_get_number_of_edges(self):
        """
        Test method "get_number_of_edges".
        """
        self.assertEqual(10, self.graph1.get_number_of_edges())

    def test_directed_graph_get_vertices(self):
        """
        Test method "get_vertices".
        """
        tmp1 = []
        tmp1.append(self.v1_g1)
        tmp1.append(self.v2_g1)
        tmp1.append(self.v3_g1)
        tmp1.append(self.v4_g1)
        tmp1.append(self.v5_g1)
        tmp2 = []
        tmp2 = self.graph1.get_vertices()
        s_list1 = sorted(tmp1, key=lambda vertex: (vertex.vertex_name, vertex.vertex_number))
        s_list2 = sorted(tmp2, key=lambda vertex: (vertex.vertex_name, vertex.vertex_number))
        self.assertEqual(s_list1, s_list2)

    def test_directed_graph_get_edges(self):
        """
        Test method "get_edges".
        """
        tmp1 = []
        tmp1.append(self.e12)
        tmp1.append(self.e14)
        tmp1.append(self.e23)
        tmp1.append(self.e24)
        tmp1.append(self.e35)
        tmp1.append(self.e42)
        tmp1.append(self.e43)
        tmp1.append(self.e45)
        tmp1.append(self.e53)
        tmp1.append(self.e51)
        tmp2 = []
        tmp2 = self.graph1.get_edges()
        s_list1 = sorted(tmp1, key=lambda edge: (edge.head_vertex, edge.tail_vertex))
        s_list2 = sorted(tmp2, key=lambda edge: (edge.head_vertex, edge.tail_vertex))
        self.assertEqual(s_list1, s_list2)

    def test_directed_graph_has_vertex(self):
        """
        Test method "has_vertex".
        """
        a_graph = graph.DirectedGraph(1)
        a_vertex = graph_vertex.UnWeightedGraphVertex(self.graph1, 'S')
        a_graph.add_vertex(a_vertex)
        self.assertTrue(a_graph.has_vertex(a_vertex))

    def test_directed_graph_has_vertex_not(self):
        """
        Test method "has_vertex" - inverted.
        """
        a_graph = graph.DirectedGraph(1)
        a_vertex = graph_vertex.UnWeightedGraphVertex(self.graph1, 'X')
        self.assertFalse(a_graph.has_vertex(a_vertex))

    def test_directed_graph_has_edge(self):
        """
        Test method "has_edge".
        """
        a_graph = graph.DirectedGraph(2)
        a_vertex = graph_vertex.UnWeightedGraphVertex(a_graph, 'S')
        b_vertex = graph_vertex.UnWeightedGraphVertex(a_graph, 'T')
        a_graph.add_vertex(a_vertex)
        a_graph.add_vertex(b_vertex)
        a_edge = graph_edge.DirectedGraphEdge(a_graph, a_vertex, b_vertex)
        a_graph.add_edge(a_vertex, b_vertex)
        self.assertTrue(a_graph.has_edge(a_edge))

    def test_directed_graph_has_edge_not(self):
        """
        Test method "has_edge" - inverted.
        """
        a_vertex = graph_vertex.UnWeightedGraphVertex(self.graph1, 'X')
        b_vertex = graph_vertex.UnWeightedGraphVertex(self.graph1, 'Y')
        a_edge = graph_edge.DirectedGraphEdge(self.graph1, a_vertex, b_vertex)
        self.assertFalse(self.graph1.has_edge(a_edge))

    def test_directed_graph_get_edge(self):
        """
        Test method "get_edge".
        """
        self.assertEqual(self.e12, self.graph1.get_edge(self.v1_g1, self.v2_g1))

    def test_directed_graph_is_edge(self):
        """
        Test method "is_edge".
        """
        try:
            self.assertTrue(self.graph1.is_edge(self.v1_g1, self.v2_g1))
        except KeyError:
            print 'Exception caught: %s' % str(KeyError)

    def test_directed_graph_remove_vertex_v0(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.DirectedGraph(5)
        vertex0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(vertex0)
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex0, vertex1)
        a_graph.add_edge(vertex0, vertex2)
        a_graph.add_edge(vertex0, vertex3)
        a_graph.add_edge(vertex0, vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex1, vertex3)
        a_graph.add_edge(vertex1, vertex4)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex2, vertex4)
        a_graph.add_edge(vertex3, vertex4)
        g_ref = graph.DirectedGraph(4)
        v1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        v4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v1_ref)
        g_ref.add_vertex(v2_ref)
        g_ref.add_vertex(v3_ref)
        g_ref.add_vertex(v4_ref)
        g_ref.add_edge(v1_ref, v2_ref)
        g_ref.add_edge(v1_ref, v3_ref)
        g_ref.add_edge(v1_ref, v4_ref)
        g_ref.add_edge(v2_ref, v3_ref)
        g_ref.add_edge(v2_ref, v4_ref)
        g_ref.add_edge(v3_ref, v4_ref)
        a_graph.remove_vertex(vertex0)
        self.assertEqual(g_ref, a_graph)

    def test_directed_graph_remove_vertex_v1(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.DirectedGraph(5)
        vertex0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(vertex0)
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex0, vertex1)
        a_graph.add_edge(vertex0, vertex2)
        a_graph.add_edge(vertex0, vertex3)
        a_graph.add_edge(vertex0, vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex1, vertex3)
        a_graph.add_edge(vertex1, vertex4)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex2, vertex4)
        a_graph.add_edge(vertex3, vertex4)
        g_ref = graph.DirectedGraph(4)
        v0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        v4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v0_ref)
        g_ref.add_vertex(v2_ref)
        g_ref.add_vertex(v3_ref)
        g_ref.add_vertex(v4_ref)
        g_ref.add_edge(v0_ref, v2_ref)
        g_ref.add_edge(v0_ref, v3_ref)
        g_ref.add_edge(v0_ref, v4_ref)
        g_ref.add_edge(v2_ref, v3_ref)
        g_ref.add_edge(v2_ref, v4_ref)
        g_ref.add_edge(v3_ref, v4_ref)
        a_graph.remove_vertex(vertex1)
        self.assertEqual(g_ref, a_graph)

    def test_directed_graph_remove_vertex_v2(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.DirectedGraph(5)
        vertex0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(vertex0)
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex0, vertex1)
        a_graph.add_edge(vertex0, vertex2)
        a_graph.add_edge(vertex0, vertex3)
        a_graph.add_edge(vertex0, vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex1, vertex3)
        a_graph.add_edge(vertex1, vertex4)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex2, vertex4)
        a_graph.add_edge(vertex3, vertex4)
        g_ref = graph.DirectedGraph(4)
        v0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        v4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v0_ref)
        g_ref.add_vertex(v1_ref)
        g_ref.add_vertex(v3_ref)
        g_ref.add_vertex(v4_ref)
        g_ref.add_edge(v0_ref, v1_ref)
        g_ref.add_edge(v0_ref, v3_ref)
        g_ref.add_edge(v0_ref, v4_ref)
        g_ref.add_edge(v1_ref, v3_ref)
        g_ref.add_edge(v1_ref, v4_ref)
        g_ref.add_edge(v3_ref, v4_ref)
        a_graph.remove_vertex(vertex2)
        self.assertEqual(g_ref, a_graph)

    def test_directed_graph_remove_vertex_v3(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.DirectedGraph(5)
        vertex0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(vertex0)
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex0, vertex1)
        a_graph.add_edge(vertex0, vertex2)
        a_graph.add_edge(vertex0, vertex3)
        a_graph.add_edge(vertex0, vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex1, vertex3)
        a_graph.add_edge(vertex1, vertex4)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex2, vertex4)
        a_graph.add_edge(vertex3, vertex4)
        g_ref = graph.DirectedGraph(4)
        v0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v0_ref)
        g_ref.add_vertex(v1_ref)
        g_ref.add_vertex(v2_ref)
        g_ref.add_vertex(v4_ref)
        g_ref.add_edge(v0_ref, v1_ref)
        g_ref.add_edge(v0_ref, v2_ref)
        g_ref.add_edge(v0_ref, v4_ref)
        g_ref.add_edge(v1_ref, v2_ref)
        g_ref.add_edge(v1_ref, v4_ref)
        g_ref.add_edge(v2_ref, v4_ref)
        a_graph.remove_vertex(vertex3)
        self.assertEqual(g_ref, a_graph)

    def test_directed_graph_remove_vertex_v4(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.DirectedGraph(5)
        vertex0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(vertex0)
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex0, vertex1)
        a_graph.add_edge(vertex0, vertex2)
        a_graph.add_edge(vertex0, vertex3)
        a_graph.add_edge(vertex0, vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex1, vertex3)
        a_graph.add_edge(vertex1, vertex4)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex2, vertex4)
        a_graph.add_edge(vertex3, vertex4)
        g_ref = graph.DirectedGraph(4)
        v0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        g_ref.add_vertex(v0_ref)
        g_ref.add_vertex(v1_ref)
        g_ref.add_vertex(v2_ref)
        g_ref.add_vertex(v3_ref)
        g_ref.add_edge(v0_ref, v1_ref)
        g_ref.add_edge(v0_ref, v2_ref)
        g_ref.add_edge(v0_ref, v3_ref)
        g_ref.add_edge(v1_ref, v2_ref)
        g_ref.add_edge(v1_ref, v3_ref)
        g_ref.add_edge(v2_ref, v3_ref)
        a_graph.remove_vertex(vertex4)
        self.assertEqual(g_ref, a_graph)

    def test_directed_graph_is_directed(self):
        """
        Test method "is_directed".
        """
        self.assertTrue(self.graph1.is_directed())

    def test_directed_graph_topological_order_traversal(self):
        """
        Test method "topological_order_traversal".
        """
        reference = []
        reference.insert(0, self.v0_g2)
        reference.insert(1, self.v1_g1_g2)
        reference.insert(2, self.v2_g1_g2)
        reference.insert(3, self.v3_g1_g2)
        reference.insert(4, self.v4_g1_g2)
        reference.insert(5, self.v5_g1_g2)
        reference.insert(6, self.v6_g2)
        reference.insert(7, self.v7_g2)
        reference.insert(8, self.v8_g2)
        visitor = vertex_visitor.VertexVisitor()
        self.graph2.topological_order_traversal(visitor)
        visited = visitor.get_visited()
        self.assertEqual(reference, visited)

    def test_directed_graph_is_strongly_connected(self):
        """
        Test method "is_strongly_connected".
        """
        self.assertTrue(self.graph1.is_strongly_connected())

    def test_directed_graph_is_strongly_connected_not(self):
        """
        Test method "is_strongly_connected" - inverted.
        """
        self.assertFalse(self.graph2.is_strongly_connected())

    def test_directed_graph_is_cyclic(self):
        """
        Test method "is_cyclic".
        """
        a_graph = graph.DirectedGraph(4)
        vertex_a = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex_b = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex_c = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex_d = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(vertex_a)
        a_graph.add_vertex(vertex_b)
        a_graph.add_vertex(vertex_c)
        a_graph.add_vertex(vertex_d)
        a_graph.add_edge(vertex_a, vertex_b)
        a_graph.add_edge(vertex_b, vertex_c)
        a_graph.add_edge(vertex_c, vertex_d)
        a_graph.add_edge(vertex_d, vertex_a)
        self.assertTrue(a_graph.is_cyclic())

    def test_directed_graph_is_cyclic_not(self):
        """
        Test method "is_cyclic" - inverted.
        """
        a_graph = graph.DirectedGraph(4)
        vertex_a = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex_b = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex_c = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex_d = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(vertex_a)
        a_graph.add_vertex(vertex_b)
        a_graph.add_vertex(vertex_c)
        a_graph.add_vertex(vertex_d)
        a_graph.add_edge(vertex_b, vertex_a)
        a_graph.add_edge(vertex_d, vertex_a)
        a_graph.add_edge(vertex_c, vertex_b)
        a_graph.add_edge(vertex_c, vertex_d)
        self.assertFalse(a_graph.is_cyclic())

    def test_directed_graph_get_vertex_at_index(self):
        """
        Test method "get_vertex_at_index".
        """
        self.assertEqual(self.v4_g1, self.graph1.get_vertex_at_index(3))

    def test_directed_graph_get_emanating_edges_v1(self):
        """
        Test method "get_emanating_edges".
        """
        ref = []
        res = []
        ref.append(self.e12)
        ref.append(self.e14)
        res = self.graph1.get_emanating_edges(self.v1_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_emanating_edges_v2(self):
        """
        Test method "get_emanating_edges".
        """
        ref = []
        res = []
        ref.append(self.e23)
        ref.append(self.e24)
        res = self.graph1.get_emanating_edges(self.v2_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_emanating_edges_v3(self):
        """
        Test method "get_emanating_edges".
        """
        ref = []
        res = []
        ref.append(self.e35)
        res = self.graph1.get_emanating_edges(self.v3_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_emanating_edges_v4(self):
        """
        Test method "get_emanating_edges".
        """
        ref = []
        res = []
        ref.append(self.e42)
        ref.append(self.e43)
        ref.append(self.e45)
        res = self.graph1.get_emanating_edges(self.v4_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_emanating_edges_v5(self):
        """
        Test method "get_emanating_edges".
        """
        ref = []
        res = []
        ref.append(self.e53)
        ref.append(self.e51)
        res = self.graph1.get_emanating_edges(self.v5_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_incident_edges_v1(self):
        """
        Test method "get_incident_edges".
        """
        ref = []
        res = []
        ref.append(self.e51)
        res = self.graph1.get_incident_edges(self.v1_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_incident_edges_v2(self):
        """
        Test method "get_incident_edges".
        """
        ref = []
        res = []
        ref.append(self.e12)
        ref.append(self.e42)
        res = self.graph1.get_incident_edges(self.v2_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_incident_edges_v3(self):
        """
        Test method "get_incident_edges".
        """
        ref = []
        res = []
        ref.append(self.e23)
        ref.append(self.e43)
        ref.append(self.e53)
        res = self.graph1.get_incident_edges(self.v3_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_incident_edges_v4(self):
        """
        Test method "get_incident_edges".
        """
        ref = []
        res = []
        ref.append(self.e14)
        ref.append(self.e24)
        res = self.graph1.get_incident_edges(self.v4_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_get_incident_edges_v5(self):
        """
        Test method "get_incident_edges".
        """
        ref = []
        res = []
        ref.append(self.e35)
        ref.append(self.e45)
        res = self.graph1.get_incident_edges(self.v5_g1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_directed_graph_classify_edges_cyclic(self):
        """
        Test edge classification - directed cyclic graph.
        """
        a_graph = graph.DirectedGraph(4)
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex3, vertex1)
        res = a_graph.classify_edges().get_edges()
        ref = dfs_edge_classification.DFSEdgeClassification(a_graph).get_edges()
        e12 = graph_edge.DirectedGraphEdge(a_graph, vertex1, vertex2)
        e23 = graph_edge.DirectedGraphEdge(a_graph, vertex2, vertex3)
        e31 = graph_edge.DirectedGraphEdge(a_graph, vertex3, vertex1)
        ref[e12] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e23] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e31] = graph_edge.EdgeClassification.BACK_EDGE
        self.assertEqual(res, ref)

    def test_directed_graph_classify_edges_acyclic(self):
        """
        Test edge classification - directed acyclic graph.
        """
        a_graph = graph.DirectedGraph(4)
        vertex1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        vertex2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        vertex3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        vertex4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(vertex1)
        a_graph.add_vertex(vertex2)
        a_graph.add_vertex(vertex3)
        a_graph.add_vertex(vertex4)
        a_graph.add_edge(vertex1, vertex2)
        a_graph.add_edge(vertex2, vertex3)
        a_graph.add_edge(vertex2, vertex4)
        res = a_graph.classify_edges().get_edges()
        ref = dfs_edge_classification.DFSEdgeClassification(a_graph).get_edges()
        e12 = graph_edge.DirectedGraphEdge(a_graph, vertex1, vertex2)
        e23 = graph_edge.DirectedGraphEdge(a_graph, vertex2, vertex3)
        e24 = graph_edge.DirectedGraphEdge(a_graph, vertex2, vertex4)
        ref[e12] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e23] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e24] = graph_edge.EdgeClassification.TREE_EDGE
        self.assertEqual(res, ref)