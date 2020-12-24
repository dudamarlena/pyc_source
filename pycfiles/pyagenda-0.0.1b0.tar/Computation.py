# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/Computation.py
# Compiled at: 2015-12-21 16:57:02
from pyage.inject import Inject

class Computation:

    @Inject('population_generator', 'stop_condition', 'op')
    def __init__(self):
        pass

    def run(self):
        population = self.population_generator()
        print population
        while True:
            for operator in self.op:
                operator(population)

            if self.stop_condition.should_stop(population):
                break