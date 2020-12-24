# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/agents/BaseAgent.py
# Compiled at: 2018-12-15 07:57:13
# Size of source mod 2**32: 320 bytes
from collections import deque

class BaseAgent:

    def __init__(self, window_size):
        self.memory = deque(maxlen=window_size)

    def deep_reset(self, stock_price, ticker):
        self.ticker = ticker
        self.memory = deque(maxlen=1000)

    def reset_memory(self):
        self.memory = deque(maxlen=1000)