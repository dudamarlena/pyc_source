# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/graph/test/GeneralVertexListTest.py
# Compiled at: 2013-11-05 14:41:00
from apgl.graph.GeneralVertexList import GeneralVertexList
from apgl.graph.test.AbstractVertexListTest import AbstractVertexListTest
from apgl.util.PathDefaults import PathDefaults
import unittest, logging

class GeneralVertexListTest(unittest.TestCase, AbstractVertexListTest):

    def setUp(self):
        self.VListType = GeneralVertexList
        self.numVertices = 10
        self.vList = GeneralVertexList(self.numVertices)
        self.emptyVertex = None
        self.initialise()
        return

    def testConstructor(self):
        self.assertEquals(self.vList.getNumVertices(), self.numVertices)

    def testSaveLoad(self):
        try:
            vList = GeneralVertexList(self.numVertices)
            vList.setVertex(0, 'abc')
            vList.setVertex(1, 12)
            vList.setVertex(2, 'num')
            tempDir = PathDefaults.getTempDir()
            fileName = tempDir + 'vList'
            vList.save(fileName)
            vList2 = GeneralVertexList.load(fileName)
            for i in range(self.numVertices):
                self.assertEquals(vList.getVertex(i), vList2.getVertex(i))

        except IOError as e:
            logging.warn(e)

    def testAddVertices(self):
        vList = GeneralVertexList(10)
        vList.setVertex(1, 2)
        self.assertEquals(vList.getNumVertices(), 10)
        self.assertEquals(vList[1], 2)
        vList.addVertices(5)
        self.assertEquals(vList.getNumVertices(), 15)
        vList.setVertex(11, 2)
        self.assertEquals(vList[1], 2)
        self.assertEquals(vList[1], 2)


if __name__ == '__main__':
    unittest.main()