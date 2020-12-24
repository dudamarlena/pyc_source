# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/solutions/evolution/selection.py
# Compiled at: 2015-12-21 17:12:57
import random
from pyage.core.operator import Operator

class TournamentSelection(Operator):

    def __init__(self, type=None, size=20, tournament_size=20):
        super(TournamentSelection, self).__init__()
        self.size = size
        self.tournament_size = tournament_size

    def process(self, population):
        p = list(population)
        population[:] = []
        for i in range(self.size):
            sample = random.sample(p, self.tournament_size)
            winner = max(sample, key=lambda genotype: genotype.fitness)
            population.append(winner)
            p.remove(winner)