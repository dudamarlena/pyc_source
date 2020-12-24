# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tgym/gens/deterministic.py
# Compiled at: 2017-06-13 15:07:39
import numpy as np
from tgym.core import DataGenerator

class WavySignal(DataGenerator):
    """Modulated sine generator
    """

    @staticmethod
    def _generator(period_1, period_2, epsilon, ba_spread=0):
        i = 0
        while True:
            i += 1
            bid_price = (1 - epsilon) * np.sin(2 * i * np.pi / period_1) + epsilon * np.sin(2 * i * np.pi / period_2)
            yield (bid_price, bid_price + ba_spread)