# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/tests/linear_ranking_selection_test.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1056 bytes
""" Test case for built-in Linear Ranking selection
"""
import unittest
from lsga.components import Population, BinaryIndividual
from lsga.operators import LinearRankingSelection

class LinearRankingSelectionTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff

        def fitness(indv):
            x, = indv.solution
            return x ** 3 - 60 * x ** 2 + 900 * x + 100

        self.fitness = fitness

    def test_selection(self):
        indv = BinaryIndividual(ranges=[(0, 30)])
        p = Population(indv)
        p.init()
        selection = LinearRankingSelection()
        father, mother = selection.select(p, fitness=(self.fitness))
        self.assertTrue(isinstance(father, BinaryIndividual))
        self.assertTrue(isinstance(mother, BinaryIndividual))
        self.assertNotEqual(father.chromsome, mother.chromsome)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(LinearRankingSelectionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)