# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/momentum_agent.py
# Compiled at: 2018-12-15 07:59:20
# Size of source mod 2**32: 4460 bytes
from .BaseAgent import BaseAgent
import pandas as pd, numpy as np
from time import time
from itertools import islice
from collections import deque

class Momentum_Agent(BaseAgent):

    def __init__(self, window_size, small_sma=20, large_sma=150, stoch_osc_days=14, stoch_osc_oversold=20, stoch_osc_overbought=80, small_ema=12, large_ema=26, signal_ema=9):
        super().__init__(window_size)
        self.window_size = window_size
        self.small_sma = small_sma
        self.large_sma = large_sma
        self.stoch_osc_days = stoch_osc_days
        self.stoch_osc_oversold = stoch_osc_oversold
        self.stoch_osc_overbought = stoch_osc_overbought
        self.small_ema = small_ema
        self.large_ema = large_ema
        self.signal_ema = signal_ema
        self.running_ema_small = 0
        self.running_ema_large = 0
        self.running_ema_signal = 0
        self.multiplier_small = 2 / (small_ema + 1)
        self.multiplier_large = 2 / (large_ema + 1)
        self.multiplier_signal = 2 / (signal_ema + 1)
        self.macd_memory = deque(maxlen=(self.signal_ema))

    def get_sma(self, window):
        memory_slice = list(islice(self.memory, self.window_size - window, self.window_size))
        return np.mean(memory_slice)

    def get_stoch_osc(self, days):
        memory_slice = list(islice(self.memory, self.window_size - days, self.window_size))
        min_price = np.min(memory_slice)
        max_price = np.max(memory_slice)
        curr_price = memory_slice[(-1)]
        return (curr_price - min_price) * 100 / (max_price - min_price)

    def get_macd_hist(self, small, large, signal, price):
        memory_slice = list(islice(self.memory, self.window_size - large, self.window_size))
        memory_slice = pd.DataFrame(memory_slice)
        df_memory = pd.DataFrame(memory_slice)
        df_macd = df_memory.ewm(span=small, adjust=False).mean() - df_memory.ewm(span=large, adjust=False).mean()
        df_macd_hist = df_macd - df_macd.ewm(span=signal, adjust=False).mean()
        return df_macd_hist[0][(large - 1)]

    def step(self, price):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0
        else:
            trading_bias = self.get_sma(self.small_sma) - self.get_sma(self.large_sma)
            stoch_osc = self.get_stoch_osc(self.stoch_osc_days)
            macd_hist = self.get_macd_hist(self.small_ema, self.large_ema, self.signal_ema, price)
            if trading_bias > 0:
                if stoch_osc < 20:
                    if macd_hist > 0:
                        return 1
            if trading_bias < 0:
                if stoch_osc > 80:
                    if macd_hist < 0:
                        return -1
            return 0