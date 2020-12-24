# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/operators/selection/roulette_wheel_selection.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1381 bytes
""" Roulette Wheel Selection implementation. """
from random import random
from bisect import bisect_right
from itertools import accumulate
from ...plugin_interfaces.operators.selection import Selection

class RouletteWheelSelection(Selection):
    __doc__ = ' Selection operator with fitness proportionate selection(FPS) or\n    so-called roulette-wheel selection implementation.\n    '

    def __init__(self):
        pass

    def select(self, population, fitness):
        """ Select a pair of parent using FPS algorithm.

        :param population: Population where the selection operation occurs.
        :type population: :obj:`lsga.components.Population`

        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`lsga.components.IndividualBase`
        """
        fit = population.all_fits(fitness)
        min_fit = min(fit)
        fit = [i - min_fit for i in fit]
        sum_fit = sum(fit)
        wheel = list(accumulate([i / sum_fit for i in fit]))
        father_idx = bisect_right(wheel, random())
        father = population[father_idx]
        mother_idx = (father_idx + 1) % len(wheel)
        mother = population[mother_idx]
        return (
         father, mother)