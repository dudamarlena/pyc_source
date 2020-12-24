# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/components/individual.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 4399 bytes
from random import uniform
from copy import deepcopy

class SolutionRanges(object):
    __doc__ = ' Descriptor for solution ranges.\n    '

    def __init__(self):
        self._SolutionRanges__ranges = []

    def __get__(self, obj, owner):
        return self._SolutionRanges__ranges

    def __set__(self, obj, ranges):
        if type(ranges) not in [tuple, list]:
            raise TypeError('solution ranges must be a list of range tuples')
        for rng in ranges:
            if type(rng) not in [tuple, list]:
                raise TypeError('range({}) is not a tuple containing two numbers'.format(rng))
            if len(rng) != 2:
                raise ValueError('length of range({}) not equal to 2')
            a, b = rng
            if a >= b:
                raise ValueError('Wrong range value {}'.format(rng))

        self._SolutionRanges__ranges = ranges


class DecretePrecision(object):
    __doc__ = ' Descriptor for individual decrete precisions.\n    '

    def __init__(self):
        self._DecretePrecision__precisions = []

    def __get__(self, obj, owner):
        return self._DecretePrecision__precisions

    def __set__(self, obj, precisions):
        if type(precisions) in [int, float]:
            precisions = [
             precisions] * len(obj.ranges)
        else:
            if type(precisions) not in [tuple, list]:
                raise TypeError('precisions must be a list of numbers')
            if len(precisions) != len(obj.ranges):
                raise ValueError('Lengths of eps and ranges should be the same')
        for (a, b), eps in zip(obj.ranges, precisions):
            if eps > b - a:
                msg = 'Invalid precision {} in range ({}, {})'.format(eps, a, b)
                raise ValueError(msg)

        self._DecretePrecision__precisions = precisions


class IndividualBase(object):
    __doc__ = ' Base class for individuals.\n\n    :param ranges: value ranges for all entries in solution.\n    :type ranges: tuple list\n\n    :param eps: decrete precisions for binary encoding, default is 0.001.\n    :type eps: float or float list (with the same length with ranges)\n    '
    ranges = SolutionRanges()
    eps = DecretePrecision()
    precisions = DecretePrecision()

    def __init__(self, ranges, eps):
        self.ranges = ranges
        self.eps = eps
        self.precisions = eps
        self.solution, self.chromsome = [], []

    def init(self, chromsome=None, solution=None):
        """ Initialize the individual by providing chromsome or solution.

        :param chromsome: chromesome sequence for the individual
        :type chromsome: list of (float / int)

        :param solution: the variable vector of the target function.
        :type solution: list of float

        .. Note::
            If both chromsome and solution are provided, only the chromsome would
            be used. If neither is provided, individual would be initialized randomly.
        """
        if not any([chromsome, solution]):
            self.solution = self._rand_solution()
            self.chromsome = self.encode()
        else:
            if chromsome:
                self.chromsome = chromsome
                self.solution = self.decode()
            else:
                self.solution = solution
                self.chromsome = self.encode()
        return self

    def clone(self):
        """ Clone a new individual from current one.
        """
        indv = self.__class__((deepcopy(self.ranges)), eps=(deepcopy(self.eps)))
        indv.init(chromsome=(deepcopy(self.chromsome)))
        return indv

    def encode(self):
        """ **NEED IMPLIMENTATION**

        Convert solution to chromsome sequence.

        :return: The chromsome sequence
        :rtype: list of float
        """
        raise NotImplementedError

    def decode(self):
        """ **NEED IMPLIMENTATION**

        Convert chromsome sequence to solution.

        :return: The solution vector
        :rtype: list of float
        """
        raise NotImplementedError

    def _rand_solution(self):
        """ Initialize individual solution randomly.
        """
        solution = []
        for eps, (a, b) in zip(self.precisions, self.ranges):
            n_intervals = (b - a) // eps
            n = int(uniform(0, n_intervals + 1))
            solution.append(a + n * eps)

        return solution