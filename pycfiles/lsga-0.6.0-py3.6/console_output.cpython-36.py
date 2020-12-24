# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/analysis/console_output.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1536 bytes
from ..plugin_interfaces.analysis import OnTheFlyAnalysis

class ConsoleOutput(OnTheFlyAnalysis):
    __doc__ = ' Built-in on-the-fly analysis plugin class for outputing log on console.\n\n    Attribute:\n\n        interval(:obj:`int`): The analysis interval in evolution iteration, default \n                              value is 1 meaning analyze every step.\n\n        master_only(:obj:`bool`): Flag for if the analysis plugin is only effective \n                                  in master process. Default is True.\n    '
    interval = 1
    master_only = True

    def setup(self, ng, engine):
        generation_info = 'Generation number: {}'.format(ng)
        population_info = 'Population number: {}'.format(engine.population.size)
        self.logger.info('{} {}'.format(generation_info, population_info))

    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        ng_info = 'Generation: {}, '.format(g + 1)
        fit_info = 'best fitness: {:.3f}, '.format(engine.ori_fmax)
        scaled_info = 'scaled fitness: {:.3f}'.format(engine.fmax)
        msg = ng_info + fit_info + scaled_info
        self.logger.info(msg)

    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x = best_indv.solution
        y = engine.ori_fmax
        msg = 'Optimal solution: ({}, {})'.format(x, y)
        self.logger.info(msg)