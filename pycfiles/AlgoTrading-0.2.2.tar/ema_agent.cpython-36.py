# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/ema_agent.py
# Compiled at: 2018-12-15 07:59:29
# Size of source mod 2**32: 903 bytes
from .BaseAgent import BaseAgent
import pandas as pd, numpy as np
from time import time

class EMA_Agent(BaseAgent):

    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.window_size = window_size
        self.multiplier = 2 / (window_size + 1)
        self.running_ema = 0
        self.up = up
        self.down = down

    def step(self, price):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0
        else:
            if self.running_ema == 0:
                self.running_ema = np.mean(self.memory)
            else:
                self.running_ema = (price - self.running_ema) * self.multiplier + self.running_ema
        if price >= self.running_ema * (1 - self.down):
            return 1
        else:
            if price <= self.running_ema * (1 + self.up):
                return -1
            return 0