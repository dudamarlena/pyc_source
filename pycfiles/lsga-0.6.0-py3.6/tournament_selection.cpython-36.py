# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/operators/selection/tournament_selection.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1762 bytes
""" Tournament Selection implementation. """
from random import sample
from ...plugin_interfaces.operators.selection import Selection

class TournamentSelection(Selection):
    __doc__ = ' Selection operator using Tournament Strategy with tournament size equals\n    to two by default.\n\n    :param tournament_size: Individual number in one tournament\n    :type tournament_size: int\n    '

    def __init__(self, tournament_size=2):
        self.tournament_size = tournament_size

    def select(self, population, fitness):
        """ Select a pair of parent using Tournament strategy.

        :param population: Population where the selection operation occurs.
        :type population: :obj:`lsga.components.Population`

        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`lsga.components.IndividualBase`
        """
        all_fits = population.all_fits(fitness)

        def complete(competitors):
            key = lambda indv: all_fits[population.individuals.index(indv)]
            return max(competitors, key=key)

        if self.tournament_size >= len(population):
            msg = 'Tournament size({}) is larger than population size({})'
            raise ValueError(msg.format(self.tournament_size, len(population)))
        competitors_1 = sample(population.individuals, self.tournament_size)
        competitors_2 = sample(population.individuals, self.tournament_size)
        father, mother = complete(competitors_1), complete(competitors_2)
        return (
         father, mother)