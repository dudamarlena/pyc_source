# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/tests/engine_test.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 2246 bytes
""" Test case for engine run.
"""
import unittest
from math import sin, cos
from .. import GAEngine
from ..components import BinaryIndividual, DecimalIndividual
from ..components import Population
from ..operators import RouletteWheelSelection
from ..operators import UniformCrossover
from ..operators import FlipBitMutation

class GAEngineTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_binary_run(self):
        """
        Make sure GA engine can run correctly.
        """
        indv_template = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
        population = Population(indv_template=indv_template, size=50).init()
        selection = RouletteWheelSelection()
        crossover = UniformCrossover(pc=0.8, pe=0.5)
        mutation = FlipBitMutation(pm=0.1)
        engine = GAEngine(population=population, selection=selection, crossover=crossover,
          mutation=mutation)

        @engine.fitness_register
        @engine.minimize
        def fitness(indv):
            x, = indv.solution
            return x + 10 * sin(5 * x) + 7 * cos(4 * x)

        engine.run(50)

    def test_decimal_run(self):
        """
        Make sure GA engine can run correctly with decimal encoding individuals.
        """
        indv_template = DecimalIndividual(ranges=[(0, 10)], eps=0.001)
        population = Population(indv_template=indv_template, size=50).init()
        selection = RouletteWheelSelection()
        crossover = UniformCrossover(pc=0.8, pe=0.5)
        mutation = FlipBitMutation(pm=0.1)
        engine = GAEngine(population=population, selection=selection, crossover=crossover,
          mutation=mutation)

        @engine.fitness_register
        @engine.minimize
        def fitness(indv):
            x, = indv.solution
            return x + 10 * sin(5 * x) + 7 * cos(4 * x)

        engine.run(50)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(GAEngineTest)
    unittest.TextTestRunner(verbosity=2).run(suite)