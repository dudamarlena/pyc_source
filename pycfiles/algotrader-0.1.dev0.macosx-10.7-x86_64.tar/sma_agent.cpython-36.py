# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/sma_agent.py
# Compiled at: 2018-12-15 07:58:29
# Size of source mod 2**32: 636 bytes
from .BaseAgent import BaseAgent
import pandas as pd, numpy as np
from time import time

class SMA_Agent(BaseAgent):

    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.up = up
        self.down = down
        self.window_size = window_size

    def step(self, price):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0
        if price <= np.mean(self.memory) * (1 - self.down):
            return 1
        else:
            if price >= np.mean(self.memory) * (1 + self.up):
                return -1
            return 0