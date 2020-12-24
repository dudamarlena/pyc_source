# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\test\test_tsp.py
# Compiled at: 2018-01-29 05:36:29
# Size of source mod 2**32: 2276 bytes
import unittest
from strategycontainer.tsp.loaders import USEquityPricingLoader
from strategycontainer.tsp import SimplePipelineEngine
from strategycontainer.tsp.data import USEquityPricing
from strategycontainer.tsp import TSP
from strategycontainer.utils.calendar import Calendar
import pandas as pd
from strategycontainer.tsp.factors.factor import CustomFactor
from strategycontainer.utils.universe import Universe

class Returns(CustomFactor):
    inputs = [
     USEquityPricing.close, USEquityPricing.adj_close]
    window_safe = True

    def compute(self, today, assets, out, close, adj_close):
        out[:] = (close[(-1)] - close[0]) / close[0]


sma_10 = Returns(window_length=5)

class MyFactor(CustomFactor):
    inputs = [
     sma_10]
    window_length = 6
    window_safe = True

    def compute(self, today, assets, out, sma_10):
        out[:] = sma_10[(-1)] - sma_10[0]


myfactor1 = MyFactor()

class MyFactor2(CustomFactor):
    inputs = [
     myfactor1]
    window_length = 4

    def compute(self, today, assets, out, sma_10):
        out[:] = sma_10[(-1)] - sma_10[0]


myfactor2 = MyFactor2()

class TSPTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTSP(self):
        cal = Calendar('20161221', '20170201')
        pipeline_loader = USEquityPricingLoader()

        def choose_loader(column):
            if column in USEquityPricing.columns:
                return pipeline_loader
            raise ValueError('No PipelineLoader registered for column %s.' % column)

        cols = {}
        cols['myfactor2'] = myfactor2
        pipe = TSP(Universe.etf_100, cols)
        engine = SimplePipelineEngine(choose_loader, cal, None)
        df = engine.run_pipeline(pipe, pd.Timestamp('2017-01-18'), pd.Timestamp('2017-01-18'))
        print(df)
        df = engine.run_pipeline(pipe, pd.Timestamp('2017-01-19'), pd.Timestamp('2017-01-20'))
        print(df)


if __name__ == '__main__':
    unittest.main()