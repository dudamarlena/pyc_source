# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_population.py
# Compiled at: 2019-07-07 03:03:57
# Size of source mod 2**32: 4184 bytes
from unittest import TestCase
from GaPy.population import *
from GaPy.exceptions import *

class TestPopulation(TestCase):

    def test__fps_selection(self):
        chromosomes = Chromosome.create(16, 100)
        for chromosome in chromosomes:
            chromosome.fitness = random.random()

        population = Population(chromosomes)
        parents = population._fps_selection()
        self.assertEqual(2, len(parents))

    def test__fps_select(self):
        chromosomes = []
        for f in range(16):
            c = Chromosome()
            c.fitness = f
            chromosomes.append(c)

        population = Population(chromosomes)
        parent = population._fps_select(4.5)
        self.assertEqual(3, parent.fitness)

    def test__sus_selection(self):
        chromosomes = Chromosome.create(16, 100)
        for chromosome in chromosomes:
            chromosome.fitness = random.random()

        population = Population(chromosomes)
        parents = population._sus_selection()
        self.assertEqual(2, len(parents))
        parents = population._sus_selection(16)
        self.assertEqual(16, len(parents))

    def test__tour_selection(self):
        chromosomes = Chromosome.create(16, 100)
        for chromosome in chromosomes:
            chromosome.fitness = random.random()

        population = Population(chromosomes)
        parents = population._tour_selection()
        self.assertEqual(2, len(parents))

    def test__random_selection(self):
        chromosomes = Chromosome.create(16, 100)
        for chromosome in chromosomes:
            chromosome.fitness = random.random()

        population = Population(chromosomes)
        parents = population._random_selection()
        self.assertEqual(2, len(parents))

    def test_total_fitness(self):
        chromosomes = Chromosome.create(16, 100)
        for chromosome in chromosomes:
            chromosome.fitness = 0.5

        population = Population(chromosomes)
        total_fitness = population.total_fitness()
        self.assertEqual(50.0, total_fitness)

    def test_get_elites(self):
        chromosomes = Chromosome.create(16, 100)
        for i in range(5):
            elite = random.choice(chromosomes)
            elite.elite = True

        population = Population(chromosomes)
        elites = population.get_elites()
        self.assertEqual(5, len(elites))

    def test_worst_chromosome(self):
        chromosomes = []
        for f in range(16):
            c = Chromosome()
            c.fitness = f
            chromosomes.append(c)

        population = Population(chromosomes)
        best = population.worst_chromosome()
        self.assertEqual(0, best.fitness)

    def test_best_chromosome(self):
        chromosomes = []
        for f in range(16):
            c = Chromosome()
            c.fitness = f
            chromosomes.append(c)

        population = Population(chromosomes)
        best = population.best_chromosome()
        self.assertEqual(15, best.fitness)

    def test_test_top(self):
        chromosomes = []
        for f in range(16):
            c = Chromosome()
            c.fitness = f
            chromosomes.append(c)

        population = Population(chromosomes)
        top = population.top(4)
        self.assertEqual(15, top[0].fitness)
        self.assertEqual(14, top[1].fitness)
        self.assertEqual(13, top[2].fitness)
        self.assertEqual(12, top[3].fitness)