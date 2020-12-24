# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/layout/layout_matrix_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1319 bytes
import unittest
from bibliopixel.layout.geometry import matrix

class MatrixTest(unittest.TestCase):

    def test_simple(self):
        m = matrix.Matrix(list(range(12)), 3)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(1, 0), 1)
        self.assertEqual(m.get(0, 1), 3)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(2, 3), 11)

    def test_transpose(self):
        m = matrix.Matrix((list(range(12))), 3, transpose=True)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(0, 1), 1)
        self.assertEqual(m.get(1, 0), 3)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(3, 2), 11)

    def test_reflect(self):
        m = matrix.Matrix((list(range(12))), 3, reflect_x=True)
        self.assertEqual(m.get(0, 0), 2)
        self.assertEqual(m.get(1, 0), 1)
        self.assertEqual(m.get(0, 1), 5)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(2, 3), 9)

    def test_serpentine(self):
        m = matrix.Matrix((list(range(12))), 3, serpentine_x=True)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(1, 0), 1)
        self.assertEqual(m.get(0, 1), 5)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(2, 2), 8)
        self.assertEqual(m.get(2, 3), 9)