# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/plugin_interfaces/analysis.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 2028 bytes
from .metaclasses import AnalysisMeta

class OnTheFlyAnalysis(metaclass=AnalysisMeta):
    __doc__ = ' Class for providing an interface to easily extend and customize the behavior\n    of the on-the-fly analysis functionality of lsga.\n\n    Attribute:\n\n        interval(:obj:`int`): The analysis interval in evolution iteration, default \n                              value is 1 meaning analyze every step.\n\n        master_only(:obj:`bool`): Flag for if the analysis plugin is only effective \n                                  in master process. Default is True.\n    '
    master_only = False
    interval = 1

    def setup(self, ng, engine):
        """ Function called right before the start of genetic algorithm main iteration
        to allow for custom setup of the analysis object.

        :param ng: The number of generation.
        :type ng: int

        :param engine: The current GAEngine where the analysis is running.
        :type engine: gaft.engine.GAEngine
        """
        raise NotImplementedError

    def register_step(self, g, population, engine):
        """
        Function called in each iteration step.

        :param g: Current generation number.
        :type g: int

        :param population: The up to date population of the iteration.
        :type population: Population

        :param engine: The current GAEngine where the analysis is running.
        :type engine: gaft.engine.GAEngine
        """
        raise NotImplementedError

    def finalize(self, population, engine):
        """
        Called after the iteration to allow for custom finalization and
        post-processing of the collected data.

        :param population: The up to date population of the iteration.
        :type population: Population

        :param engine: The current GAEngine where the analysis is running.
        :type engine: gaft.engine.GAEngine
        """
        raise NotImplementedError