# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/test/KroneckerGeneratorTest.py
# Compiled at: 2011-11-11 06:18:24
import numpy
from apgl.graph.VertexList import VertexList
from apgl.graph.SparseGraph import SparseGraph
from apgl.generator.KroneckerGenerator import KroneckerGenerator
import unittest, logging

class KroneckerGeneratorTest(unittest.TestCase):

    def setUp(self):
        pass

    def testGenerate(self):
        k = 2
        numVertices = 3
        numFeatures = 0
        vList = VertexList(numVertices, numFeatures)
        initialGraph = SparseGraph(vList)
        initialGraph.addEdge(0, 1)
        initialGraph.addEdge(1, 2)
        for i in range(numVertices):
            initialGraph.addEdge(i, i)

        d = initialGraph.diameter()
        degreeSequence = initialGraph.outDegreeSequence()
        generator = KroneckerGenerator(initialGraph, k)
        graph = generator.generate()
        d2 = graph.diameter()
        degreeSequence2 = graph.outDegreeSequence()
        self.assertTrue((numpy.kron(degreeSequence, degreeSequence) == degreeSequence2).all())
        self.assertTrue(graph.getNumVertices() == numVertices ** k)
        self.assertTrue(graph.getNumDirEdges() == initialGraph.getNumDirEdges() ** k)
        self.assertEquals(d, d2)
        k = 3
        generator.setK(k)
        graph = generator.generate()
        d3 = graph.diameter()
        degreeSequence3 = graph.outDegreeSequence()
        self.assertTrue((numpy.kron(degreeSequence, degreeSequence2) == degreeSequence3).all())
        self.assertTrue(graph.getNumVertices() == numVertices ** k)
        self.assertTrue(graph.getNumDirEdges() == initialGraph.getNumDirEdges() ** k)
        self.assertEquals(d, d3)
        logging.debug(degreeSequence)
        logging.debug(degreeSequence2)
        logging.debug(degreeSequence3)

    def testDegreeDistribution(self):
        numVertices = 3
        numFeatures = 0
        vList = VertexList(numVertices, numFeatures)
        initialGraph = SparseGraph(vList)
        initialGraph.addEdge(0, 1)
        initialGraph.addEdge(1, 2)
        for i in range(numVertices):
            initialGraph.addEdge(i, i)

        logging.debug(initialGraph.outDegreeSequence())
        logging.debug(initialGraph.degreeDistribution())
        k = 2
        generator = KroneckerGenerator(initialGraph, k)
        graph = generator.generate()
        logging.debug(graph.outDegreeSequence())
        logging.debug(graph.degreeDistribution())
        k = 3
        generator = KroneckerGenerator(initialGraph, k)
        graph = generator.generate()
        logging.debug(graph.degreeDistribution())