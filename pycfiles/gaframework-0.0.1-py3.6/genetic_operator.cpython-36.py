# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/genetic_operator.py
# Compiled at: 2019-06-14 11:49:55
# Size of source mod 2**32: 849 bytes
from abc import ABC, abstractmethod
from typing import List, Set, Dict, Tuple, Optional
from GaPy.chromosome import Chromosome

class GeneticOperator(ABC):

    @abstractmethod
    def __init__(self, p: float=1.0):
        self._p = p
        self.enabled = True
        self.evaluation_count = 0

    @abstractmethod
    def invoke(self, population, fitness_function):
        pass

    def _evaluate(self, chromosomes: List[Chromosome], fitness_function):
        try:
            for chromosome in chromosomes:
                chromosome.fitness = fitness_function(chromosome)
                self.evaluation_count += 1

        except TypeError as ex:
            raise TypeError('Ensure the supplied fitness function accepts a single argument representing the chromosome to be evaluated.')