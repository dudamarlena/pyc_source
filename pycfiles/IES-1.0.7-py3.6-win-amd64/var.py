# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\var.py
# Compiled at: 2018-12-18 04:04:33
# Size of source mod 2**32: 4626 bytes
"""
Created on 2017年7月29日

@author: sharon
"""
import os, pytz, datetime, time
from strategycontainer.utils.cache import ExpiringCache
from strategycontainer.utils.pandas_utils import clear_dataframe_indexer_caches
import pandas as pd
from strategycontainer.model import Equity

class Var(object):

    def __init__(self):
        self.PIPA_HOST = 'http://trading-server:10004'
        self.HTTP_HEADERS = None
        self.IES_DEBUG = False
        self._TIMEZONE = pytz.timezone('US/Eastern')
        self._FRAMEWORK_RUNNING_TYPE = os.environ.get('RUNNING_TYPE', 'datafetcher')
        self._FRAMEWORK_PORTFOLIOID = os.environ.get('PORTFOLIOID', -1)
        self._FRAMEWORK_DEBUGSERVER = os.environ.get('DEBUGSERVER', '127.0.0.1')
        self._FRAMEWORK_TRACEPORT = int(os.environ.get('TRACEPORT', '8001'))
        self._FRAMEWORK_RUNNING_NOTEBOOK = False
        self._FRAMEWORK_IS_BACKTEST = self._FRAMEWORK_RUNNING_TYPE == 'backtest'
        self._FRAMEWORK_IS_LIVETRADE = self._FRAMEWORK_RUNNING_TYPE == 'livetrade'
        self._FRAMEWORK_IS_DATAFETCHER = self._FRAMEWORK_RUNNING_TYPE == 'datafetcher'
        self._FRAMEWORK_BT_CURRENTTIME = None
        self._FRAMEWORK_BT_LASTTRADEDAY = datetime.datetime(1990, 1, 1)
        self._FRAMEWORK_BT_STARTDATE = '19800101'
        self._FRAMEWORK_BT_ENDDATE = '19800101'
        self._FRAMEWORK_REMOTEDEBUG = False
        self._FRAMEWORK_IS_TEST_STRATEGY = True
        self._FRAMEWORK_IS_TRAIN_TEST_STRATEGY = False
        self._FRAMEWORK_TRAIN_STARTDATE = '19800101'
        self._FRAMEWORK_TRAIN_ENDDATE = '19800101'
        self._FRAMEWORK_CURRENT_PHASE = 'train' if self._FRAMEWORK_IS_TRAIN_TEST_STRATEGY else 'test'
        self._FRAMEWORK_MARKETTYPE = 'US'
        self._FRAMEWORK_EXCEPTIONHANDLE = 'CONTINUE'
        self._framework_everyday_funcs = {}
        self._framework_monthstart_funcs = {}
        self._framework_monthend_funcs = {}
        self._framework_weekstart_funcs = {}
        self._framework_weekend_funcs = {}
        self.this_month_tradedays = None
        self.this_month_halfdays = None
        self.this_monthstart_funcs = {}
        self.this_monthend_funcs = {}
        self.this_weekstart_funcs = {}
        self.this_weekend_funcs = {}
        self.today_minute_funcs = {}
        self.context = None
        self.data = None
        self.log = None
        self.strategyModule = None
        self.cal = None
        self.ips_api = None
        self.api = None
        self.dataCache = ExpiringCache(cleanup=clear_dataframe_indexer_caches)
        self.call_start_mills = int(round(time.time() * 1000))
        self.call_count = 0
        self.max_call_per_sec = 50

    def retrieveAllStocks(self):
        today = pd.Timestamp(self._FRAMEWORK_BT_CURRENTTIME.strftime('%Y-%m-%d'))
        try:
            allStocks = self.dataCache.get('allStocks', today)
        except KeyError:
            allStocks = self.ips_api._framework_getAllStocks()
            allStocks['start_date'] = allStocks['start_date'].astype('str')
            allStocks['end_date'] = allStocks['end_date'].astype('str')
            allStocks['asset'] = allStocks[['sid', 'symbol', 'start_date', 'end_date', 'sec_type']].apply((lambda x: Equity((x[0]), (x[1].upper()), start_date=(x[2]), end_date=(x[3]), sec_type=(x[4]))), axis=1)
            allStocks.set_index('sid', inplace=True)
            if self._FRAMEWORK_IS_BACKTEST:
                end_session = pd.Timestamp(self._FRAMEWORK_BT_ENDDATE)
            if self._FRAMEWORK_IS_LIVETRADE:
                end_session = today
            self.dataCache.set('allStocks', allStocks, end_session)

        return allStocks

    def wait_if_call_too_fast(self):
        t = int(round(time.time() * 1000))
        delta_t = t - self.call_start_mills
        if delta_t > 1000:
            self.call_start_mills = t
            self.call_count = 0
        self.call_count = self.call_count + 1
        if self.call_count > self.max_call_per_sec:
            print('api call frequency is too fast')
            if 1000 - delta_t > 0:
                time.sleep((1000 - delta_t) / 1000)


if __name__ == '__main__':
    pass