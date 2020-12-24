# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/test_sma.py
# Compiled at: 2018-12-16 02:38:16
# Size of source mod 2**32: 788 bytes
import pandas as pd, sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.sma_agent import SMA_Agent
from algotrading.evaluation import Evaluation

def test(year, stock, window, up, down, get_plots=True, verbose=True):
    filename = '../Historical Data/%s/%s-%s.csv' % (year, stock, year)
    prices = pd.read_csv(filename)['Close']
    dates = pd.read_csv(filename)['Date']
    agent = SMA_Agent(window, up, down)
    test = Backtest(agent, 10000)
    output = test.run(prices)
    evaluator = Evaluation(prices, dates, output, 'SMA', stock)
    return evaluator.complete_evaluation(get_plots, verbose)


if __name__ == '__main__':
    test(sys.argv[1], sys.argv[2])