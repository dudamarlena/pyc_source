# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/tests/individual_test.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 3105 bytes
""" Test case for Individual.
"""
import unittest
from ..components import BinaryIndividual

class IndividualTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_binary_encoding(self):
        """ Make sure individual can decode and encode binary gene correctly.
        """
        indv = BinaryIndividual(ranges=[(0, 1)], eps=0.001)
        indv.init(solution=[0.398])
        ref_chromsome = [
         0, 1, 1, 0, 0, 1, 0, 1, 1]
        self.assertListEqual(indv.chromsome, ref_chromsome)
        self.assertListEqual(indv.decode(), [0.396484375])
        indv = BinaryIndividual(ranges=[(0, 1), (-1, 1)], eps=0.001)
        indv.init(solution=[0.398, 0.66])
        ref_chromsome = [
         0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
        self.assertListEqual(indv.chromsome, ref_chromsome)
        self.assertListEqual(indv.decode(), [0.396484375, 0.658203125])

    def test_descriptors(self):
        """ Make sure descriptors can check the parameters correctly.
        """
        self.assertRaises(TypeError, BinaryIndividual, ranges=0.1, eps=0.001)
        self.assertRaises(TypeError, BinaryIndividual, ranges=[(0, 1)], eps='asdf')
        self.assertRaises(ValueError, BinaryIndividual, ranges=[(0, 1)], eps=10.0)
        self.assertRaises(ValueError, BinaryIndividual, ranges=[(0, 1)], eps=[1, 2])

    def test_init(self):
        """ Make sure the individual can be initialized correctly.
        """
        indv = BinaryIndividual(ranges=[(0, 1)], eps=0.001)
        indv.init(chromsome=[0, 1, 1, 0, 0, 0, 1, 1, 1, 0])
        self.assertListEqual([0, 1, 1, 0, 0, 0, 1, 1, 1, 0], indv.chromsome)
        self.assertListEqual(indv.solution, [0.388671875])
        indv.init(solution=[0.398])
        self.assertListEqual(indv.solution, [0.398])
        self.assertListEqual(indv.chromsome, [0, 1, 1, 0, 0, 1, 0, 1, 1])

    def test_clone(self):
        """ Make sure individual can be cloned correctly.
        """
        indv = BinaryIndividual(ranges=[(0, 1)], eps=0.001).init(solution=[0.398])
        indv_clone = indv.clone()
        self.assertListEqual(indv.chromsome, indv_clone.chromsome)
        self.assertAlmostEqual((indv.solution[0]), (indv_clone.solution[0]), places=2)
        self.assertEqual(indv.ranges, indv_clone.ranges)
        self.assertEqual(indv.eps, indv_clone.eps)

    def test_multi_precisions(self):
        """ Make sure we can construct individual using different decrete precisions.
        """
        indv = BinaryIndividual(ranges=[(0, 1), (0, 10)], eps=[0.01, 1.0]).init(solution=[0.3, 0.5])
        self.assertNotEqual(indv.precisions[0], indv.precisions[1])


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(IndividualTest)
    unittest.TextTestRunner(verbosity=2).run(suite)