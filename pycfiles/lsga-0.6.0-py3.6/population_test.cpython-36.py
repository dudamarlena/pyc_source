# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/tests/population_test.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1691 bytes
""" Test case for Population
"""
import unittest
from lsga.components import Population, BinaryIndividual

class PopulationTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True
        self.indv_template = BinaryIndividual(ranges=[(0, 1)])

        def fitness(indv):
            x, = indv.solution
            return x ** 3 - 60 * x ** 2 + 900 * x + 100

        self.fitness = fitness

    def test_initialization(self):
        """ Make sure a population can be initialized correctly. """
        population = Population(indv_template=(self.indv_template), size=10)
        self.assertListEqual(population.individuals, [])
        population.init()
        self.assertEqual(len(population.individuals), 10)
        self.assertTrue(isinstance(population[0], BinaryIndividual))

    def test_new_population(self):
        """ Make sure population can clone a new population. """
        population = Population(indv_template=(self.indv_template), size=10)
        population.init()
        new_population = population.new()
        self.assertEqual(new_population.size, 10)
        self.assertListEqual(new_population.individuals, [])

    def test_all_fits(self):
        population = Population(indv_template=(self.indv_template), size=10)
        population.init()
        all_fits = population.all_fits(fitness=(self.fitness))
        self.assertEqual(len(all_fits), 10)
        for fit in all_fits:
            self.assertTrue(type(fit) is float)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(PopulationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)