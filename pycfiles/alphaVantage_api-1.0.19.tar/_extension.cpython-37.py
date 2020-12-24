# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\appli\Documents\GitHub\alphaVantageAPI Project\alphaVantageAPI\_extension.py
# Compiled at: 2020-04-19 18:58:55
# Size of source mod 2**32: 6525 bytes
import time, math, re, numpy as np, pandas as pd
from os import getenv as os_getenv
from ._base_pandas_object import *
from alphaVantageAPI.alphavantage import AlphaVantage
_AV_ = AlphaVantage(api_key=None, clean=True)

@pd.api.extensions.register_dataframe_accessor('av')
class AlphaVantageDownloader(BasePandasObject):

    def __call__(self, q=None, output_size='compact', timed=False, *args, **kwargs):
        try:
            try:
                if isinstance(q, str):
                    q = q.lower()
                    fn = getattr(self, q)
                    if timed:
                        stime = time.time()
                    query = fn(**kwargs)
                    if timed:
                        time_diff = time.time() - stime
                        ms = time_diff * 1000
                        query.timed = f"{ms:2.3f} ms ({time_diff:2.3f} s)"
                    return query
                (self.help)(args, keyword=kwargs.pop('help', None), **kwargs)
            except:
                (self.help)(args, keyword=kwargs.pop('help', None), **kwargs)

        finally:
            self._df = None

    def help(self, keyword=None, **kwargs):
        """Simple Help Screen"""
        _AV_.help(keyword)

    def global_quote(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.global_quote)(symbol, **kwargs)
        return self._df

    def search(self, keywords: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.search)(keywords, **kwargs)
        return self._df

    def sectors(self, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.sectors)(**kwargs)
        return self._df

    def daily(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.data)(function='D', symbol=symbol, **kwargs)
        return self._df

    def daily_adjusted(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.data)(function='DA', symbol=symbol, **kwargs)
        return self._df

    def intraday(self, symbol: str, interval=5, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.intraday)(symbol, interval=interval, **kwargs)
        return self._df

    def monthly(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.data)(function='M', symbol=symbol, **kwargs)
        return self._df

    def monthly_adjusted(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.data)(function='MA', symbol=symbol, **kwargs)
        return self._df

    def weekly(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.data)(function='W', symbol=symbol, **kwargs)
        return self._df

    def weekly_adjusted(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.data)(function='WA', symbol=symbol, **kwargs)
        return self._df

    def digital_daily(self, symbol: str, market: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.digital)(symbol, market=market, function='CD', **kwargs)
        return self._df

    def crypto_rating(self, symbol: str, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.crypto_rating)(symbol, function='CR', **kwargs)
        return self._df

    def digital_monthly(self, symbol: str, market: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.digital)(symbol, market=market, function='CM', **kwargs)
        return self._df

    def digital_weekly(self, symbol: str, market: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.digital)(symbol, market=market, function='CW', **kwargs)
        return self._df

    def fx(self, from_currency: str, to_currency: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.fxrate)(from_currency=from_currency, to_currency=to_currency, **kwargs)
        return self._df

    def fx_daily(self, from_symbol: str, to_symbol: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.fx)('FXD', from_symbol=from_symbol, to_symbol=to_symbol, **kwargs)
        return self._df

    def fx_intraday(self, from_symbol: str, to_symbol: str='USD', interval=5, **kwargs) -> pd.DataFrame:
        self._df = (_AV_.fx)('FXI', from_symbol=from_symbol, to_symbol=to_symbol, interval=interval, **kwargs)
        return self._df

    def fx_monthly(self, from_symbol: str, to_symbol: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.fx)('FXM', from_symbol=from_symbol, to_symbol=to_symbol, **kwargs)
        return self._df

    def fx_weekly(self, from_symbol: str, to_symbol: str='USD', **kwargs) -> pd.DataFrame:
        self._df = (_AV_.fx)('FXW', from_symbol=from_symbol, to_symbol=to_symbol, **kwargs)
        return self._df

    CR = crypto_rating
    GQ = global_quote
    S = sectors
    D = daily
    DA = daily_adjusted
    I = intraday
    M = monthly
    MA = monthly_adjusted
    W = weekly
    WA = weekly_adjusted
    CD = digital_daily
    CM = digital_monthly
    CW = digital_weekly
    FX = fx
    FXD = fx_daily
    FXI = fx_intraday
    FXM = fx_monthly
    FXW = fx_weekly

    @property
    def clean(self) -> bool:
        return _AV_.clean

    @clean.setter
    def clean(self, value: str) -> None:
        _AV_.clean = value

    @property
    def export(self) -> bool:
        return _AV_.export

    @export.setter
    def export(self, value: str) -> None:
        _AV_.export = value

    @property
    def output(self) -> str:
        return _AV_.output

    @output.setter
    def output(self, value: str) -> None:
        _AV_.output = value

    @property
    def output_size(self) -> str:
        return _AV_.output_size

    @output_size.setter
    def output_size(self, value: str) -> None:
        _AV_.output_size = value

    @property
    def premium(self) -> bool:
        return _AV_.premium

    @premium.setter
    def premium(self, value: str) -> None:
        _AV_.premium = value

    @property
    def proxy(self) -> dict:
        return _AV_.proxy

    @proxy.setter
    def proxy(self, value: str) -> None:
        _AV_.proxy = value