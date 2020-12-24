# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/test_logging.py
# Compiled at: 2018-12-15 10:27:12
# Size of source mod 2**32: 700 bytes
import pandas as pd, sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.sma_agent import SMA_Agent
import matplotlib.pyplot as plt, numpy as np, os
prices = pd.read_csv('../Historical data/2017/CIPLA-2017.csv')['Open']
agent = SMA_Agent(10, 0.015, 0.015)
test = Backtest(agent, 10000, logging=True, ticker='CIPLA')
output = test.run(prices)
fig, ax = plt.subplots()
ax.plot((np.arange(len(prices))), output, color='red')
ax.plot((np.arange(len(prices))), prices, color='green')
ax.set(xlabel='Days', ylabel='INR', title='CIPLA')
ax.grid()
plt.show()
print(test.logstore.read('CIPLA').data)