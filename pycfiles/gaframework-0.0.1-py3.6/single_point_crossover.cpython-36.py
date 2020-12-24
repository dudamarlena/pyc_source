# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/single_point_crossover.py
# Compiled at: 2019-07-07 03:30:27
# Size of source mod 2**32: 4083 bytes
import math
from GaPy.genetic_operator import *
from GaPy.population import *
from GaPy.event import *
from GaPy.event_args import *
from GaPy.exceptions import *

class SinglePointCrossover(GeneticOperator):

    def __init__(self, probability=0.85):
        super().__init__(probability)
        self.evaluations = 0
        self.parent_selection_method = ParentSelectionMethod.stochastic_universal_sampling
        self.replacement_method = ReplacementMethod.generational_replacement
        self.crossover_complete_event = Event()

    def invoke(self, population, fitness_function):
        p = random.random()
        if self.enabled:
            if p <= self._p:
                self.evaluations = 0
                p_size = len(population)
                new_chromosomes = population.get_elites()
                for child_count in range(math.ceil((p_size - len(new_chromosomes)) / 2.0)):
                    parents = population.select_parents(self.parent_selection_method)
                    parent_len_0 = len(parents[0])
                    if parent_len_0 != len(parents[1]):
                        raise ParentMismatchError
                    point = random.randint(0, parent_len_0 - 1)
                    children = self._crossover(parents, point)
                    args = CrossoverEventArgs(parents, children, [point])
                    self.crossover_complete_event(args)
                    new_chromosomes.extend(children)

                if self.replacement_method == ReplacementMethod.generational_replacement:
                    population.chromosomes = new_chromosomes[:p_size]
                elif self.replacement_method == ReplacementMethod.delete_last:
                    raise NotImplementedError('This functionality has not been implemented yet.')

    def _crossover(self, parents: List[Chromosome], point: int):
        return [
         Chromosome(parents[0].genes[:point] + parents[1].genes[point:]),
         Chromosome(parents[1].genes[:point] + parents[0].genes[point:])]