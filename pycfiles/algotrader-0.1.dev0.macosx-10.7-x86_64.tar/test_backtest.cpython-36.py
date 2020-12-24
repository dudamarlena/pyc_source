# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/test_backtest.py
# Compiled at: 2018-12-12 11:46:55
# Size of source mod 2**32: 728 bytes
import pandas as pd, sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.sma_agent import SMA_Agent
import matplotlib.pyplot as plt, numpy as np, os
stocks = os.listdir('../Historical data/')
for stock in stocks[1:7]:
    prices = pd.read_csv('../Historical data/' + stock)['Price']
    agent = SMA_Agent(10000, 10, 0.015, 0.015)
    test = Backtest(agent)
    output = test.run(prices)
    fig, ax = plt.subplots()
    ax.plot((np.arange(len(prices))), output, color='red')
    ax.plot((np.arange(len(prices))), prices, color='green')
    ax.set(xlabel='Days', ylabel='INR', title=stock)
    ax.grid()
    plt.show()