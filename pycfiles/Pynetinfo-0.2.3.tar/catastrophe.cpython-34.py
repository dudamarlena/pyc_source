# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/catastrophe.py
# Compiled at: 2016-03-12 06:54:43
# Size of source mod 2**32: 1973 bytes
import abc
from pynetics import Catastrophe
from .utils import take_chances

class ProbabilityBasedCatastrophe(Catastrophe, metaclass=abc.ABCMeta):
    """ProbabilityBasedCatastrophe"""

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
    """PackingByProbability"""

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
    """DoomsdayByProbability"""

    def perform(self, population):
        """ Replaces all the individuals but the best.

        :param population: The population where apply the catastrophe.
        """
        for i in range(1, len(population)):
            population[i] = population.spawning_pool.spawn()