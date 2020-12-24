# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/LatexTest.py
# Compiled at: 2013-07-30 12:17:01
import unittest, numpy, logging
from apgl.util.Latex import Latex

class LatexTest(unittest.TestCase):

    def testArray1DToLatex(self):
        X = numpy.array([1.2323132, 5.324323, 8.3213232])
        self.assertEquals(Latex.array1DToRow(X, 3), '1.232 & 5.324 & 8.321')
        X = numpy.array([1, 2, 3], numpy.int)
        self.assertEquals(Latex.array1DToRow(X, 3), '1 & 2 & 3')

    def testListToLatex(self):
        lst = [
         'one', 'two', 'three']
        self.assertEquals(Latex.listToRow(lst), 'one & two & three\\\\')
        lst = []
        self.assertEquals(Latex.listToRow(lst), '')

    def testArray2DToRows(self):
        numpy.random.seed(21)
        X = numpy.random.rand(2, 2)
        Y = numpy.random.rand(2, 2)
        outputStr = '0.049 (0.206) & 0.289 (0.051)\\\\\n'
        outputStr += '0.721 (0.302) & 0.022 (0.664)\\\\'
        self.assertTrue(Latex.array2DToRows(X, Y) == outputStr)
        Z = X > 0.2
        A = X > 0.7
        outputStr = '0.049 (0.206) & \\textbf{0.289} (0.051)\\\\\n'
        outputStr += '\\emph{\\textbf{0.721}} (0.302) & 0.022 (0.664)\\\\'
        self.assertTrue(Latex.array2DToRows(X, Y, bold=Z, italic=A) == outputStr)
        outputStr = '0.049 & 0.289\\\\\n'
        outputStr += '0.721 & 0.022\\\\'
        self.assertTrue(Latex.array2DToRows(X, Y=None) == outputStr)
        outputStr = '0.049 & 0.289\\\\\n'
        outputStr += '0.721 & 0.022\\\\'
        return

    def testAddRowNames(self):
        numpy.random.seed(21)
        X = numpy.random.rand(2, 2)
        Y = numpy.random.rand(2, 2)
        latexTable = Latex.array2DToRows(X, Y)
        rowNames = ['a', 'b']
        latexTable = Latex.addRowNames(rowNames, latexTable)
        outputStr = 'a & 0.049 (0.206) & 0.289 (0.051)\\\\\n'
        outputStr += 'b & 0.721 (0.302) & 0.022 (0.664)\\\\\n'
        self.assertTrue(latexTable == outputStr)
        rowNames = [
         'a', 'b', 'c']
        self.assertRaises(ValueError, Latex.addRowNames, rowNames, latexTable)
        rowNames = [
         'a']
        self.assertRaises(ValueError, Latex.addRowNames, rowNames, latexTable)

    def testLatexTable(self):
        outputStr = '0.049 (0.206) & 0.289 (0.051)\\\\\n'
        outputStr += '0.721 (0.302) & 0.022 (0.664)\\\\'


if __name__ == '__main__':
    unittest.main()