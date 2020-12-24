# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/test_momentum.py
# Compiled at: 2018-12-16 05:25:10
# Size of source mod 2**32: 1176 bytes
import pandas as pd, sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.momentum_agent import Momentum_Agent
from algotrading.evaluation import Evaluation

def test(year, stock, window=150, up=0.05, down=0.05):
    filename = '../Historical Data/%s/%s-%s.csv' % (year, stock, year)
    prices = pd.read_csv(filename)['Close']
    dates = pd.read_csv(filename)['Date']
    agent = Momentum_Agent(150, 20, 150, 14, 20, 80, 12, 26, 9)
    test = Backtest(agent, 10000)
    output = test.run(prices)
    evaluator = Evaluation(prices, dates, output, 'Moving Momentum', stock)
    return evaluator.complete_evaluation()


if __name__ == '__main__':
    test(sys.argv[1], sys.argv[2])