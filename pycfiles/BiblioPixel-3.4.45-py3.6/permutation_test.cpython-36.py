# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/permutation_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1744 bytes
import unittest
from bibliopixel.util.permutation import advance_permutation

class PermutationTest(unittest.TestCase):

    def test_permutation(self):
        a = [
         0, 1, 2, 3, 4]
        self.assertTrue(advance_permutation(a))
        self.assertEqual([0, 1, 2, 4, 3], a)
        a = [
         3, 0, 4, 2, 1]
        self.assertTrue(advance_permutation(a))
        self.assertEqual([3, 1, 0, 2, 4], a)
        a = [
         4, 3, 2, 1, 0]
        self.assertFalse(advance_permutation(a))
        self.assertEqual([0, 1, 2, 3, 4], a)

    def test_reverse(self):
        x = (
         [
          0, 1, 2, 3, 4], [3, 0, 4, 2, 1], [1, 2, 3, 4, 0], [4, 3, 2, 1, 0])
        for a in x:
            b = list(a)
            advance_permutation(b)
            advance_permutation(b, increasing=False)
            self.assertEqual(a, b)
            b = list(a)
            advance_permutation(b, increasing=False)
            advance_permutation(b)
            self.assertEqual(a, b)
            b = list(a)
            advance_permutation(b, increasing=False, forward=False)
            advance_permutation(b, forward=False)
            self.assertEqual(a, b)
            b = list(a)
            advance_permutation(b, forward=False)
            advance_permutation(b, increasing=False, forward=False)
            self.assertEqual(a, b)

    def test_right_to_left(self):
        a = [0, 1, 2, 3, 4]
        self.assertFalse(advance_permutation(a, forward=False))
        self.assertEqual([4, 3, 2, 1, 0], a)
        a = [
         3, 0, 4, 2, 1]
        self.assertTrue(advance_permutation(a, forward=False))
        self.assertEqual([0, 3, 4, 2, 1], a)
        a = [
         4, 3, 2, 1, 0]
        self.assertTrue(advance_permutation(a, forward=False))
        self.assertEqual([3, 4, 2, 1, 0], a)