# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/SparseUtilsTest.py
# Compiled at: 2013-02-21 05:52:13
import unittest, numpy, apgl, scipy.sparse
from apgl.util.SparseUtils import SparseUtils

class SparseUtilsTest(unittest.TestCase):

    def setUp(self):
        numpy.random.seed(21)

    def testEquals(self):
        A = numpy.array([[4, 2, 1], [6, 3, 9], [3, 6, 0]])
        B = numpy.array([[4, 2, 1], [6, 3, 9], [3, 6, 0]])
        A = scipy.sparse.csr_matrix(A)
        B = scipy.sparse.csr_matrix(B)
        self.assertTrue(SparseUtils.equals(A, B))
        A[(0, 1)] = 5
        self.assertFalse(SparseUtils.equals(A, B))
        A[(0, 1)] = 2
        B[(0, 1)] = 5
        self.assertFalse(SparseUtils.equals(A, B))
        A[(2, 2)] = -1
        self.assertFalse(SparseUtils.equals(A, B))
        A = scipy.sparse.csr_matrix((5, 5))
        B = scipy.sparse.csr_matrix((5, 5))
        self.assertTrue(SparseUtils.equals(A, B))

    def testNorm(self):
        numRows = 10
        numCols = 10
        for k in range(10):
            A = scipy.sparse.rand(numRows, numCols, 0.1, 'csr')
            norm = SparseUtils.norm(A)
            norm2 = 0
            for i in range(numRows):
                for j in range(numCols):
                    norm2 += A[(i, j)] ** 2

            norm2 = numpy.sqrt(norm2)
            norm3 = numpy.linalg.norm(numpy.array(A.todense()))
            self.assertAlmostEquals(norm, norm2)
            self.assertAlmostEquals(norm, norm3)

    def testResize(self):
        numRows = 10
        numCols = 10
        A = scipy.sparse.rand(numRows, numCols, 0.1, 'csr')
        B = SparseUtils.resize(A, (5, 5))
        self.assertEquals(B.shape, (5, 5))
        for i in range(5):
            for j in range(5):
                self.assertEquals(B[(i, j)], A[(i, j)])

        B = SparseUtils.resize(A, (15, 15))
        self.assertEquals(B.shape, (15, 15))
        self.assertEquals(B.nnz, A.nnz)
        for i in range(10):
            for j in range(10):
                self.assertEquals(B[(i, j)], A[(i, j)])

    def testDiag(self):
        numRows = 10
        numCols = 10
        A = scipy.sparse.rand(numRows, numCols, 0.5, 'csr')
        d = SparseUtils.diag(A)
        for i in range(numRows):
            self.assertEquals(d[i], A[(i, i)])

    def testSelectMatrix(self):
        numRows = 10
        numCols = 10
        A = scipy.sparse.rand(numRows, numCols, 0.5, 'csr')
        rowInds = numpy.zeros(numCols)
        colInds = numpy.arange(10)
        newA = SparseUtils.selectMatrix(A, rowInds, colInds)
        for i in range(numCols):
            self.assertEquals(A[(0, i)], newA[(0, i)])

        for i in range(1, numRows):
            for j in range(numCols):
                self.assertEquals(newA[(i, j)], 0)


if __name__ == '__main__':
    unittest.main()