# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/ParameterTest.py
# Compiled at: 2012-04-06 16:37:19
import unittest, numpy, logging
from apgl.util.Parameter import Parameter
import scipy.sparse

class ParameterTest(unittest.TestCase):

    def testCheckInt(self):
        min = 0
        max = 5
        i = 2
        Parameter.checkInt(i, min, max)
        Parameter.checkInt(min, min, max)
        Parameter.checkInt(max, min, max)
        Parameter.checkInt(i, i, i)
        self.assertRaises(ValueError, Parameter.checkInt, i, max, min)
        self.assertRaises(ValueError, Parameter.checkInt, i, float(min), max)
        self.assertRaises(ValueError, Parameter.checkInt, i, min, float(max))
        self.assertRaises(ValueError, Parameter.checkInt, -1, min, max)
        self.assertRaises(ValueError, Parameter.checkInt, 6, min, max)
        Parameter.checkInt(i, min, float('inf'))
        Parameter.checkInt(i, float('-inf'), max)
        min = numpy.int32(0)
        max = numpy.int32(5)
        i = numpy.int32(2)
        Parameter.checkInt(i, min, max)
        Parameter.checkInt(min, min, max)
        Parameter.checkInt(max, min, max)
        Parameter.checkInt(i, i, i)
        i = numpy.array([1], numpy.int)
        logging.debug(type(i))
        self.assertRaises(ValueError, Parameter.checkInt, i, min, max)

    def testCheckFloat(self):
        min = 0.0
        max = 5.0
        i = 2.0
        Parameter.checkFloat(i, min, max)
        Parameter.checkFloat(min, min, max)
        Parameter.checkFloat(max, min, max)
        Parameter.checkFloat(i, i, i)
        self.assertRaises(ValueError, Parameter.checkFloat, i, max, min)
        self.assertRaises(ValueError, Parameter.checkFloat, i, int(min), max)
        self.assertRaises(ValueError, Parameter.checkFloat, i, min, int(max))
        self.assertRaises(ValueError, Parameter.checkFloat, 2, min, max)
        self.assertRaises(ValueError, Parameter.checkFloat, -1, min, max)
        self.assertRaises(ValueError, Parameter.checkFloat, 6, min, max)
        Parameter.checkFloat(i, min, float('inf'))
        Parameter.checkFloat(i, float('-inf'), max)
        min = numpy.float64(0.0)
        max = numpy.float64(5.0)
        i = numpy.float64(2.0)
        Parameter.checkFloat(i, min, max)
        Parameter.checkFloat(min, min, max)
        Parameter.checkFloat(max, min, max)
        Parameter.checkFloat(i, i, i)

    def testCheckString(self):
        s = 'a'
        lst = ['a', 'b', 'c']
        Parameter.checkString('a', lst)
        Parameter.checkString('b', lst)
        Parameter.checkString('c', lst)
        self.assertRaises(ValueError, Parameter.checkString, 'd', lst)
        self.assertRaises(ValueError, Parameter.checkString, 5, lst)
        self.assertRaises(ValueError, Parameter.checkString, 'a', s)

    def testCheckList(self):
        lst = [
         1, 2, 3, 2, 2]
        Parameter.checkList(lst, Parameter.checkInt, [1, 3])
        lst = [
         1, 2, 3, 2, 4]
        self.assertRaises(ValueError, Parameter.checkList, lst, Parameter.checkInt, [1, 3])
        lst = [
         1, 2, 3, 2, 0]
        self.assertRaises(ValueError, Parameter.checkList, lst, Parameter.checkInt, [1, 3])
        lst = [
         1, 2, 3, 2, 1.2]
        self.assertRaises(ValueError, Parameter.checkList, lst, Parameter.checkInt, [1, 3])
        lst = 'a'
        self.assertRaises(ValueError, Parameter.checkList, lst, Parameter.checkInt, [1, 3])
        lst = [
         0.1, 0.6, 1.4]
        Parameter.checkList(lst, Parameter.checkFloat, [0.1, 3.0])
        lst = numpy.array([0.1, 0.6, 1.4])
        Parameter.checkList(lst, Parameter.checkFloat, [0.1, 3.0])
        lst = numpy.array([[0.1, 0.6, 1.4]])
        self.assertRaises(ValueError, Parameter.checkList, lst, Parameter.checkFloat, [0.1, 3.0])

    def checkBoolean(self):
        a = True
        b = False
        c = 0
        d = 1
        e = 's'
        Parameter.checkBoolean(a)
        Parameter.checkBoolean(b)
        self.assertRaises(ValueError, Parameter.checkBoolean, c)
        self.assertRaises(ValueError, Parameter.checkBoolean, d)
        self.assertRaises(ValueError, Parameter.checkBoolean, e)

    def checkClass(self):
        a = VertexList(10, 1)
        b = 2
        c = True
        d = SparseGraph(a)
        Parameter.checkClass(a, VertexList)
        Parameter.checkClass(b, int)
        Parameter.checkClass(c, bool)
        Parameter.checkClass(d, SparseGraph)
        self.assertRaises(ValueError, Parameter.checkClass, a, SparseGraph)
        self.assertRaises(ValueError, Parameter.checkClass, b, VertexList)

    def testCheckSymmetric(self):
        W = numpy.random.rand(5, 5)
        W = W.T + W
        Parameter.checkSymmetric(W)
        W[(0, 1)] += 0.1
        self.assertRaises(ValueError, Parameter.checkSymmetric, W)
        self.assertRaises(ValueError, Parameter.checkSymmetric, W, 0.1)
        Parameter.checkSymmetric(W, 0.2)
        W = scipy.sparse.rand(5, 5, 0.2, format='csr')
        Ws = W + W.T
        Parameter.checkSymmetric(Ws)
        Ws[(0, 1)] += 0.1
        self.assertRaises(ValueError, Parameter.checkSymmetric, Ws)
        self.assertRaises(ValueError, Parameter.checkSymmetric, W)


if __name__ == '__main__':
    unittest.main()