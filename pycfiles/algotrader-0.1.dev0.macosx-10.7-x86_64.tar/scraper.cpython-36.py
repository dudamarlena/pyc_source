# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/algotrader/scraper.py
# Compiled at: 2018-12-15 00:27:14
# Size of source mod 2**32: 641 bytes
import pandas as pd, sys
sys.path.append('../')
import numpy as np, os, quandl

def getNifty():
    nifty_list = pd.read_csv('../Historical data/Nifty50list.csv')
    quandl.ApiConfig.api_key = 'FDEDsMbK1E2t_PMf7X3M'
    for stock in nifty_list['Symbol']:
        try:
            print(stock)
            for i in range(2000, 2018):
                print(i)
                df = quandl.get(('NSE/' + stock), start_date=(str(i) + '-01-01'), end_date=(str(i) + '-12-31'))
                if len(df) > 0:
                    df.to_csv('../Historical data/%s/%s-%s.csv' % (i, stock, i))

        except:
            print('An exception occurred while retrieving %s' % stock)