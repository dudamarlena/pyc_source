# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\slippage.py
# Compiled at: 2017-07-28 22:03:39
# Size of source mod 2**32: 562 bytes
"""
@author: sharon
"""
DEFAULT_VOLUME_SLIPPAGE_BAR_LIMIT = 0.025

class SlippageModel:

    def __init__(self):
        self._volume_for_bar = 0


class VolumeShareSlippage(SlippageModel):

    def __init__(self, volume_limit=DEFAULT_VOLUME_SLIPPAGE_BAR_LIMIT, price_impact=0.1):
        self.volume_limit = volume_limit
        self.price_impact = price_impact
        super(VolumeShareSlippage, self).__init__()


class FixedSlippage(SlippageModel):

    def __init__(self, spread=0.0):
        self.spread = spread