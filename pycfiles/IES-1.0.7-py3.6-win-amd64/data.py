# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\data.py
# Compiled at: 2018-12-18 03:42:47
# Size of source mod 2**32: 4633 bytes
from strategycontainer.tsp.data.equity_market1indicator import USEquityMarket1Daily, USEquityMarket1Weekly
from strategycontainer.tsp.loaders.equity_market1_loader import outer2inner as market1FieldMap
import pandas as pd

class Data:

    def __init__(self, var):
        self.var = var
        self.tradeCalendarCache = {}

    @property
    def currentBar(self):
        return self.var._FRAMEWORK_BT_CURRENTTIME

    def history(self, assets, fields, bar_count, frequency, adj_flag=False, start_date=None, end_date=None):
        return self.var.ips_api._framework_getHistory(assets, fields, int(bar_count), frequency, self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M'), adj_flag, start_date, end_date)

    def current(self, assets, fields, adj_flag=False):
        return self.var.ips_api._framework_getCurrent(self.var._FRAMEWORK_PORTFOLIOID, assets, fields, adj_flag)

    def market1_indicator(self, fields, bar_count):
        if not isinstance(fields, list):
            raise Exception('param fields should be a list')
        else:
            if len(fields) == 0:
                raise Exception('fields list is empty')
            else:
                dailyIndicator = []
                weeklyIndicator = []
                for field in fields:
                    if field in USEquityMarket1Daily.columns:
                        dailyIndicator.append(market1FieldMap[field.name])
                    else:
                        if field in USEquityMarket1Weekly.columns:
                            weeklyIndicator.append(market1FieldMap[field.name])
                        else:
                            raise Exception('field type must be USEquityMarket1Daily or USEquityMarket1Weekly')

                dailyDf = None
                weeklyDf = None
                if dailyIndicator:
                    dailyDf = self.var.ips_api._framework_getMarket1DailyIndicator(dailyIndicator, int(bar_count), self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M'))
                if weeklyIndicator:
                    weeklyDf = self.var.ips_api._framework_getMarket1PeriodIndicator(weeklyIndicator, int(bar_count), self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M'))
            if dailyDf is not None:
                df = pd.DataFrame(index=(dailyDf.index))
            else:
                df = pd.DataFrame(index=(weeklyDf.index))
        for field in fields:
            if field in USEquityMarket1Daily.columns:
                df.insert(len(df.columns), field, dailyDf[market1FieldMap[field.name]])
            else:
                df.insert(len(df.columns), field, weeklyDf[market1FieldMap[field.name]])

        return df

    def can_trade(self, assets):
        if self.var._FRAMEWORK_IS_BACKTEST:
            result = pd.Series()
            new_assets = []
            if isinstance(assets, list):
                new_assets = list(assets)
            else:
                new_assets.append(assets)
            for s in new_assets:
                if s.sid in self.tradeCalendarCache.keys():
                    trade_calendar = self.tradeCalendarCache[s.sid]
                else:
                    if self.var._FRAMEWORK_IS_TEST_STRATEGY:
                        trade_calendar = self.var.ips_api._framework_getTradeCalendar(self.var._FRAMEWORK_BT_STARTDATE, self.var._FRAMEWORK_BT_ENDDATE, s.sid)['date']
                    else:
                        trade_calendar = self.var.ips_api._framework_getTradeCalendar(self.var._FRAMEWORK_TRAIN_STARTDATE, self.var._FRAMEWORK_BT_ENDDATE, s.sid)['date']
                    self.tradeCalendarCache[s.sid] = trade_calendar
                result.set_value(s, self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d') in trade_calendar.values)

            if len(result) == 1:
                return result.iloc[0]
            else:
                return result
        elif self.var._FRAMEWORK_IS_LIVETRADE:
            if self.var._FRAMEWORK_MARKETTYPE == 'US':
                new_assets = []
                if isinstance(assets, list):
                    new_assets = list(assets)
                else:
                    new_assets.append(assets)
                if len(new_assets) == 1:
                    return True
                else:
                    return pd.Series([True for _ in range(len(new_assets))], index=new_assets)
            else:
                series = self.var.ips_api._framework_canTrade(assets)
                if len(series) == 1:
                    return series.iloc[0]
                else:
                    return pd.Series((series.values), index=[self.var.api.sid(i) for i in series.index])