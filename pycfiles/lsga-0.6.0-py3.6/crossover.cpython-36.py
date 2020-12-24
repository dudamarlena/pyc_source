# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/plugin_interfaces/operators/crossover.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1029 bytes
""" Module for Genetic Algorithm crossover operator class """
from ..metaclasses import CrossoverMeta

class Crossover(metaclass=CrossoverMeta):
    __doc__ = ' Class for providing an interface to easily extend the behavior of crossover\n    operation between two individuals for children breeding.\n\n    Attributes:\n\n        pc(:obj:`float`): The probability of crossover (usaully between 0.25 ~ 1.0)\n    '
    pc = 0.8

    def cross(self, father, mother):
        """ Called when we need to cross parents to generate children.

        :param father: The parent individual to be crossed
        :type father: gaft.components.IndividualBase

        :param mother: The parent individual to be crossed
        :type mother: gaft.components.IndividualBase

        :return children: Two new children individuals
        :type children: tuple of gaft.components.IndividualBase
        """
        raise NotImplementedError