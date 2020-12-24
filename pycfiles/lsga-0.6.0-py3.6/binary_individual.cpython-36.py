# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/components/binary_individual.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 3534 bytes
""" Module for Individual with binary encoding.
"""
from math import log2
from itertools import accumulate
import logging
from .individual import IndividualBase
from ..mpiutil import MPIUtil
mpi = MPIUtil()

class BinaryIndividual(IndividualBase):
    __doc__ = '\n    Class for individual in population. Random solution will be initialized\n    by default.\n\n    :param ranges: value ranges for all entries in solution.\n    :type ranges: tuple list\n\n    :param eps: decrete precisions for binary encoding, default is 0.001.\n    :type eps: float or float list (with the same length with ranges)\n\n    .. Note:\n\n        The decrete precisions for different components in varants may be\n        adjusted automatically (possible precision loss) if eps and ranges\n        are not appropriate.\n    '

    def __init__(self, ranges, eps=0.001):
        super(self.__class__, self).__init__(ranges, eps)
        self.lengths = []
        for i, ((a, b), eps) in enumerate(zip(self.ranges, self.eps)):
            length = int(log2((b - a) / eps))
            precision = (b - a) / 2 ** length
            self.lengths.append(length)
            self.precisions[i] = precision

        self.gene_indices = self._get_gene_indices()
        self.init()

    def encode(self):
        """ Encode solution to gene sequence in individual using different encoding.
        """
        chromsome = []
        for var, (a, _), length, eps in zip(self.solution, self.ranges, self.lengths, self.precisions):
            chromsome.extend(self.binarize(var - a, eps, length))

        return chromsome

    def decode(self):
        """ Decode gene sequence to solution of target function.
        """
        solution = [self.decimalize(self.chromsome[start:end], eps, lower_bound) for (start, end), (lower_bound, _), eps in zip(self.gene_indices, self.ranges, self.precisions)]
        return solution

    def _get_gene_indices(self):
        """
        Helper function to get gene slice indices.
        """
        end_indices = list(accumulate(self.lengths))
        start_indices = [0] + end_indices[:-1]
        return list(zip(start_indices, end_indices))

    @staticmethod
    def binarize(decimal, eps, length):
        """ Helper function to convert a float to binary sequence.

        :param decimal: the decimal number to be converted
        :type decimal: float

        :param eps: the decrete precision of binary sequence
        :type eps: float

        :param length: the length of binary sequence.
        :type length: int
        """
        n = int(decimal / eps)
        bin_str = '{:0>{}b}'.format(n, length)
        return [int(i) for i in bin_str]

    @staticmethod
    def decimalize(binary, eps, lower_bound):
        """ Helper function to convert a binary sequence back to decimal number.

        :param binary: The binary list to be converted
        :type binary: list of int

        :param eps: the decrete precision of binary sequence
        :type eps: float

        :param lower_bound: the lower bound for decimal number
        :type lower_bound: float
        """
        bin_str = ''.join([str(bit) for bit in binary])
        return lower_bound + int(bin_str, 2) * eps