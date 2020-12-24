# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/replacements.py
# Compiled at: 2016-03-12 06:54:43
# Size of source mod 2**32: 1678 bytes
from pynetics import Replacement

class LowElitism(Replacement):
    __doc__ = " Low elitism replacement.\n\n    The method will replace the less fit individuals by the ones specified in\n    the offspring. This makes this operator elitist, but at least not much.\n    Moreover, if offspring size equals to the population size then it's a full\n    replacement (i.e. a generational scheme).\n    "

    def __call__(self, population, individuals):
        """ Removes less fit individuals and then inserts the offspring.

        :param population: The population where make the replacement.
        :param individuals: The new population to use as replacement.
        """
        if individuals:
            population.sort()
            del population[-len(individuals):]
            population.extend(individuals)


class HighElitism(Replacement):
    __doc__ = ' Drops the less fit individuals among all (population plus offspring).\n\n    The method will add all the individuals in the offspring to the population,\n    removing afterwards those individuals less fit. This makes this operator\n    highly elitist but if length os population and offspring are the same, the\n    process will result in a full replacement, i.e. a generational scheme of\n    replacement.\n    '

    def __call__(self, population, indviduals):
        """ Inserts the offspring in the population and removes the less fit.

        :param population: The population where make the replacement.
        :param indviduals: The new population to use as replacement.
        """
        if indviduals:
            population.sort()
            population.extend(indviduals)
            del population[-len(indviduals):]