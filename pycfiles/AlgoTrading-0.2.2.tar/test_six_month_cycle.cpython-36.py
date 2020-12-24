# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/test_six_month_cycle.py
# Compiled at: 2018-12-16 05:25:10
# Size of source mod 2**32: 957 bytes
import pandas as pd, sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.six_month_cycle_agent import SixMonthCycle_Agent
from algotrading.evaluation import Evaluation

def test(year, stock, window=10, up=0.05, down=0.05):
    filename = '../Historical Data/%s/%s-%s.csv' % (year, stock, year)
    prices = pd.read_csv(filename)['Close']
    dates = pd.read_csv(filename)['Date']
    agent = SixMonthCycle_Agent(26, 12, 26, 9, 0.015, 0.015)
    test = Backtest(agent, 10000)
    output = test.run(prices, dates)
    evaluator = Evaluation(prices, dates, output, 'Six Month Cycle MACD', stock)
    return evaluator.complete_evaluation()


if __name__ == '__main__':
    test(sys.argv[1], sys.argv[2])