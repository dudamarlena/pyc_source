# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/operators/selection/linear_ranking_selection.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 2063 bytes
""" Linear Ranking Selection implementation. """
from random import random
from itertools import accumulate
from bisect import bisect_right
from ...plugin_interfaces.operators.selection import Selection

class LinearRankingSelection(Selection):
    __doc__ = ' Selection operator using Linear Ranking selection method.\n\n    Reference: Baker J E. Adaptive selection methods for genetic\n    algorithms[C]//Proceedings of an International Conference on Genetic\n    Algorithms and their applications. 1985: 101-111.\n    '

    def __init__(self, pmin=0.1, pmax=0.9):
        self.pmin, self.pmax = pmin, pmax

    def select(self, population, fitness):
        """ Select a pair of parent individuals using linear ranking method.

        :param population: Population where the selection operation occurs.
        :type population: :obj:`lsga.components.Population`

        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`lsga.components.IndividualBase`
        """
        NP = len(population)
        all_fits = population.all_fits(fitness)
        indvs = population.individuals
        sorted_indvs = sorted(indvs, key=(lambda indv: all_fits[indvs.index(indv)]))
        p = lambda i: self.pmin + (self.pmax - self.pmin) * (i - 1) / (NP - 1)
        probabilities = [self.pmin] + [p(i) for i in range(2, NP)] + [self.pmax]
        psum = sum(probabilities)
        wheel = list(accumulate([p / psum for p in probabilities]))
        father_idx = bisect_right(wheel, random())
        father = sorted_indvs[father_idx]
        mother_idx = (father_idx + 1) % len(wheel)
        mother = sorted_indvs[mother_idx]
        return (
         father, mother)