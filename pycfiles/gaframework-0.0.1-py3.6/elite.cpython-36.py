# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/elite.py
# Compiled at: 2019-06-14 12:15:44
# Size of source mod 2**32: 704 bytes
import math
from GaPy.genetic_operator import *
from GaPy.population import *
from GaPy.event import *
from GaPy.event_args import *

class Elite(GeneticOperator):

    def __init__(self, percentage=5.0):
        super().__init__(percentage)

    def invoke(self, population, fitness_function):
        if self.enabled:
            population.clear_elites()
            temp = sorted((population.chromosomes), key=(lambda x: x.fitness), reverse=True)
            p = len(population) * (self._p / 100)
            elites = temp[:math.ceil(p)]
            for elite in elites:
                elite.elite = True