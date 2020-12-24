# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/tests/uniform_crossover_test.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 848 bytes
""" Test case for built-in Uniform Crossover operator.
"""
import unittest
from lsga.components import BinaryIndividual
from lsga.operators.crossover.uniform_crossover import UniformCrossover

class UniformCrossoverTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff

    def test_cross(self):
        """ Make sure individuals can be crossed correctly.
        """
        father = BinaryIndividual(ranges=[(0, 1)]).init(solution=[0.398])
        mother = BinaryIndividual(ranges=[(0, 1)]).init(solution=[0.298])
        crossover = UniformCrossover(pc=1.0, pe=0.5)
        child1, child2 = crossover.cross(father, mother)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(UniformCrossoverTest)
    unittest.TextTestRunner(verbosity=2).run(suite)