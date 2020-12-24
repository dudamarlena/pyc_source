# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/replacements.py
# Compiled at: 2016-03-12 06:54:43
# Size of source mod 2**32: 1678 bytes
from pynetics import Replacement

class LowElitism(Replacement):
    """LowElitism"""

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
    """HighElitism"""

    def __call__(self, population, indviduals):
        """ Inserts the offspring in the population and removes the less fit.

        :param population: The population where make the replacement.
        :param indviduals: The new population to use as replacement.
        """
        if indviduals:
            population.sort()
            population.extend(indviduals)
            del population[-len(indviduals):]