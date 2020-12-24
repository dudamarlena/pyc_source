# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/test/SmallWorldGeneratorTest.py
# Compiled at: 2011-11-11 06:18:48
__doc__ = '\nCreated on 3 Jul 2009\n\n@author: charanpal\n'
from apgl.graph.VertexList import VertexList
from apgl.graph.SparseGraph import SparseGraph
from apgl.generator.SmallWorldGenerator import SmallWorldGenerator
from apgl.io.PajekWriter import PajekWriter
import unittest, logging

class SmallWorldGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.numVertices = 100
        self.numFeatures = 2
        p = 0.1
        k = 10
        self.vList = VertexList(self.numVertices, self.numFeatures)
        self.graph = SparseGraph(self.vList)
        self.swg = SmallWorldGenerator(p, k)

    def testgenerate(self):
        p = 0.0
        k = 1
        self.swg.setP(p)
        self.swg.setK(k)
        sGraph = self.swg.generate(self.graph)
        self.assertEquals(sGraph.getNumEdges(), sGraph.getNumVertices())
        for i in range(self.numVertices):
            for j in range(k):
                self.assertEquals(sGraph.getEdge(i, (i + j + 1) % self.numVertices), 1)

        k = 3
        sGraph.removeAllEdges()
        self.swg.setP(p)
        self.swg.setK(k)
        sGraph = self.swg.generate(self.graph)
        self.assertEquals(sGraph.getNumEdges(), sGraph.getNumVertices() * k)
        for i in range(self.numVertices):
            for j in range(k):
                self.assertEquals(sGraph.getEdge(i, (i + j + 1) % self.numVertices), 1)

        p = 0.5
        k = 1
        sGraph.removeAllEdges()
        self.swg.setP(p)
        self.swg.setK(k)
        sGraph = self.swg.generate(self.graph)
        self.assertEquals(sGraph.getNumEdges(), sGraph.getNumVertices())
        p = 0.1
        k = 2
        sGraph.removeAllEdges()
        self.swg.setP(p)
        self.swg.setK(k)
        sGraph = self.swg.generate(self.graph)
        self.assertEquals(sGraph.getNumEdges(), sGraph.getNumVertices() * k)

    def tearDown(self):
        pass

    def testInit(self):
        pass

    def testGetClusteringCoefficient(self):
        p = 0.0
        k = 10
        self.swg.setP(p)
        self.swg.setK(k)
        cc = 3 * (k - 1) * (1 - p) ** 3 / (2 * (2 * k - 1))
        self.assertEquals(self.swg.clusteringCoefficient(), cc)
        p = 0.5
        self.swg.setP(p)
        cc = 3 * (k - 1) * (1 - p) ** 3 / (2 * (2 * k - 1))
        self.assertEquals(self.swg.clusteringCoefficient(), cc)
        k = 1
        self.swg.setK(k)
        self.assertEquals(self.swg.clusteringCoefficient(), 0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SmallWorldGeneratorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)