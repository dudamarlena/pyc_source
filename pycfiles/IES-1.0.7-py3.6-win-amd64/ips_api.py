# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\ips_api.py
# Compiled at: 2018-12-18 03:51:50
# Size of source mod 2**32: 37235 bytes
"""
Created on 2017年7月29日

@author: sharon
"""
import requests, datetime, time, math, os, pytz, pandas as pd, numpy as np
from pandas import read_csv
from pandas.compat import StringIO
from strategycontainer.exception import PortfolioNotFoundException, PortfolioNotStartException, BusinessError
from strategycontainer.tsp.data import USEquityFundamental

class IPSApi(object):

    def __init__(self, var):
        self.var = var

    def _framework_tradingServer_url(self):
        return self.var.PIPA_HOST + '/ts-mng/'

    def _framework_createSubPortfolio(self, groupId, count, percentage):
        param = {'parentPID':self.var._FRAMEWORK_PORTFOLIOID, 
         'groupId':groupId,  'subPortfolioCount':count,  'percentage':percentage}
        return self._framework_getResponse(self._framework_tradingServer_url() + 'createSubPortfolio', param)

    def _framework_readyToDebug(self):
        param = {'portfolioId': self.var._FRAMEWORK_PORTFOLIOID}
        self._framework_putResponse(self._framework_tradingServer_url() + 'readyForDebug', param, '')

    def _framework_saveCustomData(self, key, value):
        param = {'portfolioId':self.var._FRAMEWORK_PORTFOLIOID, 
         'key':key}
        self._framework_postResponse(self._framework_tradingServer_url() + 'customData', param, value)

    def _framework_loadCustomData(self, key):
        param = {'portfolioId':self.var._FRAMEWORK_PORTFOLIOID, 
         'key':key}
        return self._framework_getResponse(self._framework_tradingServer_url() + 'customData', param)

    def _framework_getStockWatchlist(self):
        param = {}
        return self._framework_getResponse(self._framework_tradingServer_url() + 'stockWatchlist', param)

    def _framework_setCommission(self, portfolioId, param):
        param['portfolioId'] = portfolioId
        self._framework_postResponse(self._framework_tradingServer_url() + 'setCommissionModel', param, '')

    def _framework_setBenchmark(self, portfolioId, benchmark):
        param = {'portfolioId':portfolioId, 
         'benchmark':benchmark}
        self._framework_postResponse(self._framework_tradingServer_url() + 'setBenchmark', param, '')

    def _framework_setUseAdjPrice(self, portfolioId):
        param = {'portfolioId':portfolioId, 
         'useAdjPrice':True}
        self._framework_postResponse(self._framework_tradingServer_url() + 'setUseAdjPrice', param, '')

    def _framework_backtestNoop(self):
        param = {'portfolioId': self.var._FRAMEWORK_PORTFOLIOID}
        self._framework_getResponse(self._framework_tradingServer_url() + 'backtestNoop', param)

    def _framework_getPortfolio(self, portfolioId, subPortfolioId):
        self._framework_waitForBTOrderFinish()
        param = {'portfolioId':portfolioId,  'marketType':self.var._FRAMEWORK_MARKETTYPE}
        if subPortfolioId is not None:
            param['subPortfolioId'] = subPortfolioId
        if self.var._FRAMEWORK_IS_BACKTEST:
            param['tradeTime'] = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M')
            param['phase'] = self.var._FRAMEWORK_CURRENT_PHASE
        return self._framework_getResponse(self._framework_tradingServer_url() + 'getPortfolio', param)

    def _framework_getTradeCalendar(self, startDate, endDate, sid=None):
        param = {'startDate':startDate, 
         'endDate':endDate,  'marketType':self.var._FRAMEWORK_MARKETTYPE}
        if sid is not None:
            param['stockId'] = sid
        data = self._framework_getResponse(self._framework_tradingServer_url() + 'getTradeCalendar', param)
        out = StringIO()
        out.write(data)
        out.seek(0)
        return read_csv(out, dtype={'date': np.str})

    def _framework_getCurrent(self, portfolio_id, assets, fields, adj_flag):
        singleAsset = True
        if isinstance(assets, list):
            if len(assets) > 1:
                singleAsset = False
        if singleAsset:
            if isinstance(assets, list):
                assets = assets[0]
        singleField = True
        if isinstance(fields, list):
            if len(fields) > 1:
                singleField = False
        else:
            if singleField:
                if isinstance(fields, list):
                    fields = fields[0]
            ids = []
            symbols = []
            if singleAsset:
                ids.append(str(assets.sid))
                symbols.append(assets.symbol)
            else:
                for asset in assets:
                    ids.append(str(asset.sid))
                    symbols.append(asset.symbol)

        param = {'portfolioId': portfolio_id}
        param['ids'] = ','.join(ids)
        param['symbols'] = ','.join(symbols)
        if self.var._FRAMEWORK_IS_BACKTEST:
            param['currentTime'] = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d')
        else:
            param['marketType'] = self.var._FRAMEWORK_MARKETTYPE
            data = self._framework_getResponse(self._framework_tradingServer_url() + 'getCurrent', param)
            out = StringIO()
            out.write(data)
            out.seek(0)
            df = read_csv(out, index_col='asset')
            if self.var._FRAMEWORK_IS_BACKTEST:
                if self.var._FRAMEWORK_MARKETTYPE == 'US':
                    df['adj_close'] = df['price']
                    if adj_flag:
                        ratio = df['close'] / df['adj_close']
                        df['open'] = df['open'] / ratio
                        df['high'] = df['high'] / ratio
                        df['low'] = df['low'] / ratio
                        df['close'] = df['close'] / ratio
                    if self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%H%M') < '1300':
                        df['price'] = df['open']
                    else:
                        df['price'] = df['close']
                else:
                    if self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%H%M') <= '1130':
                        df['price'] = df['open']
                    else:
                        df['price'] = df['open']
        df['last_traded'] = df['last_traded'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000, self.var._TIMEZONE))
        if singleAsset:
            if singleField:
                return df.iloc[0][fields]
        if singleAsset:
            if not singleField:
                return df.loc[(assets.sid, fields)]
        if not singleAsset and singleField:
            _s = df.loc[:, fields]
            result = pd.Series()
            for asset in assets:
                result[asset] = _s[asset.sid]

            return result
        else:
            result = pd.DataFrame(index=assets, columns=fields)
            for asset in assets:
                for field in fields:
                    result[field][asset] = df[field][asset.sid]

            return result

    def _framework_getHistory(self, assets, fields, bar_count, frequency, current_time, adj_flag, start_date=None, end_date=None):
        if not isinstance(assets, list):
            assets = [
             assets]
        elif not isinstance(fields, list):
            fields = [
             fields]
        else:
            singleAsset = True if len(assets) <= 1 else False
            singleField = True if len(fields) <= 1 else False
            fields = [s.lower() for s in fields]
            _fields = list(fields)
            if self.var._FRAMEWORK_MARKETTYPE == 'US':
                idx = None
                if end_date is not None:
                    end_date = pd.Timestamp(end_date)
                    current_time = end_date.strftime('%Y%m%d') + '2230'
                    end_date = end_date.strftime('%Y%m%d')
                else:
                    idx = self.var.cal.get_first_idx(pd.Timestamp(current_time[0:8]))
                    end_date = self.var.cal[idx].strftime('%Y%m%d')
                if start_date is not None:
                    start_date = self.var.cal[self.var.cal.get_first_ge_idx(pd.Timestamp(start_date))]
                    start_date = start_date.strftime('%Y%m%d')
                else:
                    if idx is None:
                        idx = self.var.cal.get_first_idx(pd.Timestamp(current_time[0:8]))
                    if current_time[8:12] < '2230':
                        idx = max(0, idx - 1)
                    start_idx = max(0, idx - bar_count + 1)
                    start_date = self.var.cal[start_idx].strftime('%Y%m%d')
                param = {'startDate':start_date, 
                 'endDate':end_date,  'marketType':self.var._FRAMEWORK_MARKETTYPE}
                ids = []
                asset_map = {}
                for asset in assets:
                    ids.append(str(asset.sid))
                    asset_map[str(asset.sid)] = asset

                str_ids = ','.join(ids)
                ret = {}
                cache = {}
                trade_dt = None
                quotesIndicators = ['open', 'high', 'low', 'close', 'volume', 'adj_close']
                fundmentalIndicators = [c.name.lower() for c in USEquityFundamental.columns]
                if 'price' in fields:
                    _fields.remove('price')
                    if 'close' not in _fields:
                        _fields.append('close')
                for indicator in _fields:
                    if indicator in ret.keys():
                        continue
                    if indicator in quotesIndicators:
                        if indicator == 'adj_close':
                            self.fetch_indicator(str_ids, 'adj_close', param, cache)
                            ret['adj_close'] = cache['adj_close']
                        else:
                            self.fetch_indicator(str_ids, 'close', param, cache)
                            if not adj_flag:
                                self.fetch_indicator(str_ids, 'split_close', param, cache)
                                if indicator == 'close':
                                    ret['close'] = cache['split_close']
                                else:
                                    if 'split_ratio' not in cache.keys():
                                        cache['split_ratio'] = cache['close'] / cache['split_close']
                                    self.fetch_indicator(str_ids, indicator, param, cache)
                                    if indicator == 'volume':
                                        ret['volume'] = cache['volume'] * cache['split_ratio']
                                    else:
                                        ret[indicator] = cache[indicator] / cache['split_ratio']
                            else:
                                self.fetch_indicator(str_ids, 'adj_close', param, cache)
                            if indicator == 'close':
                                ret['close'] = cache['adj_close']
                            else:
                                if 'adj_ratio' not in cache.keys():
                                    cache['adj_ratio'] = cache['close'] / cache['adj_close']
                                self.fetch_indicator(str_ids, indicator, param, cache)
                                if indicator == 'volume':
                                    ret['volume'] = cache['volume'] * cache['adj_ratio']
                                else:
                                    ret[indicator] = cache[indicator] / cache['adj_ratio']
                    else:
                        if indicator in fundmentalIndicators:
                            if trade_dt is None:
                                trade_dt = list(self.var.cal.all_sessions)
                                trade_dt = pd.DataFrame(trade_dt, index=trade_dt, columns=['date']).sort_index()
                            cache[indicator] = self._fetch_fundamental(ids, indicator, bar_count, current_time, trade_dt)
                            ret[indicator] = cache[indicator]
                        else:
                            self.fetch_indicator(str_ids, indicator, param, cache)
                            ret[indicator] = cache[indicator]

                if 'price' in fields:
                    ret['price'] = ret['close']
                pnl = pd.Panel(ret)
                x = fields[0] if singleField else fields
                y = ids[0] if singleAsset else ids
                r = pnl.loc[x, :, y]
                if isinstance(r, pd.Panel):
                    r.minor_axis = map(lambda x: asset_map[x], ids)
                    return r
                if isinstance(r, pd.DataFrame):
                    if singleAsset:
                        return r.loc[:, x]
                    else:
                        r.columns = map(lambda x: asset_map[x], ids)
                        return r.loc[:, assets]
                else:
                    return r
            else:
                idx = self.var.cal.get_first_idx(pd.Timestamp(current_time[0:8]))
                if current_time[8:12] < '2030':
                    idx = max(0, idx - 1)
                start_idx = max(0, idx - bar_count + 1)
                param = {'startDate':self.var.cal[start_idx].strftime('%Y%m%d'),  'endDate':self.var.cal[idx].strftime('%Y%m%d'),  'marketType':self.var._FRAMEWORK_MARKETTYPE}
                ids = []
                asset_map = {}
                for asset in assets:
                    ids.append(str(asset.sid))
                    asset_map[str(asset.sid)] = asset

                str_ids = ','.join(ids)
                ret = {}
                preIndicators = ['pre_open', 'pre_high', 'pre_low', 'pre_close', 'pre_volume', 'pre_fund_open', 'pre_fund_high', 'pre_fund_low', 'pre_fund_close', 'pre_fund_volume']
                postIndicators = ['post_open', 'post_high', 'post_low', 'post_close', 'post_volume']
                cache = {}
                for indicator in _fields:
                    if indicator in ret.keys():
                        continue
                    if indicator in postIndicators:
                        self.fetch_indicator(str_ids, 'cumbacktafactor', param, cache)
                        self.fetch_indicator(str_ids, indicator[5:], param, cache)
                        back_factor_df = cache['cumbacktafactor']
                        df = cache[indicator[5:]]
                        df = df * back_factor_df
                        ret[indicator] = df
                    else:
                        if indicator in preIndicators:
                            if indicator.startswith('pre_fund_'):
                                if 'fund_fronttafactor' not in cache.keys():
                                    self.fetch_indicator(str_ids, 'fund_fronttafactor', param, cache)
                                    df = cache['fund_fronttafactor']
                                    df.iloc[-1] = 1
                                    df = df.sort_index(ascending=False).cumprod(axis=0).sort_index()
                                    cache['fund_fronttafactor'] = df
                                front_factor_df = cache['fund_fronttafactor']
                            else:
                                if 'fronttafactor' not in cache.keys():
                                    self.fetch_indicator(str_ids, 'fronttafactor', param, cache)
                                    df = cache['fronttafactor']
                                    df.iloc[-1] = 1
                                    df = df.sort_index(ascending=False).cumprod(axis=0).sort_index()
                                    cache['fronttafactor'] = df
                                front_factor_df = cache['fronttafactor']
                            self.fetch_indicator(str_ids, indicator[4:], param, cache)
                            df = cache[indicator[4:]]
                            df = df * front_factor_df
                            ret[indicator] = df
                        else:
                            self.fetch_indicator(str_ids, indicator, param, cache)
                            ret[indicator] = cache[indicator]

                pnl = pd.Panel(ret)
                x = _fields[0] if singleField else _fields
                y = ids[0] if singleAsset else ids
                r = pnl.loc[x, :, y]
                if isinstance(r, pd.Panel):
                    r.minor_axis = map(lambda x: asset_map[x], ids)
                    return r
                if isinstance(r, pd.DataFrame):
                    if singleAsset:
                        return r.loc[:, x]
                    else:
                        r.columns = map(lambda x: asset_map[x], ids)
                        return r.loc[:, assets]
                else:
                    return r

    def fetch_indicator(self, str_ids, indicator, param, cache):
        if indicator not in cache.keys():
            param['indicatorName'] = indicator
            data = self._framework_postResponse(self._framework_tradingServer_url() + 'getDailyIndicator', param, str_ids)
            out = StringIO()
            out.write(data)
            out.seek(0)
            df = read_csv(out, parse_dates=['date'], sep='|').set_index('date')
            tradedays = self.var.cal.slice(param['startDate'], param['endDate'])
            df2 = pd.DataFrame(index=(list(set(df.index) | set(tradedays.index))), columns=(df.columns)).sort_index()
            df2[df.notnull()] = df
            df2 = df2.tz_localize('UTC', level=0)
            cache[indicator] = df2.apply(pd.to_numeric)

    def _framework_getFundamental(self, assets, fields, bar_count, current_time):
        if not isinstance(assets, list):
            assets = [
             assets]
        else:
            if not isinstance(fields, list):
                fields = [
                 fields]
            singleAsset = True if len(assets) <= 1 else False
            singleField = True if len(fields) <= 1 else False
            _fields = [s.lower() for s in fields]
            ids = []
            asset_map = {}
            for asset in assets:
                ids.append(str(asset.sid))
                asset_map[str(asset.sid)] = asset

            ret = {}
            trade_dt = list(self.var.cal.all_sessions)
            trade_dt = pd.DataFrame(trade_dt, index=trade_dt, columns=['date']).sort_index()
            for indicator in _fields:
                if indicator in ret.keys():
                    pass
                else:
                    ret[indicator] = self._fetch_fundamental(ids, indicator, bar_count, current_time, trade_dt)

            pnl = pd.Panel(ret)
            x = _fields[0] if singleField else _fields
            y = ids[0] if singleAsset else ids
            r = pnl.loc[x, :, y]
            if isinstance(r, pd.Panel):
                r.minor_axis = list(map(lambda x: asset_map[x], ids))
                return r
            if isinstance(r, pd.DataFrame):
                if singleAsset:
                    return r.loc[:, x]
                else:
                    r.columns = map(lambda x: asset_map[x], ids)
                    return r.loc[:, assets]
            else:
                return r

    def _fetch_fundamental(self, asset_ids, indicator, bar_count, current_time, trade_dt):
        endday = pd.Timestamp(current_time[0:8])
        try:
            data = self.var.dataCache.get('fundamental_' + indicator, endday)
        except KeyError:
            param = {'marketType':self.var._FRAMEWORK_MARKETTYPE, 
             'fields':indicator}
            data = self._framework_postResponse(self._framework_tradingServer_url() + 'getFundamental', param, ' ')
            out = StringIO()
            out.write('date|s_id|v')
            for i in data:
                for key, value in i.items():
                    if key.startswith('s_'):
                        out.write('\n')
                        out.write(i['date'])
                        out.write('|')
                        out.write(key[2:])
                        out.write('|')
                        out.write(str(value))

            if self.var._FRAMEWORK_IS_BACKTEST:
                end_session = pd.Timestamp(self.var._FRAMEWORK_BT_ENDDATE)
            if self.var._FRAMEWORK_IS_LIVETRADE:
                end_session = endday
            data = out
            self.var.dataCache.set('fundamental_' + indicator, data, end_session)

        data.seek(0)
        df = pd.read_csv(data, parse_dates=['date'], sep='|', dtype={'s_id': str})
        df = df.pivot(values='v', index='date', columns='s_id').sort_index()
        df = pd.concat([trade_dt, df], axis=1).fillna(method='ffill')
        df = df[df.index.isin(trade_dt.index)]
        df.drop('date', errors='ignore', inplace=True, axis=1)
        df.drop('mark', errors='ignore', inplace=True, axis=1)
        df.drop('groupId', errors='ignore', inplace=True, axis=1)
        df = self.slice_fundamental_indicator(current_time, bar_count, asset_ids, df)
        return df.apply(pd.to_numeric)

    def slice_fundamental_indicator(self, current_time, window_lengh, asset_ids, returnFrame):
        idx = self.var.cal.get_first_idx(pd.Timestamp(current_time[0:8]))
        if current_time[8:12] < '2230':
            idx = max(0, idx - 1)
        start_idx = max(0, idx - window_lengh + 1)
        trade_dt = self.var.cal.all_sessions[start_idx:idx + 1]
        returnFrame = returnFrame.loc[(trade_dt, list(set(asset_ids) & set(returnFrame.columns)))]
        tmpFrame = pd.DataFrame(index=trade_dt, columns=(list(set(asset_ids) - set(returnFrame.columns))))
        returnsFrame = pd.concat([returnFrame, tmpFrame], axis=1)
        return returnsFrame

    def _framework_getMarket1DailyIndicator(self, fields, bar_count, current_time):
        param = {'barCount':bar_count, 
         'currentTime':current_time}
        param['fields'] = ','.join(fields)
        data = self._framework_getResponse(self._framework_tradingServer_url() + 'getMarket1DailyIndicator', param)
        out = StringIO()
        out.write(data)
        out.seek(0)
        df = read_csv(out, index_col='date', parse_dates=['date'])
        return df

    def _framework_getMarket1PeriodIndicator(self, fields, bar_count, current_time):
        param = {'barCount':bar_count, 
         'currentTime':current_time}
        param['fields'] = ','.join(fields)
        data = self._framework_getResponse(self._framework_tradingServer_url() + 'getMarket1PeriodIndicator', param)
        out = StringIO()
        out.write(data)
        out.seek(0)
        df = read_csv(out, index_col='date', parse_dates=['date'])
        return df

    def _framework_getAllStocks(self):
        data = self._framework_getResponse(self._framework_tradingServer_url() + 'allStocks', {'marketType': self.var._FRAMEWORK_MARKETTYPE})
        out = StringIO()
        out.write(data)
        out.seek(0)
        return read_csv(out, dtype={'start_date':str,  'end_date':str})

    def _framework_getStockUniverse(self, universe):
        param = {'universe': universe}
        data = self._framework_getResponse(self._framework_tradingServer_url() + 'stockUniverse', param)
        out = StringIO()
        out.write(data)
        out.seek(0)
        df = read_csv(out)
        return df['sid']

    def _framework_canTrade(self, assets):
        param = {'marketType': self.var._FRAMEWORK_MARKETTYPE}
        if isinstance(assets, list):
            ids = []
            symbols = []
            for asset in assets:
                ids.append(str(asset.sid))
                symbols.append(asset.symbol)

            param['ids'] = ','.join(ids)
            param['symbols'] = ','.join(symbols)
        else:
            param['ids'] = assets.sid
            param['symbols'] = assets.symbol
        data = self._framework_getResponse(self._framework_tradingServer_url() + 'canTrade', param)
        out = StringIO()
        out.write(data)
        out.seek(0)
        return read_csv(out, index_col='sid').iloc[:, 0]

    def _framework_waitForBTOrderFinish(self):
        if self.var._FRAMEWORK_IS_BACKTEST:
            while True:
                try:
                    isOrderFinish = self._framework_isBTOrdersFinished(self.var._FRAMEWORK_PORTFOLIOID, self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M'))
                    if isOrderFinish:
                        break
                    else:
                        time.sleep(0.2)
                except PortfolioNotFoundException as e:
                    raise e
                except Exception as msg:
                    print(str(msg))
                    time.sleep(0.2)

    def _framework_getOpenOrders(self, portfolioId, sid, subPortfolioId):
        param = {'portfolioId': portfolioId}
        if sid is not None:
            param['stockId'] = sid
        if subPortfolioId is not None:
            param['subPortfolioId'] = subPortfolioId
        return self._framework_getResponse(self._framework_tradingServer_url() + 'getOpenOrders', param)

    def _framework_getOrder(self, portfolioId, oid, subPortfolioId):
        param = {'portfolioId':portfolioId, 
         'orderId':oid,  'phase':self.var._FRAMEWORK_CURRENT_PHASE}
        if subPortfolioId is not None:
            param['subPortfolioId'] = subPortfolioId
        return self._framework_getResponse(self._framework_tradingServer_url() + 'getOrder', param)

    def genParam(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        if amount is None or asset is None or orderType is None:
            raise Exception('amount or asset can not be None')
        else:
            if math.isnan(amount):
                raise Exception('amount can not be NaN')
            else:
                param = {'stockId':asset.sid, 
                 'symbol':asset.symbol,  'amount':amount,  'orderType':orderType,  'portfolioId':portfolioId}
                if limitPrice is not None:
                    param['limitPrice'] = limitPrice
                if stopPrice is not None:
                    param['stopPrice'] = stopPrice
                if exchange is not None:
                    param['exchange'] = exchange
                if scheduleTime is not None:
                    param['scheduleTime'] = scheduleTime
                if orderTime is not None:
                    param['orderTime'] = orderTime
                param['phase'] = self.var._FRAMEWORK_CURRENT_PHASE
                if sub_portfolio_id is not None:
                    param['subPortfolioId'] = sub_portfolio_id
            if trade_threshhold is not None:
                param['tradeThreshHold'] = trade_threshhold
        return param

    def _framework_sendTechIndicator(self, indicator):
        param = {'indicator':indicator, 
         'marketType':self.var._FRAMEWORK_MARKETTYPE}
        self._framework_getResponse(self._framework_tradingServer_url() + 'sendTechIndicator', param)

    def _framework_sendIDAComplete(self):
        param = {'marketType': self.var._FRAMEWORK_MARKETTYPE}
        self._framework_getResponse(self._framework_tradingServer_url() + 'sendIDAComplete', param)

    def _framework_EODLatestDate(self):
        param = {}
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'EODLatestDate', param))

    def _framework_order(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        param = self.genParam(portfolioId, asset, amount, orderType, limitPrice, stopPrice, exchange, scheduleTime, orderTime, sub_portfolio_id, trade_threshhold)
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'order', param))

    def _framework_orderValue(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        param = self.genParam(portfolioId, asset, amount, orderType, limitPrice, stopPrice, exchange, scheduleTime, orderTime, sub_portfolio_id, trade_threshhold)
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'orderValue', param))

    def _framework_orderPercent(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        param = self.genParam(portfolioId, asset, amount, orderType, limitPrice, stopPrice, exchange, scheduleTime, orderTime, sub_portfolio_id, trade_threshhold)
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'orderPercent', param))

    def _framework_orderTarget(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        param = self.genParam(portfolioId, asset, amount, orderType, limitPrice, stopPrice, exchange, scheduleTime, orderTime, sub_portfolio_id, trade_threshhold)
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'orderTarget', param))

    def _framework_orderTargetValue(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        param = self.genParam(portfolioId, asset, amount, orderType, limitPrice, stopPrice, exchange, scheduleTime, orderTime, sub_portfolio_id, trade_threshhold)
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'orderTargetValue', param))

    def _framework_orderTargetPercent(self, portfolioId, asset, amount, orderType, limitPrice=None, stopPrice=None, exchange=None, scheduleTime=None, orderTime=None, sub_portfolio_id=None, trade_threshhold=None):
        param = self.genParam(portfolioId, asset, amount, orderType, limitPrice, stopPrice, exchange, scheduleTime, orderTime, sub_portfolio_id, trade_threshhold)
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'orderTargetPercent', param))

    def _framework_setTargetPortfolio(self, portfolioId, signals, exchange=None, scheduleTime=None, orderTime=None):
        param = {'signals':signals, 
         'portfolioId':portfolioId}
        if exchange is not None:
            param['exchange'] = exchange
        if scheduleTime is not None:
            param['scheduleTime'] = scheduleTime
        if orderTime is not None:
            param['orderTime'] = orderTime
        param['phase'] = self.var._FRAMEWORK_CURRENT_PHASE
        return str(self._framework_getResponse(self._framework_tradingServer_url() + 'setTargetPortfolio', param))

    def _framework_record(self, portfolioId, recordTime, records):
        param = {'portfolioId': portfolioId}
        if recordTime is not None:
            param['recordTime'] = recordTime
        param['phase'] = self.var._FRAMEWORK_CURRENT_PHASE
        self._framework_postResponse(self._framework_tradingServer_url() + 'record', param, records)

    def _framework_log(self, portfolioId, logs):
        param = {'portfolioId': portfolioId}
        self._framework_postResponse(self._framework_tradingServer_url() + 'log', param, logs)

    def _framework_elasticLog(self, log):
        if self.var._FRAMEWORK_IS_LIVETRADE:
            param = {'portfolioId': self.var._FRAMEWORK_PORTFOLIOID}
            self._framework_postResponse(self._framework_tradingServer_url() + 'elasticLog', param, log)

    def _framework_mailToDeveloper(self, content):
        if self.var._FRAMEWORK_IS_LIVETRADE:
            param = {'portfolioId': self.var._FRAMEWORK_PORTFOLIOID}
            self._framework_postResponse(self._framework_tradingServer_url() + 'mailToDeveloper', param, content)

    def _framework_startOfTradeDay(self, portfolioId, today, lastday):
        param = {'portfolioId':portfolioId,  'today':today,  'lastday':lastday}
        self._framework_getResponse(self._framework_tradingServer_url() + 'startOfTradeDay', param)

    def _framework_isBTOrdersFinished(self, portfolioId, tradeTime):
        param = {'portfolioId':portfolioId, 
         'tradeTime':tradeTime,  'phase':self.var._FRAMEWORK_CURRENT_PHASE}
        return self._framework_getResponse(self._framework_tradingServer_url() + 'isBTOrdersFinished', param)

    def _framework_endOfBacktest(self, portfolioId):
        param = {'portfolioId': portfolioId}
        self._framework_getResponse(self._framework_tradingServer_url() + 'endOfBacktest', param)

    def _framework_cancelBacktest(self, portfolioId):
        param = {'portfolioId': portfolioId}
        self._framework_getResponse(self._framework_tradingServer_url() + 'cancelBacktest', param)

    def _framework_getStrategyCode(self, portfolioId):
        param = {'portfolioId': portfolioId}
        try:
            r = requests.get((self._framework_tradingServer_url() + 'getPortfolioStrategyCode'), params=param, stream=True, verify=False)
            if r.status_code == 200:
                if not os.path.exists('strategy/'):
                    os.makedirs('strategy/')
                with open('strategy/StrategyCode.py', 'wb') as (code):
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            code.write(chunk)

                self.var._FRAMEWORK_MARKETTYPE = 'CN' if r.headers['marketType'] == '2' else 'US'
                if r.headers['marketType'] == '2':
                    self.var._TIMEZONE = pytz.timezone('Asia/Shanghai')
                self.var._FRAMEWORK_EXCEPTIONHANDLE = 'RESTART' if r.headers['exceptionHandle'] == '2' else 'CONTINUE'
                self.var.max_call_per_sec = int(r.headers['max_call_per_sec'])
                if self.var._FRAMEWORK_IS_BACKTEST:
                    self.var._FRAMEWORK_BT_STARTDATE = r.headers['startDate']
                    self.var._FRAMEWORK_BT_ENDDATE = r.headers['endDate']
                    self.var._FRAMEWORK_REMOTEDEBUG = r.headers['remoteDebug'] == 'true'
                    self.var._FRAMEWORK_IS_TEST_STRATEGY = r.headers['strategyType'] == '1'
                    self.var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY = not self.var._FRAMEWORK_IS_TEST_STRATEGY
                    self.var._FRAMEWORK_CURRENT_PHASE = 'train' if self.var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY else 'test'
                    if self.var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY:
                        self.var._FRAMEWORK_TRAIN_STARTDATE = r.headers['trainStartDate']
                        self.var._FRAMEWORK_TRAIN_ENDDATE = r.headers['trainEndDate']
            else:
                raise Exception('[' + str(r.status_code) + ']' + r.text)
        except Exception as msg:
            raise msg

    def _framework_checkResponse(self, r):
        if r.status_code == 200:
            if r.json()['code'] == 0:
                return r.json()['data']
            else:
                if r.json()['code'] == 1:
                    raise PortfolioNotFoundException('[' + str(r.json()['code']) + ']' + r.json()['errMsg'])
                else:
                    if r.json()['code'] == 4:
                        raise PortfolioNotStartException('[' + str(r.json()['code']) + ']' + r.json()['errMsg'])
                    else:
                        if r.json()['code'] == 7:
                            raise BusinessError('[' + str(r.json()['code']) + ']' + r.json()['errMsg'])
                        else:
                            raise Exception('[' + str(r.json()['code']) + ']' + r.json()['errMsg'])
        else:
            raise Exception('[' + str(r.status_code) + ']' + r.text)

    def _framework_postResponse(self, url, parameter, json):
        self.var.wait_if_call_too_fast()
        retryCount = 0
        while True:
            try:
                r = requests.post(url, params=parameter, headers=(self.var.HTTP_HEADERS), data=json, verify=False)
                return self._framework_checkResponse(r)
            except (PortfolioNotFoundException, PortfolioNotStartException, BusinessError) as e:
                raise e
            except Exception as msg:
                retryCount = retryCount + 1
                if retryCount >= 10:
                    raise msg
                time.sleep(3)

    def _framework_putResponse(self, url, parameter, json):
        self.var.wait_if_call_too_fast()
        retryCount = 0
        while True:
            try:
                r = requests.put(url, params=parameter, headers=(self.var.HTTP_HEADERS), data=json, verify=False)
                return self._framework_checkResponse(r)
            except (PortfolioNotFoundException, PortfolioNotStartException, BusinessError) as e:
                raise e
            except Exception as msg:
                retryCount = retryCount + 1
                if retryCount >= 10:
                    raise msg
                time.sleep(3)

    def _framework_getResponse(self, url, parameter):
        self.var.wait_if_call_too_fast()
        retryCount = 0
        while True:
            try:
                r = requests.get(url, params=parameter, headers=(self.var.HTTP_HEADERS), verify=False)
                return self._framework_checkResponse(r)
            except (PortfolioNotFoundException, PortfolioNotStartException, BusinessError) as e:
                raise e
            except Exception as msg:
                retryCount = retryCount + 1
                if retryCount >= 10:
                    raise msg
                time.sleep(3)


if __name__ == '__main__':
    pass