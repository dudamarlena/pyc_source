# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/operators/mutation/flip_bit_mutation.py
# Compiled at: 2019-02-10 16:12:45
# Size of source mod 2**32: 2084 bytes
""" Flip Bit mutation implementation. """
from random import random, uniform
from ...mpiutil import MPIUtil
from ...plugin_interfaces.operators.mutation import Mutation
from ...components.binary_individual import BinaryIndividual
from ...components.decimal_individual import DecimalIndividual
mpi = MPIUtil()

class FlipBitMutation(Mutation):
    __doc__ = ' Mutation operator with Flip Bit mutation implementation.\n\n    :param pm: The probability of mutation (usually between 0.001 ~ 0.1)\n    :type pm: float in range (0.0, 1.0]\n    '

    def __init__(self, pm):
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')
        self.pm = pm

    def mutate(self, individual, engine):
        """ Mutate the individual.

        :param individual: The individual on which crossover operation occurs
        :type individual: :obj:`lsga.components.IndividualBase`

        :param engine: Current genetic algorithm engine
        :type engine: :obj:`lsga.engine.GAEngine`

        :return: A mutated individual
        :rtype: :obj:`lsga.components.IndividualBase`
        """
        do_mutation = True if random() <= self.pm else False
        if do_mutation:
            for i, genome in enumerate(individual.chromsome):
                no_flip = True if random() > self.pm else False
                if no_flip:
                    pass
                else:
                    if type(individual) is BinaryIndividual:
                        individual.chromsome[i] = genome ^ 1
                    else:
                        if type(individual) is DecimalIndividual:
                            a, b = individual.ranges[i]
                            eps = individual.precisions[i]
                            n_intervals = (b - a) // eps
                            n = int(uniform(0, n_intervals + 1))
                            individual.chromsome[i] = a + n * eps
                        else:
                            raise TypeError('Wrong individual type: {}'.format(type(individual)))

            individual.solution = individual.decode()
        return individual