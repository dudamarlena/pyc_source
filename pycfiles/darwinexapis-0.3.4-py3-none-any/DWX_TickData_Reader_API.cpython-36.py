# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eriz/Desktop/darwinexapis/darwinexapis/API/TickDataAPI/DWX_TickData_Reader_API.py
# Compiled at: 2020-05-13 05:35:38
# Size of source mod 2**32: 5294 bytes
"""
    Sample code:
    DWX_TickData_Reader_API.py
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
from pathlib import Path
import pandas as pd, numpy as np, gzip, os, matplotlib.pyplot as plt, logging
logger = logging.getLogger()
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class DWX_TickData_Reader_API:
    __doc__ = 'This class will read the bid and ask files on a directory and create\n    a dataframe with both price sequences (i.e. time series).'

    def __init__(self, _bids_file='<INSERT_PATH>', _asks_file='<INSERT_PATH>'):
        self._file_name_csv = _bids_file.split('/')[(-1)].replace('BID', 'BID_ASK').replace('pkl', 'csv')
        self._asset_name = _bids_file.split('/')[(-1)].split('_')[0]
        self._bid_price_col_name = f"{self._asset_name}_bid_price"
        self._ask_price_col_name = f"{self._asset_name}_ask_price"
        self._bid_size_col_name = f"{self._asset_name}_bid_size"
        self._ask_size_col_name = f"{self._asset_name}_ask_size"
        self._bids_file = _bids_file
        self._asks_file = _asks_file

    def _construct_data_(self, _filename):
        _df = pd.read_pickle(_filename)
        if 'BID' in _filename:
            _df.columns = [
             self._bid_price_col_name, self._bid_size_col_name]
        else:
            if 'ASK' in _filename:
                _df.columns = [
                 self._ask_price_col_name, self._ask_size_col_name]
        _df.index.name = f"{self._asset_name}_timestamp"
        return _df.apply(pd.to_numeric)

    def _get_symbol_as_dataframe_(self, _convert_epochs=True, _check_integrity=False, _calc_spread=False, _reindex=[], _precision='tick', _daily_start=22, _symbol_digits=5):
        """
        See http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
        for .resample() rule / frequency strings.        
        """
        _bids = self._construct_data_(self._bids_file)
        _asks = self._construct_data_(self._asks_file)
        _df = _asks.merge(_bids, how='outer', left_index=True, right_index=True, copy=False).fillna(method='ffill').dropna()
        if _calc_spread:
            _df[f"{self._asset_name}_spread"] = abs(np.diff(_df[[self._ask_price_col_name, self._bid_price_col_name]]))
        if _convert_epochs:
            _df.index = pd.to_datetime((_df.index), unit='ms')
        if len(_reindex) > 0:
            _df = _df.reindex(_reindex, axis=1)
        if _precision != 'tick':
            _df[f"{self._asset_name}_mid_price"] = round((_df[self._ask_price_col_name] + _df[self._bid_price_col_name]) / 2, _symbol_digits)
            if _precision not in ('B', 'C', 'D', 'W', '24H'):
                _df = _df[f"{self._asset_name}_mid_price"].resample(rule=_precision).ohlc()
            else:
                _df = _df[f"{self._asset_name}_mid_price"].resample(rule=_precision, base=_daily_start).ohlc().dropna()
        if _check_integrity:
            logger.warning('\n\n[INFO] Checking data integrity..')
            self._integrity_check_(_df)
        return _df

    def _save_df_to_csv(self, dataframe_to_save, which_path=None):
        if which_path:
            dataframe_to_save.to_csv(which_path + self._file_name_csv)
        else:
            dataframe_to_save.to_csv(self._file_name_csv)

    def _integrity_check_(self, _df):
        if isinstance(_df, pd.DataFrame) == False:
            logger.warning('[ERROR] Input must be a Pandas DataFrame')
        else:
            _diff = _df.index.to_series().diff()
            logger.warning('\n[TEST #1] Data Frequency Statistics\n--')
            logger.warning(_diff.describe())
            logger.warning('\n[TEST #2] Mode of Gap Distribution\n--')
            logger.warning(_diff.value_counts().head(1))
            logger.warning('\n[TEST #3] Hourly Spread Distribution\n--')
            _df.groupby(_df.index.hour)[f"{self._asset_name}_spread"].mean().plot(xticks=(range(0, 24)),
              title='Average Spread by Hour (UTC)')
            plt.show()