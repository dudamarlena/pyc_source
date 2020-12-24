# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/tema_agent.py
# Compiled at: 2018-12-15 07:58:21
# Size of source mod 2**32: 1996 bytes
from .BaseAgent import BaseAgent
import pandas as pd, numpy as np
from time import time
from collections import deque

class TEMA_Agent(BaseAgent):

    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.window_size = window_size
        self.multiplier = 2 / (window_size + 1)
        self.running_ema = 0
        self.up = up
        self.down = down
        self.running_dema_memory = deque(maxlen=window_size)
        self.running_dema = 0
        self.running_dema_memory.append(0)
        self.running_tema_memory = deque(maxlen=window_size)
        self.running_tema = 0
        self.running_tema_memory.append(0)

    def step(self, price):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0
        else:
            if self.running_ema == 0:
                self.running_ema = np.mean(self.memory)
            else:
                self.running_ema = (price - self.running_ema) * self.multiplier + self.running_ema
            if len(self.running_dema_memory) < self.window_size:
                self.running_dema = np.mean(self.running_dema_memory)
            else:
                self.running_dema = (self.running_ema - self.running_dema) * self.multiplier + self.running_dema
            if len(self.running_tema_memory) < self.window_size:
                self.running_tema = np.mean(self.running_tema_memory)
            else:
                self.running_tema = (self.running_dema - self.running_tema) * self.multiplier + self.running_tema
        TEMA = 3 * self.running_ema - 3 * self.running_dema + self.running_tema
        self.running_dema_memory.append(self.running_ema)
        self.running_tema_memory.append(self.running_dema)
        if price >= TEMA * (1 - self.down):
            return 1
        else:
            if price <= TEMA * (1 + self.up):
                return -1
            return 0