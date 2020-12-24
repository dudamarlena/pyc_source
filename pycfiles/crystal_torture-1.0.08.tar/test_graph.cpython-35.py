# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/tests/test_graph.py
# Compiled at: 2018-05-29 04:42:59
# Size of source mod 2**32: 1963 bytes
import unittest
from unittest.mock import Mock
from crystal_torture import Cluster, Graph, Node
from crystal_torture.pymatgen_interface import graph_from_file, clusters_from_file
from crystal_torture import tort

class GraphTestCase(unittest.TestCase):
    __doc__ = ' Test for Graph Class'

    def setUp(self):
        self.labels = [
         'A', 'B', 'O', 'A', 'B', 'O']
        self.elements = ['Mg', 'Al', 'O', 'Mg', 'Al', 'O']
        self.node_ids = [0, 1, 2, 3, 4, 5]
        self.neighbours = [[1, 2, 3, 5], [0, 2, 4, 5], [1, 0, 4, 3], [0, 4, 5, 2], [1, 2, 3, 5], [4, 3, 0, 1]]
        self.nodes = [Mock(spec=Node, index=i, element=e, labels=l, neighbours_ind=n, neigbours=None) for i, e, l, n in zip(self.node_ids, self.elements, self.labels, self.neighbours)]
        for node in self.nodes:
            node.neighbours = [self.nodes[n] for n in node.neighbours_ind]
            node.neighbours = set(node.neighbours)

        self.cluster = Cluster({self.nodes.pop()})
        self.graph = Graph({self.cluster})

    def test_graph_is_initialised(self):
        self.cluster.grow_cluster()
        graph = Graph({self.cluster})
        c_nodes = set([node.index for node in self.cluster.nodes])
        g_nodes = set([node.index for node in graph.clusters.pop().nodes])
        self.assertEqual(g_nodes, c_nodes)

    def test_graph_from_file(self):
        graph = graph_from_file(filename='crystal_torture/tests/STRUCTURE_FILES/POSCAR_2_clusters.vasp', rcut=4.0, elements={'Li'})
        g_nodes = set([node.index for node in graph.clusters.pop().nodes])
        tort.tort_mod.tear_down()
        clusters = clusters_from_file(filename='crystal_torture/tests/STRUCTURE_FILES/POSCAR_2_clusters.vasp', rcut=4.0, elements={'Li'})
        c_nodes = set([node.index for node in clusters.pop().nodes])
        tort.tort_mod.tear_down()
        self.assertEqual(g_nodes, c_nodes)


if __name__ == '__main__':
    unittest.main()