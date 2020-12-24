# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/PySparseUtilsTest.py
# Compiled at: 2011-03-03 05:35:30
import unittest, numpy, apgl

@apgl.skipIf(not apgl.checkImport('pysparse'), 'No module pysparse')
class PySparseUtilsTest(unittest.TestCase):

    def testSum(self):
        try:
            from pysparse import spmatrix
            from apgl.util.PySparseUtils import PySparseUtils
        except ImportError as error:
            return

        n = 10
        X = spmatrix.ll_mat(n, n)
        self.assertEquals(PySparseUtils.sum(X), 0.0)
        X[(1, 1)] = 5
        X[(2, 4)] = 6.1
        X[(3, 1)] = 2.5
        self.assertEquals(PySparseUtils.sum(X), 13.6)

    def testNonzero(self):
        try:
            from pysparse import spmatrix
            from apgl.util.PySparseUtils import PySparseUtils
        except ImportError as error:
            return

        n = 10
        X = spmatrix.ll_mat(n, n)
        self.assertTrue((PySparseUtils.nonzero(X)[0] == numpy.array([], numpy.int)).all())
        self.assertTrue((PySparseUtils.nonzero(X)[0] == numpy.array([], numpy.int)).all())
        X[(1, 1)] = 5
        X[(2, 4)] = 6.1
        X[(3, 1)] = 2.5
        self.assertTrue((PySparseUtils.nonzero(X)[0] == numpy.array([1, 2, 3], numpy.int)).all())
        self.assertTrue((PySparseUtils.nonzero(X)[1] == numpy.array([1, 4, 1], numpy.int)).all())


if __name__ == '__main__':
    unittest.main()