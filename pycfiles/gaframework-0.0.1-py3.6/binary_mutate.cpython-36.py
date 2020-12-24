# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/binary_mutate.py
# Compiled at: 2019-07-07 03:10:08
# Size of source mod 2**32: 1381 bytes
from GaPy.genetic_operator import *
from GaPy.chromosome import *

class BinaryMutate(GeneticOperator):

    def __init__(self, probability=0.01):
        super().__init__(probability)

    def invoke(self, population, fitness_function):
        if self.enabled:
            for c in population.chromosomes:
                self._mutate_chromosome(c)

    def _mutate_chromosome(self, chromosome):
        for i in range(len(chromosome)):
            p = random.random()
            if p < self._p:
                chromosome.genes[i] = self._mutate_gene(chromosome.genes[i])

    def _mutate_gene(self, gene):
        if isinstance(gene, bool):
            return not gene
        if isinstance(gene, int) or isinstance(gene, float):
            return gene * -1
        raise TypeError('The gene is of the incorrect type. The type should be bool, float, int.')