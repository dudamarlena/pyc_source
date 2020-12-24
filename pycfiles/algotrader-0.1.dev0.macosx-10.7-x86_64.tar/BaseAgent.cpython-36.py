# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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