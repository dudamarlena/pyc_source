# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/test/BarabasiAlbertGeneratorTest.py
# Compiled at: 2011-05-06 16:11:42
import unittest, logging
from apgl.generator.BarabasiAlbertGenerator import BarabasiAlbertGenerator
from apgl.graph.VertexList import VertexList
from apgl.graph.SparseGraph import SparseGraph

class BarabasiAlbertGeneratorTest(unittest.TestCase):

    def testGenerate(self):
        numFeatures = 1
        numVertices = 20
        vList = VertexList(numVertices, numFeatures)
        graph = SparseGraph(vList)
        ell = 2
        m = 0
        generator = BarabasiAlbertGenerator(ell, m)
        graph = generator.generate(graph)
        self.assertEquals(graph.getNumEdges(), 0)
        ell = 5
        graph.removeAllEdges()
        generator.setEll(ell)
        graph = generator.generate(graph)
        self.assertEquals(graph.getNumEdges(), 0)
        ell = 2
        m = 1
        graph.removeAllEdges()
        generator.setEll(ell)
        generator.setM(m)
        graph = generator.generate(graph)
        self.assertEquals(graph.getNumEdges(), (numVertices - ell) * m)
        m = 2
        graph.removeAllEdges()
        generator.setM(m)
        graph = generator.generate(graph)
        self.assertEquals(graph.getNumEdges(), (numVertices - ell) * m)

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
        ell = 2
        m = 2
        generator = BarabasiAlbertGenerator(ell, m)
        graph = generator.generate(graph)
        logging.debug(graph.degreeDistribution())
        nxGraph = graph.toNetworkXGraph()
        nodePositions = networkx.spring_layout(nxGraph)
        nodesAndEdges = networkx.draw_networkx(nxGraph, pos=nodePositions)


if __name__ == '__main__':
    unittest.main()