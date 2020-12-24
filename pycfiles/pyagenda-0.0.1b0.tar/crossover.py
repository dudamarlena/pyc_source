# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/solutions/evolution/crossover.py
# Compiled at: 2015-12-21 17:12:57
import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype

class AbstractCrossover(Operator):

    def __init__(self, type, size):
        super(AbstractCrossover, self).__init__(type)
        self.__size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)


class AverageCrossover(AbstractCrossover):

    def __init__(self, size=100):
        super(AverageCrossover, self).__init__(PointGenotype, size)

    def cross(self, p1, p2):
        genotype = PointGenotype((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)
        return genotype


class AverageFloatCrossover(AbstractCrossover):

    def __init__(self, size=100):
        super(AverageFloatCrossover, self).__init__(FloatGenotype, size)

    def cross(self, p1, p2):
        genotype = FloatGenotype([ sum(p) / 2.0 for p in zip(p1.genes, p2.genes) ])
        return genotype


class SinglePointCrossover(AbstractCrossover):

    def __init__(self, size=100):
        super(SinglePointCrossover, self).__init__(FloatGenotype, size)

    def cross(self, p1, p2):
        crossingPoint = random.randint(1, len(p1.genes))
        return FloatGenotype(p1.genes[:crossingPoint] + p2.genes[crossingPoint:])


class UniformCrossover(AbstractCrossover):

    def __init__(self, size=100, probability=0.5):
        super(UniformCrossover, self).__init__(FloatGenotype, size)
        self.probability = probability

    def cross(self, p1, p2):
        return FloatGenotype([ p1.genes[i] if random.random() < self.probability else p2.genes[i] for i in range(len(p1.genes))
                             ])