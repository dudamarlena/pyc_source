# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\api.py
# Compiled at: 2018-12-18 03:59:23
# Size of source mod 2**32: 18260 bytes
"""
@author: sharon
"""
from strategycontainer.model import Order, MarketOrder, LimitOrder, StopOrder, StopLimitOrder, date_rules, time_rules, Equity
from strategycontainer.commission import PerShare, PerTrade, PerDollar
from itertools import chain
from six import iteritems
import json, datetime, pytz, pickle, pandas as pd

class API(object):

    def __init__(self, var):
        self.var = var

    def get_trade_calendar(self):
        return self.var.cal.all_sessions

    def __trade_days_between(self, start_date, end_date):
        end_session = pd.Timestamp(end_date)
        end_loc = self.var.cal.get_first_idx(end_session)
        end_session = self.var.cal.all_sessions[end_loc]
        start_idx, end_idx = self.var.cal.slice_locs(pd.Timestamp(start_date), end_session)
        return end_idx - start_idx

    def get_backtest_days(self):
        if self.var._FRAMEWORK_IS_LIVETRADE:
            return (0, 0)
        if self.var._FRAMEWORK_IS_BACKTEST:
            train_days = 0
            test_days = 0
            if self.var._FRAMEWORK_CURRENT_PHASE == 'train':
                train_days = self._API__trade_days_between(self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y-%m-%d'), self.var._FRAMEWORK_TRAIN_ENDDATE)
                start_session = pd.Timestamp(self.var._FRAMEWORK_BT_STARTDATE)
                start_loc = self.var.cal.get_first_ge_idx(start_session)
                start_session = self.var.cal.all_sessions[start_loc]
                test_days = self._API__trade_days_between(start_session, self.var._FRAMEWORK_BT_ENDDATE)
            else:
                if self.var._FRAMEWORK_CURRENT_PHASE == 'test':
                    test_days = self._API__trade_days_between(self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y-%m-%d'), self.var._FRAMEWORK_BT_ENDDATE)
            return (
             train_days, test_days)

    def create_subportfolio(self, groupId, num_of_subportfolio, percentage):
        return self.var.ips_api._framework_createSubPortfolio(groupId, num_of_subportfolio, percentage)

    def save_data(self, key, data):
        if data is not None:
            if key is not None:
                if not isinstance(key, str):
                    raise Exception('type of key must be str')
                self.var.ips_api._framework_saveCustomData(key, pickle.dumps(data).hex())

    def load_data(self, key):
        if key is None:
            return
        else:
            if not isinstance(key, str):
                raise Exception('type of key must be str')
            data = self.var.ips_api._framework_loadCustomData(key)
            if data is not None:
                return pickle.loads(bytes.fromhex(data))

    def set_adjusted_price(self):
        if self.var._FRAMEWORK_IS_BACKTEST:
            self.var.ips_api._framework_setUseAdjPrice(self.var._FRAMEWORK_PORTFOLIOID)

    def set_benchmark(self, benchmark):
        if self.var._FRAMEWORK_IS_BACKTEST:
            if benchmark is not None:
                self.var.ips_api._framework_setBenchmark(self.var._FRAMEWORK_PORTFOLIOID, benchmark.sid)

    def sid(self, sid):
        allStocks = self.var.retrieveAllStocks()
        try:
            asset = allStocks.loc[sid].asset
        except KeyError:
            raise Exception('Equity for sid: ' + str(sid) + ' not found.')

        return asset

    def symbol(self, symbol):
        allStocks = self.var.retrieveAllStocks()
        try:
            asset = allStocks[(allStocks.symbol == symbol.upper())].sort_values(by='start_date', ascending=False).asset.values[0]
        except IndexError:
            raise Exception('Equity for symbol: ' + symbol + ' not found.')

        return asset

    def symbols(self, *args):
        notFound = []
        assets = []
        for symbol in args:
            try:
                if isinstance(symbol, list):
                    for _symbol in symbol:
                        asset = self.symbol(_symbol)
                        assets.append(asset)

                else:
                    asset = self.symbol(symbol)
                    assets.append(asset)
            except:
                notFound.append(str(symbol))

        if notFound:
            raise Exception('Equity for symbol: ' + ','.join(notFound) + ' not found.')
        return assets

    def set_symbol_lookup_date(self, lookupDate):
        pass

    def set_slippage(self, slippage):
        pass

    def get_stock_watchlist(self):
        s = self.var.ips_api._framework_getStockWatchlist()
        if s is None or s == '':
            return []
        else:
            return (self.symbols)(*s.split(','))

    def set_commission(self, commission):
        if self.var._FRAMEWORK_IS_BACKTEST:
            param = {}
            if isinstance(commission, PerShare):
                param['type'] = 0
                param['perShare'] = commission.cost_per_share
                param['minPerTrade'] = commission.min_trade_cost
            else:
                if isinstance(commission, PerTrade):
                    param['type'] = 1
                    param['perTrade'] = commission.cost
                else:
                    if isinstance(commission, PerDollar):
                        param['type'] = 2
                        param['perDollar'] = commission.cost_per_dollar
            self.var.ips_api._framework_setCommission(self.var._FRAMEWORK_PORTFOLIOID, param)

    def send_tech_indicator(self, indicator):
        if self.var._FRAMEWORK_IS_LIVETRADE:
            self.var.ips_api._framework_sendTechIndicator(indicator)

    def send_IDA_complete(self):
        if self.var._FRAMEWORK_IS_LIVETRADE:
            self.var.ips_api._framework_sendIDAComplete()

    def EOD_latestdate(self):
        if self.var._FRAMEWORK_IS_BACKTEST:
            minute = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%H%M')
            if minute > '1600':
                return self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d')
            else:
                yestoday = self.var._FRAMEWORK_BT_CURRENTTIME + datetime.timedelta(days=(-1))
                return yestoday.strftime('%Y%m%d')
        else:
            return self.var.ips_api._framework_EODLatestDate()

    def genOrder(self, orderDict):
        order = Order()
        order.oid = str(orderDict['id'])
        status = orderDict['status'].lower() if orderDict['status'] is not None else ''
        if status == 'readytosend':
            order.status = 0
        else:
            if status == 'filled':
                order.status = 1
            else:
                if status == 'cancelled':
                    order.status = 2
                else:
                    if status == 'ignored':
                        order.status = 5
                    else:
                        order.status = 4
        order.amount = orderDict['amount']
        order.sid = self.sid(orderDict['stockId']) if orderDict['stockId'] is not None else None
        order.filled = orderDict['shares']
        order.Commission = orderDict['commission']
        return order

    def get_open_orders(self, sid=None, sub_portfolio_id=None):
        olist = []
        if self.var._FRAMEWORK_IS_LIVETRADE:
            if sid is not None:
                if isinstance(sid, Equity):
                    sid = sid.sid
            data = self.var.ips_api._framework_getOpenOrders(self.var._FRAMEWORK_PORTFOLIOID, sid, sub_portfolio_id)
            olist = json.loads(data)
        if sid is not None:
            orders = []
            for o in olist:
                orders.append(self.genOrder(o))

            return orders
        else:
            odict = {}
            for assetOrder in olist:
                orders = []
                assetOrders = assetOrder['orders']
                for o in assetOrders:
                    orders.append(self.genOrder(o))

                odict[assetOrder['sid']] = orders

            return odict

    def get_order(self, order, sub_portfolio_id=None):
        oid = None
        if isinstance(order, str):
            oid = order
        else:
            if isinstance(order, Order):
                oid = order.oid
            else:
                oid = str(order)
        data = self.var.ips_api._framework_getOrder(self.var._FRAMEWORK_PORTFOLIOID, oid, sub_portfolio_id)
        if data != '':
            return self.genOrder(json.loads(data))

    def schedule_function(self, func, date_rule=None, time_rule=None):
        if date_rule is None:
            date_rule = date_rules.every_day()
        else:
            if time_rule is None:
                time_rule = time_rules.every_minute()
            if date_rule.ruleType == 0:
                self.handle_time_rule(time_rule, self.var._framework_everyday_funcs, func)
            else:
                funcDict = {}
                if date_rule.ruleType == 1:
                    if date_rule.days_offset in self.var._framework_monthstart_funcs.keys():
                        funcDict = self.var._framework_monthstart_funcs[date_rule.days_offset]
                    else:
                        self.var._framework_monthstart_funcs[date_rule.days_offset] = funcDict
                elif date_rule.ruleType == 2:
                    if date_rule.days_offset in self.var._framework_monthend_funcs.keys():
                        funcDict = self.var._framework_monthend_funcs[date_rule.days_offset]
                    else:
                        self.var._framework_monthend_funcs[date_rule.days_offset] = funcDict
                elif date_rule.ruleType == 3:
                    if date_rule.days_offset in self.var._framework_weekstart_funcs.keys():
                        funcDict = self.var._framework_weekstart_funcs[date_rule.days_offset]
                    else:
                        self.var._framework_weekstart_funcs[date_rule.days_offset] = funcDict
                else:
                    if date_rule.days_offset in self.var._framework_weekend_funcs.keys():
                        funcDict = self.var._framework_weekend_funcs[date_rule.days_offset]
                    else:
                        self.var._framework_weekend_funcs[date_rule.days_offset] = funcDict
                    self.handle_time_rule(time_rule, funcDict, func)

    def handle_time_rule(self, time_rule, funcDict, func):
        if time_rule.ruleType == 0:
            key = 'every'
        else:
            if time_rule.ruleType == 1:
                key = 'o' + str(time_rule.minutes_offset)
            else:
                key = 'c' + str(-time_rule.minutes_offset)
        self.add_func(key, funcDict, func)

    def add_func(self, key, funcDict, func):
        funcs = []
        if key in funcDict.keys():
            funcs = funcDict[key]
        else:
            funcDict[key] = funcs
        if func not in funcs:
            funcs.append(func)

    def genParam(self, style):
        orderType = 'MKT'
        limitPrice = None
        stopPrice = None
        orderTime = None
        if isinstance(style, LimitOrder):
            orderType = 'LMT'
            limitPrice = style.limit_price
        else:
            if isinstance(style, StopOrder):
                orderType = 'STP'
                stopPrice = style.stop_price
            else:
                if isinstance(style, StopLimitOrder):
                    orderType = 'STP_LMT'
                    limitPrice = style.limit_price
                    stopPrice = style.stop_price
        if self.var._FRAMEWORK_IS_BACKTEST:
            orderTime = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M')
        return (
         orderType, limitPrice, stopPrice, orderTime)

    def order(self, asset, amount, style=MarketOrder('smart'), schedule_time=None, sub_portfolio_id=None, trade_threshhold=None):
        orderType, limitPrice, stopPrice, orderTime = self.genParam(style)
        return self.var.ips_api._framework_order(self.var._FRAMEWORK_PORTFOLIOID, asset, amount, orderType, limitPrice, stopPrice, style._exchange, schedule_time, orderTime, sub_portfolio_id, trade_threshhold)

    def order_value(self, asset, amount, style=MarketOrder('smart'), schedule_time=None, sub_portfolio_id=None, trade_threshhold=None):
        orderType, limitPrice, stopPrice, orderTime = self.genParam(style)
        return self.var.ips_api._framework_orderValue(self.var._FRAMEWORK_PORTFOLIOID, asset, amount, orderType, limitPrice, stopPrice, style._exchange, schedule_time, orderTime, sub_portfolio_id, trade_threshhold)

    def order_percent(self, asset, amount, style=MarketOrder('smart'), schedule_time=None, sub_portfolio_id=None, trade_threshhold=None):
        orderType, limitPrice, stopPrice, orderTime = self.genParam(style)
        return self.var.ips_api._framework_orderPercent(self.var._FRAMEWORK_PORTFOLIOID, asset, amount, orderType, limitPrice, stopPrice, style._exchange, schedule_time, orderTime, sub_portfolio_id, trade_threshhold)

    def order_target(self, asset, amount, style=MarketOrder('smart'), schedule_time=None, sub_portfolio_id=None, trade_threshhold=None):
        orderType, limitPrice, stopPrice, orderTime = self.genParam(style)
        return self.var.ips_api._framework_orderTarget(self.var._FRAMEWORK_PORTFOLIOID, asset, amount, orderType, limitPrice, stopPrice, style._exchange, schedule_time, orderTime, sub_portfolio_id, trade_threshhold)

    def order_target_value(self, asset, amount, style=MarketOrder('smart'), schedule_time=None, sub_portfolio_id=None, trade_threshhold=None):
        orderType, limitPrice, stopPrice, orderTime = self.genParam(style)
        return self.var.ips_api._framework_orderTargetValue(self.var._FRAMEWORK_PORTFOLIOID, asset, amount, orderType, limitPrice, stopPrice, style._exchange, schedule_time, orderTime, sub_portfolio_id, trade_threshhold)

    def order_target_percent(self, asset, amount, style=MarketOrder('smart'), schedule_time=None, sub_portfolio_id=None, trade_threshhold=None):
        orderType, limitPrice, stopPrice, orderTime = self.genParam(style)
        return self.var.ips_api._framework_orderTargetPercent(self.var._FRAMEWORK_PORTFOLIOID, asset, amount, orderType, limitPrice, stopPrice, style._exchange, schedule_time, orderTime, sub_portfolio_id, trade_threshhold)

    def set_target_portfolio(self, signals, exchange=None, schedule_time=None):
        return self.var.ips_api._framework_setTargetPortfolio(self.var._FRAMEWORK_PORTFOLIOID, signals, exchange, schedule_time, self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M') if self.var._FRAMEWORK_IS_BACKTEST else None)

    def record(self, *args, **kwargs):
        args = [
         iter(args)] * 2
        positionals = zip(*args)
        records = []
        for name, value in chain(positionals, iteritems(kwargs)):
            _dict = {}
            _dict['name'] = name
            _dict['value'] = value
            records.append(_dict)

        recordTime = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d') if self.var._FRAMEWORK_IS_BACKTEST else int((self.var._FRAMEWORK_BT_CURRENTTIME - datetime.datetime(1970, 1, 1, tzinfo=(pytz.timezone('UTC')))).total_seconds() * 1000)
        self.var.ips_api._framework_record(self.var._FRAMEWORK_PORTFOLIOID, recordTime, json.dumps(records))


if __name__ == '__main__':
    from strategycontainer.var import Var
    from strategycontainer.model import Context
    from strategycontainer.data import Data
    from strategycontainer.ips_api import IPSApi
    from strategycontainer.utils.calendar import Calendar
    from strategycontainer.utils.universe import Universe
    from strategycontainer.tsp.data.equity_market1indicator import USEquityMarket1Daily, USEquityMarket1Weekly
    import logging
    var = Var()
    var.log = logging.getLogger('IES')
    var.context = Context(var)
    var.data = Data(var)
    var.ips_api = IPSApi(var)
    var.api = API(var)
    universe = Universe(var)
    var._FRAMEWORK_PORTFOLIOID = -1
    var._FRAMEWORK_MARKETTYPE = 'US'
    var._TIMEZONE = pytz.timezone('US/Eastern')
    var._FRAMEWORK_IS_BACKTEST = True
    var._FRAMEWORK_IS_LIVETRADE = False
    var._FRAMEWORK_IS_DATAFETCHER = False
    var._FRAMEWORK_IS_TEST_STRATEGY = True
    var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY = False
    var._FRAMEWORK_REMOTEDEBUG = False
    var._FRAMEWORK_BT_CURRENTTIME = var._TIMEZONE.localize(datetime.datetime.strptime('201211042130', '%Y%m%d%H%M'))
    var._FRAMEWORK_BT_STARTDATE = '20000101'
    var._FRAMEWORK_BT_ENDDATE = '20190105'
    var._FRAMEWORK_IS_BACKTEST = True
    var._FRAMEWORK_IS_LIVETRADE = False
    var.cal = Calendar(var, '20000101', '30000101')
    s = datetime.datetime.now()
    df = var.data.history([Equity(100, '')], ['open', 'pe'], 5, '1d', adj_flag=False, start_date='2012-10-27', end_date='2012-11-04')
    print(df)
    print(datetime.datetime.now() - s)