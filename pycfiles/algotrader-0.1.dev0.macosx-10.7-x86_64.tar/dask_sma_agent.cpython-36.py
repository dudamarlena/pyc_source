# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/dask-agents/dask_sma_agent.py
# Compiled at: 2018-12-14 08:23:19
# Size of source mod 2**32: 1539 bytes
from .BaseDaskAgent import BaseDaskAgent
import numpy as np
from time import time
import pandas as pd

class SMA_Agent(BaseDaskAgent):

    def __init__(self, cash, window_size, up, down):
        super().__init__(cash, window_size)
        self.up = up
        self.down = down
        self.window_size = window_size
        self.memory = Null
        self.moving_avg = 0

    def step(self, row):
        row = np.array(row)
        if self.memory is Null:
            self.memory = pd.read_csv('dummy.csv')
        if len(self.memory) < self.window_size:
            self.memory.append(row)
            return 0
        self.memory['SMA'] = 0
        self.moving_avg = self.memory.loc[len(self.memory) - self.window_size:len(self.memory)]['Close'].mean()
        if row[5] <= np.mean(self.memory) * (1 - self.down) and self.cash > price:
            self.stock += self.cash // price
            self.cash -= self.cash // price * price
            self.memory.append((row, self.moving_avg))
            return 1
        else:
            if row[5] >= np.mean(self.memory) * (1 + self.up):
                if self.stock > 0:
                    self.cash += self.stock * price
                    self.stock = 0
                    self.memory.append((row, self.moving_avg))
                    return -1
            self.memory.append((row, self.moving_avg))
            return 0