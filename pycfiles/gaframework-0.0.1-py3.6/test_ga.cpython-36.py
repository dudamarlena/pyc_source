# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_ga.py
# Compiled at: 2019-07-07 03:15:37
# Size of source mod 2**32: 3499 bytes
from unittest import TestCase
from GaPy.ga import *
generations = 0
evaluations = 0

def display_event_details(args: GaEventArgs):
    global evaluations
    global generations
    generations = args.generation_count
    evaluations = args.evaluation_count
    best_chromosome = args.population.best_chromosome()


def terminate(population: Population, generation_count: int, evaluation_count: int):
    if generation_count == 100:
        return True


def fitness(chromosome: Chromosome):
    try:
        return 0.1
    except Exception as ex:
        raise FitnessError('An error has occurred within the fitness function: {0}'.format(ex))


class TestGa(TestCase):

    def test_run(self):
        chromosomes = Chromosome.create(40, 100)
        population = Population(chromosomes)
        ga = Ga(population)
        ga.initial_evaluation_complete_event += display_event_details
        self.assertEqual(generations, 0)
        ga.generation_complete_event += display_event_details
        ga.run(fitness, terminate)
        self.assertEqual(100, generations)

    def test_get_range_constant(self):
        rc = Ga.get_range_constant(0, 100, 16)
        val = 65535 * rc
        self.assertTrue(val > 99.99 and val <= 100.0)
        val = 32767 * rc
        self.assertTrue(val > 49.99 and val <= 50.01)
        rc = Ga.get_range_constant(-50, 50, 16)
        self.assertTrue(val > 49.99 and val <= 50.01)

    def test_normalise_binary(self):
        bval = '1111111111111111'
        val = Ga.normalise_binary(bval, 0.0, 100.0)
        self.assertTrue(val > 99.99 and val <= 100.0)
        val = Ga.normalise_binary(bval, -50.0, 50.0)
        self.assertTrue(val > 49.99 and val <= 50.01)
        bval = '0111111111111111'
        val = Ga.normalise_binary(bval, 0.0, 100.0)
        self.assertTrue(val > 49.99 and val <= 50.0)
        val = Ga.normalise_binary(bval, -50.0, 50.0)
        self.assertTrue(val > -0.99 and val <= 0.01)
        val = Ga.normalise_binary(bval, 50.0, 150.0)
        self.assertTrue(val > 99.99 and val <= 100.01)

    def test_schaffer_f6_function(self):
        file = open('f6.csv', 'w')
        for x in range(-100, 100):
            y = 0
            z = Ga.schaffer_f6_function(x, y)
            file.write('{0},{1},{2}\r\n'.format(x, y, z))

        file.close()
        x = 0.0
        y = 0.0
        r = Ga.schaffer_f6_function(x, y)
        self.assertEqual(1.0, r)