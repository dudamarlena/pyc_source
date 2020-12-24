# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/plugin_interfaces/operators/mutation.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 803 bytes
""" Module for Genetic Algorithm mutation operator class """
from ..metaclasses import MutationMeta

class Mutation(metaclass=MutationMeta):
    __doc__ = ' Class for providing an interface to easily extend the behavior of selection\n    operation.\n\n    Attributes:\n\n        pm(float): Default mutation probability, default is 0.1\n    '
    pm = 0.1

    def mutate(self, individual, engine):
        """ Called when an individual to be mutated.

        :param individual: The individual to be mutated
        :type individual: gaft.components.IndividualBase

        :param engine: The GA engine where the mutation operator belongs.
        :type engine: gaft.engine.GAEngine
        """
        raise NotImplementedError