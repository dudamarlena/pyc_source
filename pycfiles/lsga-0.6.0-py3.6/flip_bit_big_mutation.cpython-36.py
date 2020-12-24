# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/operators/mutation/flip_bit_big_mutation.py
# Compiled at: 2019-02-10 16:12:32
# Size of source mod 2**32: 1881 bytes
from ...mpiutil import MPIUtil
from .flip_bit_mutation import FlipBitMutation
mpi = MPIUtil()

class FlipBitBigMutation(FlipBitMutation):
    __doc__ = ' Mutation operator using Flip Bit mutation implementation with adaptive\n    big mutation rate to overcome premature or local-best solution.\n\n    :param pm: The probability of mutation (usually between 0.001 ~ 0.1)\n    :type pm: float in (0.0, 1.0]\n\n    :param pbm: The probability of big mutation, usually more than 5 times\n                bigger than pm.\n    :type pbm: float\n\n    :param alpha: intensive factor\n    :type alpha: float, in range (0.5, 1)\n    '

    def __init__(self, pm, pbm, alpha):
        super(self.__class__, self).__init__(pm)
        if not 0.0 < pbm < 1.0:
            raise ValueError('Invalid big mutation probability')
        if pbm < 5 * pm:
            if mpi.is_master:
                self.logger.warning('Relative low probability for big mutation')
        self.pbm = pbm
        if not 0.5 < alpha < 1.0:
            raise ValueError('Invalid intensive factor, should be in (0.5, 1.0)')
        self.alpha = alpha

    def mutate(self, individual, engine):
        pm = self.pm
        if engine.fmax * self.alpha < engine.fmean:
            self.pm = self.pbm
        individual = super(self.__class__, self).mutate(individual, engine)
        self.pm = pm
        return individual