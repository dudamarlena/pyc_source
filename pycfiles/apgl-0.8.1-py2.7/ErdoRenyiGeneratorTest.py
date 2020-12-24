# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/test/ErdoRenyiGeneratorTest.py
# Compiled at: 2012-11-06 11:18:12
"""
Created on 3 Jul 2009

@author: charanpal
"""
from apgl.graph.DenseGraph import DenseGraph
from apgl.graph.SparseGraph import SparseGraph
from apgl.graph.VertexList import VertexList
from apgl.graph.GeneralVertexList import GeneralVertexList
from apgl.generator.ErdosRenyiGenerator import ErdosRenyiGenerator
import unittest, logging, apgl, numpy

class ErdoRenyiGeneratorTest(unittest.TestCase):

    def setUp(self):
        numpy.set_printoptions(suppress=True, linewidth=200, precision=5)
        self.numVertices = 10
        self.numFeatures = 2
        self.vList = VertexList(self.numVertices, self.numFeatures)
        self.graph = SparseGraph(self.vList)
        self.p = 0.1
        self.erg = ErdosRenyiGenerator(self.p)

    def testGenerate(self):
        p = 0.0
        self.graph.removeAllEdges()
        self.erg.setP(p)
        graph = self.erg.generate(self.graph)
        self.assertEquals(graph.getNumEdges(), 0)
        undirected = False
        self.graph = SparseGraph(self.vList, undirected)
        self.graph.removeAllEdges()
        self.erg = ErdosRenyiGenerator(p)
        graph = self.erg.generate(self.graph)
        self.assertEquals(graph.getNumEdges(), 0)
        p = 1.0
        undirected = True
        self.graph = SparseGraph(self.vList, undirected)
        self.graph.removeAllEdges()
        self.erg = ErdosRenyiGenerator(p)
        graph = self.erg.generate(self.graph)
        self.assertEquals(graph.getNumEdges(), (self.numVertices * self.numVertices - self.numVertices) / 2)
        p = 1.0
        undirected = False
        self.graph = SparseGraph(self.vList, undirected)
        self.graph.removeAllEdges()
        self.erg = ErdosRenyiGenerator(p)
        graph = self.erg.generate(self.graph)
        self.assertEquals(graph.getNumEdges(), self.numVertices * self.numVertices - self.numVertices)
        self.assertEquals(graph.getEdge(1, 2), 1)
        self.assertEquals(graph.getEdge(1, 1), None)
        p = 0.5
        numVertices = 1000
        numFeatures = 0
        vList = VertexList(numVertices, numFeatures)
        undirected = False
        self.graph = SparseGraph(vList, undirected)
        self.erg = ErdosRenyiGenerator(p)
        graph = self.erg.generate(self.graph)
        self.assertAlmostEquals(graph.getNumEdges() / float(numVertices ** 2 - numVertices), p, places=2)
        p = 0.1
        self.graph = SparseGraph(vList, undirected)
        self.erg = ErdosRenyiGenerator(p)
        graph = self.erg.generate(self.graph)
        self.assertAlmostEquals(graph.getNumEdges() / float(numVertices ** 2 - numVertices), p, places=2)
        p = 0.5
        numVertices = 10
        vList = VertexList(numVertices, numFeatures)
        graph = SparseGraph(vList, undirected)
        graph.addEdge(0, 1, 5)
        graph.addEdge(0, 2)
        graph.addEdge(0, 5, 0.7)
        graph.addEdge(1, 8)
        graph.addEdge(2, 9)
        numEdges = graph.getNumEdges()
        graph = self.erg.generate(graph, False)
        self.assertTrue(graph.getNumEdges() > numEdges)
        return

    @apgl.skip('')
    def testGraphDisplay(self):
        try:
            import networkx, matplotlib
        except ImportError as error:
            logging.debug(error)
            return

        numFeatures = 1
        numVertices = 20
        vList = VertexList(numVertices, numFeatures)
        graph = SparseGraph(vList)
        p = 0.2
        generator = ErdosRenyiGenerator(p)
        graph = generator.generate(graph)
        logging.debug(graph.getNumEdges())
        nxGraph = graph.toNetworkXGraph()
        nodePositions = networkx.spring_layout(nxGraph)
        nodesAndEdges = networkx.draw_networkx(nxGraph, pos=nodePositions)
        ax = matplotlib.pyplot.axes()
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    def testGenerate2(self):
        numVertices = 20
        graph = SparseGraph(GeneralVertexList(numVertices))
        p = 0.2
        generator = ErdosRenyiGenerator(p)
        graph = generator.generate(graph)
        self.assertTrue(graph.getNumEdges() - p * numVertices * numVertices / 2 < 8)

    def testErdosRenyiGenerations(self):
        numVertices = 20
        graph = DenseGraph(GeneralVertexList(numVertices))
        p = 0.2
        generator = ErdosRenyiGenerator(p)
        graph = generator.generate(graph)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ErdoRenyiGeneratorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)