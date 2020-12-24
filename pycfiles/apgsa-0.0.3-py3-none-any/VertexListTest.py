# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/graph/test/VertexListTest.py
# Compiled at: 2013-11-05 14:41:00
from apgl.util.PathDefaults import PathDefaults
from apgl.graph.test.AbstractVertexListTest import AbstractVertexListTest
from apgl.graph.VertexList import VertexList
import unittest, numpy, logging, numpy.testing as nptst

class VertexListTest(unittest.TestCase, AbstractVertexListTest):

    def setUp(self):
        self.numVertices = 10
        self.numFeatures = 3
        self.vList = VertexList(self.numVertices, self.numFeatures)
        self.emptyVertex = numpy.zeros(self.numFeatures)
        self.initialise()

    def testConstructor(self):
        self.assertEquals(self.vList.getNumFeatures(), self.numFeatures)
        self.assertEquals(self.vList.getNumVertices(), self.numVertices)

    def testSaveLoad(self):
        try:
            vList = VertexList(self.numVertices, self.numFeatures)
            vList.setVertex(0, numpy.array([1, 2, 3]))
            vList.setVertex(1, numpy.array([4, 5, 6]))
            vList.setVertex(2, numpy.array([7, 8, 9]))
            tempDir = PathDefaults.getTempDir()
            fileName = tempDir + 'vList'
            vList.save(fileName)
            vList2 = VertexList.load(fileName)
            self.assertTrue((vList.getVertices() == vList2.getVertices()).all())
        except IOError as e:
            logging.warn(e)

    def testGetItem2(self):
        V = numpy.random.rand(self.numVertices, self.numFeatures)
        self.vList.setVertices(V)
        for i in range(self.numVertices):
            nptst.assert_array_equal(self.vList[i, :], V[i, :])

    def testSetItem2(self):
        V = numpy.random.rand(self.numVertices, self.numFeatures)
        for i in range(self.numVertices):
            self.vList[i, :] = V[i, :]
            nptst.assert_array_equal(self.vList[i, :], V[i, :])

    def testAddVertices(self):
        numFeatures = 5
        vList = VertexList(10, numFeatures)
        vList.setVertex(1, numpy.ones(numFeatures) * 0.1)
        self.assertEquals(vList.getNumVertices(), 10)
        nptst.assert_array_equal(vList[1], numpy.ones(numFeatures) * 0.1)
        vList.addVertices(5)
        self.assertEquals(vList.getNumVertices(), 15)
        vList.setVertex(11, numpy.ones(numFeatures) * 2)
        nptst.assert_array_equal(vList[1], numpy.ones(numFeatures) * 0.1)
        nptst.assert_array_equal(vList[11], numpy.ones(numFeatures) * 2)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(VertexListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)