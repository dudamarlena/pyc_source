# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/plugin_interfaces/operators/selection.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 711 bytes
""" Module for Genetic Algorithm selection operator class """
from ..metaclasses import SelectionMeta

class Selection(metaclass=SelectionMeta):
    __doc__ = ' Class for providing an interface to easily extend the behavior of selection\n    operation.\n    '

    def select(self, population, fitness):
        """ Called when we need to select parents from a population to later breeding.

        :param population: The current population
        :type population: lsga.compoenents.Population

        :return parents: Two selected individuals for crossover
        :type parents: tuple of gaft.components.IndividualBase
        """
        raise NotImplementedError