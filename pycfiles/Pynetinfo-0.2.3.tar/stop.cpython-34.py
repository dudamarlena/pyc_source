# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/stop.py
# Compiled at: 2016-03-12 06:09:25
# Size of source mod 2**32: 1976 bytes
from pynetics import StopCondition

class StepsNum(StopCondition):
    """StepsNum"""

    def __init__(self, steps):
        """ Initializes this function with the number of iterations.

        :param steps: The number of iterations to do before stop.
        """
        self.steps = steps

    def __call__(self, genetic_algorithm):
        """ Checks if this stop criteria is met.

        It will look at the generation of the genetic algorithm. It's expected
        that, if its generation is greater or equal than the specified in
        initialization method, the criteria is met.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """
        return genetic_algorithm.generation >= self.steps


class FitnessBound(StopCondition):
    """FitnessBound"""

    def __init__(self, fitness_bound):
        """ Initializes this function with the upper bound for the fitness.

        :param fitness_bound: A fitness value. The criteria will be met when the
            fitness in the algorithm (in one or all populations managed, see
            below) is greater than this specified fitness.
        """
        self.fitness_bound = fitness_bound

    def __call__(self, genetic_algorithm):
        """ Checks if this stop criteria is met.

        It will look at the fitness of the best individual the genetic algorithm
        has discovered. In case of its fitness being greater or equal than the
        specified at initialization time, the condition will be met and the
        algorithm will stop.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """
        return genetic_algorithm.best().fitness() >= self.fitness_bound