# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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