# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/analysis/fitness_store.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1584 bytes
from ..plugin_interfaces.analysis import OnTheFlyAnalysis

class FitnessStore(OnTheFlyAnalysis):
    __doc__ = ' Built-in on-the-fly analysis plugin class for storing fitness related data during iteration.\n\n    Attribute:\n        interval(:obj:`int`): The analysis interval in evolution iteration, default \n                              value is 1 meaning analyze every step.\n        master_only(:obj:`bool`): Flag for if the analysis plugin is only effective \n                                  in master process. Default is True.\n    '
    interval = 1
    master_only = True

    def setup(self, ng, engine):
        self.ngs = []
        self.fitness_values = []
        self.solution = []

    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        best_fit = engine.ori_fmax
        self.ngs.append(g)
        self.solution.append(best_indv.solution)
        self.fitness_values.append(best_fit)

    def finalize(self, population, engine):
        with open('best_fit.py', 'w', encoding='utf-8') as (f):
            f.write('best_fit = [\n')
            for ng, x, y in zip(self.ngs, self.solution, self.fitness_values):
                f.write('    ({}, {}, {}),\n'.format(ng, x, y))

            f.write(']\n\n')
        self.logger.info('Best fitness values are written to best_fit.py')