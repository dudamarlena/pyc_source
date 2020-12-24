# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/catastrophe.py
# Compiled at: 2016-03-12 06:54:43
# Size of source mod 2**32: 1973 bytes
import abc
from pynetics import Catastrophe
from .utils import take_chances

class ProbabilityBasedCatastrophe(Catastrophe, metaclass=abc.ABCMeta):
    __doc__ = ' Base class for some bundled probability based catastrophe methods.\n\n    This method will have a probability to be triggered. Is expected this\n    probability to be very little.\n    '

    def __init__(self, probability):
        """ Initializes this catastrophe method.

        :param probability: The probability fot the catastrophe to happen.
        """
        self._ProbabilityBasedCatastrophe__probability = probability

    def __call__(self, population):
        if take_chances(self._ProbabilityBasedCatastrophe__probability):
            self.perform(population)

    @abc.abstractmethod
    def perform(self, population):
        """ Returns a list of the individuals to remove from population.

        :param population: The population from where extract individuals.
        :return: The individuals to retain after the catastrophe application.
        """
        pass


class PackingByProbability(ProbabilityBasedCatastrophe):
    __doc__ = ' Replaces all repeated individuals maintaining only one copy of each. '

    def perform(self, population):
        """ Replaces all repeated individuals by new ones.

        :param population: The population where apply the catastrophe.
        """
        visited_individuals = []
        for i in range(len(population)):
            if population[i] in visited_individuals:
                population[i] = population.spawning_pool.spawn()
            visited_individuals.append(population[i])


class DoomsdayByProbability(ProbabilityBasedCatastrophe):
    __doc__ = ' Replaces all but the best individual. '

    def perform(self, population):
        """ Replaces all the individuals but the best.

        :param population: The population where apply the catastrophe.
        """
        for i in range(1, len(population)):
            population[i] = population.spawning_pool.spawn()