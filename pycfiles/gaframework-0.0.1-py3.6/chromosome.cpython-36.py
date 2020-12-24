# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/chromosome.py
# Compiled at: 2019-12-29 14:20:48
# Size of source mod 2**32: 1153 bytes
import random

class Chromosome:

    def __init__(self, genes=[]):
        self.genes = genes
        self.fitness = 0
        self.elite = False

    @staticmethod
    def create(chromosome_length: int, population_size: int=1):
        random.seed()
        result = []
        for c in range(population_size):
            genes = []
            for i in range(chromosome_length):
                genes.append(bool(random.getrandbits(1)))

            result.append(Chromosome(genes))

        return result

    def evaluate(self, fitness_function):
        self.fitness = fitness_function(self)

    def __str__(self):
        s = ''
        for gene in self.genes:
            if gene:
                s += '1'
            else:
                s += '0'

        return s

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.genes)