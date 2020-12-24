# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/graph/test/DenseGraphTest.py
# Compiled at: 2012-11-17 06:55:50
__doc__ = '\nCreated on 1 Jul 2009\n\n@author: charanpal\n'
from apgl.graph.DenseGraph import DenseGraph
from apgl.graph.VertexList import VertexList
from apgl.util import *
from apgl.graph.test.MatrixGraphTest import MatrixGraphTest
import unittest, numpy, logging, scipy.sparse

class DenseGraphTest(unittest.TestCase, MatrixGraphTest):

    def setUp(self):
        self.GraphType = DenseGraph
        self.initialise()

    def testInit(self):
        numVertices = 0
        numFeatures = 1
        vList = VertexList(numVertices, numFeatures)
        graph = DenseGraph(vList)
        self.assertEquals(graph.weightMatrixDType(), numpy.float64)
        graph = DenseGraph(vList, dtype=numpy.int16)
        self.assertEquals(graph.weightMatrixDType(), numpy.int16)
        numVertices = 0
        numFeatures = 1
        vList = VertexList(numVertices, numFeatures)
        graph = DenseGraph(vList, dtype=numpy.int16)
        numVertices = 10
        numFeatures = 1
        vList = VertexList(numVertices, numFeatures)
        graph = DenseGraph(vList, dtype=numpy.int16)
        self.assertEquals(type(graph.W), numpy.ndarray)
        self.assertRaises(ValueError, DenseGraph, [])
        self.assertRaises(ValueError, DenseGraph, vList, 1)
        self.assertRaises(ValueError, DenseGraph, vList, True, 1)
        W = scipy.sparse.csr_matrix((numVertices, numVertices))
        self.assertRaises(ValueError, DenseGraph, vList, True, W)
        W = numpy.zeros((numVertices + 1, numVertices))
        self.assertRaises(ValueError, DenseGraph, vList, True, W)
        W = numpy.zeros((numVertices, numVertices))
        W[(0, 1)] = 1
        self.assertRaises(ValueError, DenseGraph, vList, True, W)
        W = numpy.zeros((numVertices, numVertices))
        graph = DenseGraph(vList, W=W)
        self.assertEquals(type(graph.W), numpy.ndarray)
        numVertices = 10
        W = numpy.zeros((numVertices, numVertices))
        W[(1, 0)] = 1.1
        W[(0, 1)] = 1.1
        graph = DenseGraph(numVertices, W=W)
        self.assertEquals(graph[(1, 0)], 1.1)
        graph = DenseGraph(numVertices)
        self.assertEquals(graph.size, numVertices)
        graph = DenseGraph(numVertices, dtype=numpy.int)
        self.assertEquals(graph.W.dtype, numpy.int)
        graph[(0, 0)] = 1.2
        self.assertEquals(graph[(0, 0)], 1)


if __name__ == '__main__':
    unittest.main()