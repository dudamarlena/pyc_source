# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/six_month_cycle_agent.py
# Compiled at: 2018-12-15 07:58:38
# Size of source mod 2**32: 1591 bytes
from .BaseAgent import BaseAgent
import pandas as pd, numpy as np
from itertools import islice

class SixMonthCycle_Agent(BaseAgent):

    def __init__(self, window_size, small, large, signal, up, down):
        super().__init__(window_size)
        self.up = up
        self.down = down
        self.large = large
        self.small = small
        self.signal = signal
        self.window_size = window_size

    def get_macd_signal(self):
        memory_slice = list(islice(self.memory, self.window_size - self.large, self.window_size))
        memory_slice = pd.DataFrame(memory_slice)
        df_memory = pd.DataFrame(memory_slice)
        df_macd = df_memory.ewm(span=(self.small), adjust=False).mean() - df_memory.ewm(span=(self.large), adjust=False).mean()
        signal = df_macd.ewm(span=(self.signal), adjust=False).mean()[0][(self.large - 1)]
        macd = df_macd[0][(self.large - 1)]
        if macd >= (1 + self.up) * signal:
            return 'buy'
        else:
            if macd <= (1 - self.down) * signal:
                return 'sell'
            return 'hold'

    def step(self, price, date):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0
        date = list(map(int, date.split('-')))
        month = date[1]
        macd_signal = self.get_macd_signal()
        if month > 10 or month < 5 and macd_signal == 'buy':
            return 1
        else:
            if month > 4:
                if month < 11:
                    if macd_signal == 'sell':
                        return -1
            return 0