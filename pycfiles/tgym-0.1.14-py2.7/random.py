# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tgym/gens/random.py
# Compiled at: 2017-06-13 15:07:39
import numpy as np
from tgym.core import DataGenerator

class RandomWalk(DataGenerator):
    """Random walk data generator for one product
    """

    @staticmethod
    def _generator(ba_spread=0):
        """Generator for a pure random walk

        Args:
            ba_spread (float): spread between bid/ask

        Yields:
            (tuple): bid ask prices
        """
        val = 0
        while True:
            yield (
             val, val + ba_spread)
            val += np.random.standard_normal()


class AR1(DataGenerator):
    """Standardised AR1 data generator
    """

    @staticmethod
    def _generator(a, ba_spread=0):
        """Generator for standardised AR1

        Args:
            a (float): AR1 coefficient
            ba_spread (float): spread between bid/ask

        Yields:
            (tuple): bid ask prices
        """
        assert abs(a) < 1
        sigma = np.sqrt(1 - a ** 2)
        val = np.random.normal(scale=sigma)
        while True:
            yield (
             val, val + ba_spread)
            val += (a - 1) * val + np.random.normal(scale=sigma)