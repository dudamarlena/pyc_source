# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zmlaptop/Desktop/darwinexapis/darwinexapis/API/InfoAPI/DWX_Info_API.py
# Compiled at: 2020-05-09 05:36:27
# Size of source mod 2**32: 17723 bytes
"""
    DWX_Info_API.py - DARWIN Info API (Subclass of DWX_API)
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 07, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import os, time
from darwinexapis.MINIONS.dwx_graphics_helpers import DWX_Graphics_Helpers
from darwinexapis.API.dwx_api import DWX_API
import pandas as pd, numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 500)

class DWX_Info_API(DWX_API):

    def __init__(self, _auth_creds='', _api_url='https://api.darwinex.com', _api_name='darwininfo', _version=1.5, _demo=False):
        super(DWX_Info_API, self).__init__(_auth_creds, _api_url, _api_name, _version, _demo)
        self._graphics = DWX_Graphics_Helpers()

    def _Get_Historical_Quotes_(self, _symbols=[
 'THA.4.12', 'LVS.4.20'], _start='', _end='', _endpoint='/products/{}/history/quotes', _plot_title='DWX_Info_API: def _Get_Quotes_() Example', _plot=False, _delay=0.01):
        if isinstance(_symbols, list):
            _dict = {}
            _count = 1
            for darwin in _symbols:
                print(('\r[DarwinInfoAPI] Getting Quotes for DARWIN {} / {}: ${}'.format(_count, len(_symbols), darwin)), end='',
                  flush=True)
                try:
                    if _start not in ['', np.nan]:
                        _ep = _endpoint.format(darwin) + '?start={}&end={}'.format(int(_start.timestamp()) * 1000, int(_end.timestamp()) * 1000)
                    else:
                        _ep = _endpoint.format(darwin)
                    _dict[darwin] = pd.DataFrame(data=(self._Call_API_(_ep, 'GET', '')))
                    _dict[darwin].columns = [
                     'timestamp', darwin]
                    _dict[darwin].timestamp = pd.to_datetime((_dict[darwin].timestamp), unit='ms')
                    _dict[darwin] = _dict[darwin][(_dict[darwin].timestamp.dt.date < pd.to_datetime('today').date())]
                    _dict[darwin] = _dict[darwin].set_index('timestamp')
                    if _delay > 0:
                        time.sleep(_delay)
                except Exception as ex:
                    print('[ERROR] Something went wrong while looking up ${}'.format(darwin))
                    _exstr = 'Exception Type {0}. Args:\n{1!r}'
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    continue

                _count += 1

            _retdf = pd.concat([_df for _df in _dict.values() if isinstance(_df, pd.DataFrame)], axis=1)
            _retdf.columns = _symbols
            if _plot:
                self._graphics._plotly_dataframe_scatter_(_custom_filename='example_quotes.html', _dir_prefix='MISC/',
                  _df=_retdf,
                  _x_title='EOD Timestamp',
                  _y_title='DARWIN Quote',
                  _main_title=_plot_title)
            return _retdf
        print('[ERROR] Please specify symbols as Python list []')

    def _Get_Historical_Scores_(self, _symbols=[
 'THA.4.12', 'LVS.4.20'], _endpoint='/products/{}/history/badges', _plot_title='DWX_Info_API: def _Get_Historical_Scores_() Example', _plot=False, _delay=0.01):
        if isinstance(_symbols, list):
            _dict = {}
            _count = 1
            _badge_cols = [
             'eod_ts', 'Dp', 'Ex', 'Mc', 'Rs',
             'Ra', 'Os', 'Cs', 'Rp', 'Rm',
             'Dc', 'La', 'Pf', 'Cp', 'Ds',
             'fcal_ts', 'lcal_ts']
            for darwin in _symbols:
                print(('\r[DarwinInfoAPI] Getting Scores for DARWIN {} / {}: ${}'.format(_count, len(_symbols), darwin)), end='',
                  flush=True)
                try:
                    _dict[darwin] = self._Call_API_(_endpoint.format(darwin), 'GET', '')
                    _dict[darwin] = [_dict[darwin][i][:2] + [x for x in _dict[darwin][i][2]] + _dict[darwin][i][-2:] for i in range(len(_dict[darwin]))]
                    _dict[darwin] = pd.DataFrame(data=(_dict[darwin]), index=[_dict[darwin][i][0] for i in range(len(_dict[darwin]))])
                    _dict[darwin].columns = _badge_cols
                    _dict[darwin].eod_ts = pd.to_datetime((_dict[darwin].eod_ts), unit='ms')
                    _dict[darwin].fcal_ts = pd.to_datetime((_dict[darwin].fcal_ts), unit='ms')
                    _dict[darwin].lcal_ts = pd.to_datetime((_dict[darwin].lcal_ts), unit='ms')
                    _dict[darwin] = _dict[darwin].set_index('eod_ts')
                    if _delay > 0:
                        time.sleep(_delay)
                except Exception as ex:
                    print('[ERROR] Something went wrong while looking up ${}'.format(darwin))
                    _exstr = 'Exception Type {0}. Args:\n{1!r}'
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    continue

                _count += 1

            if len(_symbols) == 1:
                if _plot:
                    self._graphics._plotly_dataframe_scatter_(_custom_filename='example_scores.html', _dir_prefix='MISC/',
                      _df=(_dict[_symbols[0]].drop(['fcal_ts', 'lcal_ts', 'Ds', 'Dp'], axis=1).loc[:,]),
                      _x_title='EOD Timestamp',
                      _y_title='Score / Investment Attribute',
                      _main_title=_plot_title)
            return _dict
        print('[ERROR] Please specify symbols as Python list []')

    def _Get_DARWIN_Universe_(self, _status='ALL', _endpoint='/products{}', _query_string='?status={}&page={}&per_page={}', _page=0, _perPage=50, _iterate=True, _delay=0.01):
        try:
            print('[DarwinInfoAPI] Getting first {} DARWINs..'.format(_perPage))
            _darwins = self._Call_API_((_endpoint.format(_query_string.format(_status, _page, _perPage))),
              _type='GET',
              _data='')
        except Exception as ex:
            _exstr = 'Exception Type {0}. Args:\n{1!r}'
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            return

        if _iterate:
            _pages = int(_darwins['totalPages'])
            _darwins = _darwins['content']
            print('[DarwinInfoAPI] {} pages of {} DARWINs each found.. iterating, stand by! :muscle:\n'.format(_pages, _perPage))
            for i in range(_page + 1, _pages):
                print(('\r[DarwinInfoAPI] Getting page {} of {}'.format(i + 1, _pages)), end='', flush=True)
                try:
                    _darwins = _darwins + self._Call_API_((_endpoint.format(_query_string.format(_status, i, _perPage))),
                      _type='GET',
                      _data='')['content']
                    if _delay > 0:
                        time.sleep(_delay)
                except Exception as ex:
                    _exstr = 'Exception Type {0}. Args:\n{1!r}'
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    continue

        return pd.DataFrame(_darwins)

    def _Get_Filtered_DARWINS_(self, _endpoint='/products', _filters=[
 [
  'drawdown', -10, 0, '6m'],
 [
  'return', 5, 100, '1m']], _order=[
 'return', '12m', 'DESC'], _page=0, _perPage=50, _delay=0.01):
        _json = dict(filter=[dict(name=(_filters[i][0]), options=[dict(max=(_filters[i][2]), min=(_filters[i][1]), period=(_filters[i][3]))]) for i in range(len(_filters))],
          order=(_order[2]),
          orderField=(_order[0]),
          page=_page,
          perPage=_perPage,
          period=(_order[1]))
        _rets = []
        while _json['page'] != -1:
            print(('\r[DarwinInfoAPI] Getting page {} of DARWINs that satisfy criteria..'.format(_json['page'])),
              end='', flush=True)
            try:
                _ret = self._Call_API_(_endpoint, _type='POST',
                  _data=(str(_json).replace("'", '"')))
                if len(_ret) > 0:
                    _json['page'] += 1
                    _rets = _rets + _ret
                    time.sleep(_delay)
                else:
                    _json['page'] = -1
            except AssertionError:
                print('[ERROR] name, period, min and max lists must be the same length.')
                return

        return pd.DataFrame(_rets)

    def _Get_DARWIN_OHLC_Candles_(self, _symbols=[
 'KVL'], _resolution='1m', _from_dt='2019-05-31 12:00:00', _to_dt=str(pd.Timestamp('now')), _timeframe='/1D', _endpoint='/products/{}/candles{}', _delay=0.01):
        if _from_dt != '':
            _from_epoch = int(pd.Timestamp(_from_dt).timestamp())
            _to_epoch = int(pd.Timestamp(_to_dt).timestamp())
            _query_string = f"?resolution={_resolution}&from={_from_epoch}                             &to={_to_epoch}"
        else:
            if _timeframe != '':
                _query_string = f"{_timeframe}?resolution={_resolution}"
            else:
                print('[KERNEL] Inputs not recognized.. please try again.')
                return
        _candles = {}
        for _darwin in _symbols:
            try:
                print('[DarwinInfoAPI] Getting Candles for {}..'.format(_darwin))
                _d = self._Call_API_((_endpoint.format(_darwin, _query_string)),
                  _type='GET',
                  _data='')
                _candles[_darwin] = pd.DataFrame(data=[_row['candle'] for _row in _d['candles']],
                  index=[_row['timestamp'] for _row in _d['candles']])
                _candles[_darwin].index = pd.to_datetime((_candles[_darwin].index), unit='s')
            except Exception as ex:
                _exstr = 'Exception Type {0}. Args:\n{1!r}'
                _msg = _exstr.format(type(ex).__name__, ex.args)
                print(_msg)
                return

        return _candles