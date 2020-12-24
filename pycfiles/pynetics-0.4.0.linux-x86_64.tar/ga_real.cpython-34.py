# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/ga_real.py
# Compiled at: 2016-04-14 05:05:14
# Size of source mod 2**32: 5096 bytes
import random
from pynetics.ga_list import Alleles, ListRecombination

class RealIntervalAlleles(Alleles):
    __doc__ = ' The possible alleles are real numbers belonging to an interval. '

    def __init__(self, a, b):
        """ Initializes the alleles with the interval of all their valid values

        It doesn't matters the order of the parameters. The interval will be all
        the real numbers between the lower and the upper values.

        :param a: One end of the interval.
        :param b: Other end of the interval.
        """
        self.a = min(a, b)
        self.b = max(a, b)

    def get(self):
        """ A random value is selected uniformly over the interval. """
        return random.uniform(self.a, self.b)


class PlainRecombination(ListRecombination):

    def __call__(self, parent1, parent2):
        """ Realizes the crossover operation.

        :param parent1: One of the individuals from which generate the progeny.
        :param parent2: The other.
        :return: A list of two individuals, each one a child containing some
            characteristics derived from the parents.
        """
        child1, child2 = super().__call__(parent1, parent2)
        for g in range(len(parent1)):
            lower_bound = min(parent1[g], parent2[g])
            upper_bound = max(parent1[g], parent2[g])
            child1[g] = random.uniform(lower_bound, upper_bound)
            child2[g] = upper_bound - (child1[g] - lower_bound)

        return (
         child1, child2)


class FlexibleRecombination(ListRecombination):

    def __init__(self, α):
        self.α = α

    def __call__(self, parent1, parent2):
        """ Realizes the crossover operation.

        :param parent1: One of the individuals from which generate the progeny.
        :param parent2: The other.
        :return: A list of two individuals, each one a child containing some
            characteristics derived from the parents.
        """
        child1, child2 = super().__call__(parent1, parent2)
        for g in range(len(parent1)):
            lower_bound = min(parent1[g], parent2[g]) - self.α
            upper_bound = max(parent1[g], parent2[g]) + self.α
            child1[g] = random.uniform(lower_bound, upper_bound)
            child2[g] = upper_bound - (child1[g] - lower_bound)

        return (
         child1, child2)


class MorphologicalRecombination(ListRecombination):
    __doc__ = 'Crossover that changes its behaviour depending on population diversity.\n\n    The idea is that, for each dimension of the vector (the chromosome of the\n    list individual) the algorithm first see how diverse is this dimension in\n    the population, that is, how big is the maximum difference between values\n    of different individuals in the same dimension. If the difference is to big,\n    the algorithm will choose the value of the children from a smaller interval\n    whereas if the diversity is to low, the algorithm will increase the interval\n    to increase the diversity.\n\n    NOTE: Works only for individuals with list chromosomes of real interval\n    alleles.\n    NOTE: The value of each gene must be normalized to the interval [0, 1].\n    '

    def __init__(self, a=-0.001, b=-0.133, c=0.54, d=0.226):
        """ Initializes this crossover method.

        The parameters a, b, c, d are the stated on paper: [INSERT HERE THE
        REFERENCE]

        :param a: One of the parameters.
        :param b: Other parameter.
        :param c: Yes, other parameter.
        :param d: Ok, the last parameter is this.
        """
        self._MorphologicalRecombination__a = a
        self._MorphologicalRecombination__b = b
        self._MorphologicalRecombination__c = c
        self._MorphologicalRecombination__d = d
        self._MorphologicalRecombination__calc_1 = (b - a) / c
        self._MorphologicalRecombination__calc_2 = d / (1 - c)
        self._MorphologicalRecombination__calc_3 = self._MorphologicalRecombination__calc_2 * -c

    def __call__(self, parent1, parent2):
        """ Realizes the crossover operation.

        :param parent1: One of the individuals from which generate the progeny.
        :param parent2: The other.
        :return: A list of two individuals, each one a child containing some
            characteristics derived from the parents.
        """
        child1, child2 = super().__call__(parent1, parent2)
        for g in range(len(parent1)):
            genes_in_position_g = [i[g] for i in parent1.population]
            diversity = max(genes_in_position_g) - min(genes_in_position_g)
            phi = self._MorphologicalRecombination__phi(diversity)
            lower_bound = min(parent1[g], parent2[g]) + phi
            upper_bound = max(parent1[g], parent2[g]) - phi
            child1[g] = random.uniform(lower_bound, upper_bound)
            child2[g] = upper_bound - (child1[g] - lower_bound)

        return (
         child1, child2)

    def __phi(self, x):
        """ Value in the interval from where to obtain the values grow or shrink

        :param x: The value of the diversity
        :return:
        """
        if x <= self._MorphologicalRecombination__c:
            return self._MorphologicalRecombination__calc_1 * x + self._MorphologicalRecombination__a
        else:
            return self._MorphologicalRecombination__calc_2 * x + self._MorphologicalRecombination__calc_3