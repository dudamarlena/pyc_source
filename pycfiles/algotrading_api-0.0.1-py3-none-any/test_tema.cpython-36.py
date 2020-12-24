# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/test_tema.py
# Compiled at: 2018-12-15 12:43:55
# Size of source mod 2**32: 805 bytes
import pandas as pd, sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.tema_agent import TEMA_Agent
from algotrading.evaluation import Evaluation

def test(year, stock, window=10, up=0.05, down=0.05, get_plots=True, verbose=True):
    filename = '../Historical Data/%s/%s-%s.csv' % (year, stock, year)
    prices = pd.read_csv(filename)['Close']
    dates = pd.read_csv(filename)['Date']
    agent = TEMA_Agent(window, up, down)
    test = Backtest(agent, 10000)
    output = test.run(prices)
    evaluator = Evaluation(prices, dates, output, 'TEMA', stock)
    return evaluator.complete_evaluation(get_plots, verbose)


if __name__ == '__main__':
    test(sys.argv[1], sys.argv[2])