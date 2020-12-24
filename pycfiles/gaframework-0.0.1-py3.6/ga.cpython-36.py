# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/ga.py
# Compiled at: 2019-07-07 04:41:39
# Size of source mod 2**32: 5105 bytes
from GaPy.single_point_crossover import *
from GaPy.binary_mutate import *
from GaPy.elite import *
from GaPy.event import *
from GaPy.event_args import *
from GaPy.exceptions import *

class Ga:

    def __init__(self, population: Population):
        self.population = population
        self._operators = []
        self.generation_complete_event = Event()
        self.initial_evaluation_complete_event = Event()
        self.operator_complete_event = Event()

    def append_operator(self, operator: GeneticOperator):
        if not isinstance(operator, GeneticOperator):
            raise TypeError('Operators should be derived from the abstract base class GeneticOperator.')
        self._operators.append(operator)

    def run(self, fitness_function, terminate_function):
        evaluation_count = self._evaluate(fitness_function)
        generation_count = 0
        args = GaEventArgs(self.population, generation_count, evaluation_count)
        self.initial_evaluation_complete_event(args)
        while not terminate_function(self.population, generation_count, evaluation_count):
            generation_count += 1
            for operator in self._operators:
                operator.invoke(self.population, fitness_function)
                evaluation_count += operator.evaluation_count
                args = GaEventArgs(self.population, generation_count, evaluation_count)
                self.operator_complete_event(args)

            evaluation_count += self._evaluate(fitness_function)
            args = GaEventArgs(self.population, generation_count, evaluation_count)
            self.generation_complete_event(args)

    def _evaluate(self, fitness_function):
        """Evaluates the whole population."""
        evaluation_count = 0
        try:
            for chromosome in self.population.chromosomes:
                if not chromosome.elite:
                    chromosome.evaluate(fitness_function)
                    evaluation_count += 1

            return evaluation_count
        except TypeError as ex:
            raise TypeError('Ensure the supplied fitness function accepts a single argument representing the chromosome to be evaluated.')

    @staticmethod
    def normalise_fitness(value: float, value_a: float, min_value=0):
        pass

    @staticmethod
    def get_range_constant(range_min: float, range_max: float, bits: int):
        if range_min >= range_max:
            raise BadRangeException("The value of 'range_value_high' must be greater than 'range_value_low'.")
        range = range_max - range_min
        return range / (pow(2, bits) - 1)

    @staticmethod
    def normalise_binary(binary_string_value: str, range_min: float=1e-10, range_max: float=1.0):
        value = int(binary_string_value, 2)
        range_constant = Ga.get_range_constant(range_min, range_max, len(binary_string_value))
        value *= range_constant
        return value + range_min

    @staticmethod
    def clamp(n: float):
        """Clamps a value between 0.0. and 1.0"""
        return float(max(min(0, n), 1.0))

    @staticmethod
    def schaffer_f6_function(x, y):
        xsqrdysqrd = x * x + y * y
        return 0.5 - (math.sin(math.sqrt(xsqrdysqrd)) ** 2 - 0.5) / (1.0 + 0.001 * xsqrdysqrd) ** 2