# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/operators/crossover/uniform_crossover.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 1861 bytes
""" Uniform Crossover operator implementation. """
from random import random
from copy import deepcopy
from ...plugin_interfaces.operators.crossover import Crossover

class UniformCrossover(Crossover):
    __doc__ = ' Crossover operator with uniform crossover algorithm,\n    see https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)\n\n    :param pc: The probability of crossover (usaully between 0.25 ~ 1.0)\n    :type pc: float in (0.0, 1.0]\n\n    :param pe: Gene exchange probability.\n    :type pe: float in range (0.0, 1.0]\n    '

    def __init__(self, pc, pe=0.5):
        if pc <= 0.0 or pc > 1.0:
            raise ValueError('Invalid crossover probability')
        self.pc = pc
        if pe <= 0.0 or pe > 1.0:
            raise ValueError('Invalid genome exchange probability')
        self.pe = pe

    def cross(self, father, mother):
        """ Cross chromsomes of parent using uniform crossover method.

        :param population: Population where the selection operation occurs.
        :type population: :obj:`lsga.components.Population`

        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`lsga.components.IndividualBase`
        """
        do_cross = True if random() <= self.pc else False
        if not do_cross:
            return (father.clone(), mother.clone())
        else:
            chrom1 = deepcopy(father.chromsome)
            chrom2 = deepcopy(mother.chromsome)
            for i, (g1, g2) in enumerate(zip(chrom1, chrom2)):
                do_exchange = True if random() < self.pe else False
                if do_exchange:
                    chrom1[i], chrom2[i] = g2, g1

            child1, child2 = father.clone(), father.clone()
            child1.init(chromsome=chrom1)
            child2.init(chromsome=chrom2)
            return (
             child1, child2)