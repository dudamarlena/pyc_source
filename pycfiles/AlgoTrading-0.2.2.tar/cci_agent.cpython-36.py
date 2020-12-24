# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/cci_agent.py
# Compiled at: 2018-12-15 08:02:00
# Size of source mod 2**32: 659 bytes
from .BaseAgent import BaseAgent
import pandas as pd, numpy as np
from time import time

class CCI_Agent(BaseAgent):

    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.up = up
        self.down = down
        self.window_size = window_size

    def step(self, price):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0
        CCI = (price - np.mean(self.memory)) / (0.015 * np.std(self.memory))
        if CCI > 100:
            return 1
        else:
            if CCI < -100:
                return -1
            return 0