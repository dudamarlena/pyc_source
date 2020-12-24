# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_elite.py
# Compiled at: 2019-06-14 12:47:33
# Size of source mod 2**32: 734 bytes
from unittest import TestCase
from GaPy.chromosome import *
from GaPy.population import *
from GaPy.elite import *

class TestElite(TestCase):

    def test_invoke(self):
        chromosomes = []
        for f in range(100):
            c = Chromosome()
            c.fitness = f
            chromosomes.append(c)

        population = Population(chromosomes)
        elites = population.get_elites()
        self.assertEqual(0, len(elites))
        elite = Elite(10)
        elite.invoke(population, None)
        elites = population.get_elites()
        self.assertEqual(10, len(elites))
        self.assertEqual(99, elites[9].fitness)