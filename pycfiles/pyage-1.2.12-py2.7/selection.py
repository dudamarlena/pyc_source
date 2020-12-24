# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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