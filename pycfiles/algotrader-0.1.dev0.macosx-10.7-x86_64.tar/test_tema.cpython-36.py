# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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