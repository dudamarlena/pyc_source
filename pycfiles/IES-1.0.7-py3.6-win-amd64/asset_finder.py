# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\asset_finder.py
# Compiled at: 2018-10-15 06:58:16
# Size of source mod 2**32: 923 bytes
import pandas as pd
from .numpy_utils import as_column

class AssetFinder(object):

    def __init__(self, universe, var):
        self.var = var
        allStocks = self.var.retrieveAllStocks()
        sids = [asset.sid for asset in universe]
        self.stocks = allStocks.loc[sids].sort_index(ascending=True)

    def lifetimes(self, dates, include_start_date):
        raw_dates = as_column(dates.strftime('%Y%m%d').astype(str))
        if include_start_date:
            mask = self.stocks.start_date.values <= raw_dates
        else:
            mask = self.stocks.start_date.values < raw_dates
        mask &= raw_dates <= self.stocks.end_date.values
        df = pd.DataFrame(mask, index=[pd.Timestamp(date) for date in dates], columns=(self.stocks.index.values))
        return df

    def retrieve_all(self, sids):
        return self.stocks.loc[sids.values].asset.values