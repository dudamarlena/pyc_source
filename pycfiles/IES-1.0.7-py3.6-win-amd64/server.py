# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\server.py
# Compiled at: 2018-12-18 04:57:22
# Size of source mod 2**32: 33663 bytes
"""
@author: sharon
"""
import threading, web, calendar, datetime, logging, traceback, sys, json, os
from strategycontainer.var import Var
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from strategycontainer import slippage, commission
from strategycontainer.model import date_rules, time_rules, Context, MarketOrder, LimitOrder, StopOrder, StopLimitOrder, IESLogHandler
from strategycontainer.data import Data
from strategycontainer.api import API
from strategycontainer.ips_api import IPSApi
from strategycontainer.exception import PortfolioNotFoundException, PortfolioNotStartException, RestartException, ContinueException
from strategycontainer.jsonencoder import ObjectEncoder
from strategycontainer.tsp.data import USEquityPricing, AStockPricing, USEquityFundamental, AStockFundamental, USEquityMarket1Daily, USEquityMarket1Weekly, AStockIndicator, USEquityFundamentalMetrics
from strategycontainer.tsp.loaders import USEquityPricingLoader, AStockPricingLoader, USEquityFundamentalLoader, AStockFundamentalLoader, USEquityMarket1DailyLoader, USEquityMarket1PeriodLoader, AStockIndicatorLoader, USEquityIndicatorLoader
from strategycontainer.tsp import TSP, SimplePipelineEngine
from strategycontainer.utils.calendar import Calendar
from strategycontainer.utils.cache import ExpiringCache
from strategycontainer.utils.universe import Universe
from strategycontainer.utils.pandas_utils import clear_dataframe_indexer_caches
from strategycontainer.tsp.factor_out_cache import factorOutCache
import pandas as pd

class _framework_BacktestNoopThread(threading.Thread):

    def __init__(self, var):
        super(_framework_BacktestNoopThread, self).__init__()
        self.stopped = False
        self.event = threading.Event()
        self.var = var

    def stop(self):
        self.stopped = True

    def notify(self):
        self.event.set()

    def run(self):
        while not self.stopped:
            try:
                try:
                    self.var.ips_api._framework_backtestNoop()
                except Exception as msg:
                    print(str(msg))

            finally:
                self.event.wait(60)


class _framework_BackTest:

    def __init__(self, ies_server):
        self.ies_server = ies_server
        self.var = self.ies_server.var
        self.noopThread = _framework_BacktestNoopThread(self.var)
        self.needInit = True

    def doBacktest(self, startDate, endDate):
        days_in_month = calendar.monthrange(int(endDate[0:4]), int(endDate[4:6]))[1]
        tradeCalendarDf = self.var.cal.slice(startDate[0:6] + '01', endDate[0:6] + str(days_in_month))
        tradeCalendar = tradeCalendarDf[((tradeCalendarDf.date >= startDate) & (tradeCalendarDf.date <= endDate))]['date']
        hasHandleDataFunc = hasattr(self.var.strategyModule, 'handle_data')
        lastMonthEndDay = '00000000'
        lastWeekEndDay = '00000000'
        lastday = ''
        for tradeDay in tradeCalendar:
            self.var._FRAMEWORK_BT_CURRENTTIME = self.var._TIMEZONE.localize(datetime.datetime.strptime(tradeDay + '0000', '%Y%m%d%H%M'))
            self.var.ips_api._framework_startOfTradeDay(self.var._FRAMEWORK_PORTFOLIOID, tradeDay, lastday)
            if self.needInit:
                if hasattr(self.var.strategyModule, 'initialize'):
                    self.var.strategyModule.initialize(self.var.context)
                if hasattr(self.var.strategyModule, 'start'):
                    self.var.strategyModule.start(self.var.context)
                self.var.context.clearPortfolioCache()
                self.needInit = False
            if tradeDay > lastMonthEndDay:
                self.var.this_monthstart_funcs.clear()
                self.var.this_monthend_funcs.clear()
                days_in_month = calendar.monthrange(self.var._FRAMEWORK_BT_CURRENTTIME.year, self.var._FRAMEWORK_BT_CURRENTTIME.month)[1]
                firstDay = datetime.datetime(self.var._FRAMEWORK_BT_CURRENTTIME.year, self.var._FRAMEWORK_BT_CURRENTTIME.month, 1)
                lastDay = datetime.datetime(self.var._FRAMEWORK_BT_CURRENTTIME.year, self.var._FRAMEWORK_BT_CURRENTTIME.month, days_in_month)
                tmpDf = tradeCalendarDf[((tradeCalendarDf.date >= firstDay.strftime('%Y%m%d')) & (tradeCalendarDf.date <= lastDay.strftime('%Y%m%d')))]
                self.var.this_month_tradedays = tmpDf['date']
                self.var.this_month_halfdays = tmpDf[(tmpDf.halfday == True)]['date']
                for offset in self.var._framework_monthstart_funcs.keys():
                    if offset < len(self.var.this_month_tradedays):
                        self.var.this_monthstart_funcs[self.var.this_month_tradedays.iloc[offset]] = self.var._framework_monthstart_funcs[offset]

                for offset in self.var._framework_monthend_funcs.keys():
                    if offset < len(self.var.this_month_tradedays):
                        self.var.this_monthend_funcs[self.var.this_month_tradedays.iloc[(len(self.var.this_month_tradedays) - offset - 1)]] = self.var._framework_monthend_funcs[offset]

                lastMonthEndDay = lastDay.strftime('%Y%m%d')
            if tradeDay > lastWeekEndDay:
                self.var.this_weekstart_funcs.clear()
                self.var.this_weekend_funcs.clear()
                firstDay = self.var._FRAMEWORK_BT_CURRENTTIME - datetime.timedelta(days=(self.var._FRAMEWORK_BT_CURRENTTIME.weekday()))
                lastDay = self.var._FRAMEWORK_BT_CURRENTTIME + datetime.timedelta(days=(6 - self.var._FRAMEWORK_BT_CURRENTTIME.weekday()))
                tmpDf = tradeCalendarDf[((tradeCalendarDf.date >= firstDay.strftime('%Y%m%d')) & (tradeCalendarDf.date <= lastDay.strftime('%Y%m%d')))]
                week_tradedays = tmpDf['date']
                for offset in self.var._framework_weekstart_funcs.keys():
                    if offset < len(week_tradedays):
                        self.var.this_weekstart_funcs[week_tradedays.iloc[offset]] = self.var._framework_weekstart_funcs[offset]

                for offset in self.var._framework_weekend_funcs.keys():
                    if offset < len(week_tradedays):
                        self.var.this_weekend_funcs[week_tradedays.iloc[(len(week_tradedays) - offset - 1)]] = self.var._framework_weekend_funcs[offset]

                lastWeekEndDay = lastDay.strftime('%Y%m%d')
            self.var.today_minute_funcs.clear()
            halfDay = tradeDay in self.var.this_month_halfdays.values
            if tradeDay in self.var.this_month_tradedays.values:
                self.ies_server.gen_today_funcs(self.var._framework_everyday_funcs, halfDay)
            if tradeDay in self.var.this_monthstart_funcs.keys():
                self.ies_server.gen_today_funcs(self.var.this_monthstart_funcs[tradeDay], halfDay)
            if tradeDay in self.var.this_monthend_funcs.keys():
                self.ies_server.gen_today_funcs(self.var.this_monthend_funcs[tradeDay], halfDay)
            if tradeDay in self.var.this_weekstart_funcs.keys():
                self.ies_server.gen_today_funcs(self.var.this_weekstart_funcs[tradeDay], halfDay)
            if tradeDay in self.var.this_weekend_funcs.keys():
                self.ies_server.gen_today_funcs(self.var.this_weekend_funcs[tradeDay], halfDay)
            self.everyMinute = hasHandleDataFunc
            self.barsOfDay = []
            self.everyMinute = self.everyMinute or 'every' in self.var.today_minute_funcs.keys()
            for minute in self.var.today_minute_funcs.keys():
                if 'every' != minute:
                    self.barsOfDay.append(minute)

            tradingBars = []
            if self.everyMinute:
                _tmpdt = datetime.datetime(2000, 1, 1, 9, 30)
                closeTime = '1600'
                if self.var._FRAMEWORK_MARKETTYPE == 'CN':
                    closeTime = '1500'
                if halfDay:
                    closeTime = '1300'
                while _tmpdt.strftime('%H%M') <= closeTime:
                    if self.var._FRAMEWORK_MARKETTYPE == 'US':
                        tradingBars.append(_tmpdt.strftime('%H%M'))
                    else:
                        if _tmpdt.strftime('%H%M') >= '0930' and _tmpdt.strftime('%H%M') <= '1130' or _tmpdt.strftime('%H%M') >= '1300' and _tmpdt.strftime('%H%M') <= '1500':
                            tradingBars.append(_tmpdt.strftime('%H%M'))
                    _tmpdt = _tmpdt + datetime.timedelta(minutes=1)

            self.barsOfDay = list(set(self.barsOfDay + tradingBars))
            self.barsOfDay.sort()
            for barMinute in self.barsOfDay:
                self.var._FRAMEWORK_BT_CURRENTTIME = self.var._TIMEZONE.localize(datetime.datetime.strptime(tradeDay + barMinute, '%Y%m%d%H%M'))
                self.ies_server.execBar(barMinute)

            self.var._FRAMEWORK_BT_LASTTRADEDAY = self.var._FRAMEWORK_BT_CURRENTTIME
            lastday = tradeDay

        self.var.ips_api._framework_startOfTradeDay(self.var._FRAMEWORK_PORTFOLIOID, '', lastday)

    def start(self):
        try:
            try:
                if not self.var.IES_DEBUG:
                    from qdb import disable
                else:
                    self.noopThread.start()
                    if self.var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY:
                        self.doBacktest(self.var._FRAMEWORK_TRAIN_STARTDATE, self.var._FRAMEWORK_TRAIN_ENDDATE)
                        self.var._FRAMEWORK_CURRENT_PHASE = 'test'
                    self.doBacktest(self.var._FRAMEWORK_BT_STARTDATE, self.var._FRAMEWORK_BT_ENDDATE)
                    self.var.log.critical('Backtest Complete')
                    logging.shutdown()
                    if self.var._FRAMEWORK_REMOTEDEBUG:
                        disable()
                self.var.ips_api._framework_endOfBacktest(self.var._FRAMEWORK_PORTFOLIOID)
            except:
                msg = self.ies_server.traceMsg()
                self.var.log.critical(msg)
                logging.shutdown()
                self.var.ips_api._framework_cancelBacktest(self.var._FRAMEWORK_PORTFOLIOID)

        finally:
            if self.var.IES_DEBUG:
                self.noopThread.stop()
                self.noopThread.notify()


class IESServer(object):

    def __init__(self, var=None):
        self.var = var if var is not None else Var()
        self.var.context = Context(self.var)
        self.var.data = Data(self.var)
        self.var.ips_api = IPSApi(self.var)
        self.var.api = API(self.var)
        _framework_executors = {'default':ThreadPoolExecutor(10), 
         'processpool':ProcessPoolExecutor(3)}
        self._framework_scheduler = BackgroundScheduler(executors=_framework_executors)
        self.usequityPricing_loader = USEquityPricingLoader(self.var)
        self.usequityfundamental_loader = USEquityFundamentalLoader(self.var)
        self.usequityMarket1daily_loader = USEquityMarket1DailyLoader(self.var)
        self.usequityMarket1weekly_loader = USEquityMarket1PeriodLoader(self.var)
        self.astockPricing_loader = AStockPricingLoader(self.var)
        self.astockIndicator_loader = AStockIndicatorLoader(self.var)
        self.astockFundamental_loader = AStockFundamentalLoader(self.var)
        self.usequityIndicator_loader = USEquityIndicatorLoader(self.var)
        self.tsps = {}
        self.tsp_cache = ExpiringCache(cleanup=clear_dataframe_indexer_caches)
        self.universe = Universe(self.var)

    def execScheduleFunc(self, func):
        func(self.var.context, self.var.data)

    def execHandleData(self):
        if hasattr(self.var.strategyModule, 'handle_data'):
            self.var.strategyModule.handle_data(self.var.context, self.var.data)

    def execBar(self, barMinute):
        today = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d')
        halfDay = today in self.var.this_month_halfdays.values
        if self.var._FRAMEWORK_MARKETTYPE == 'US':
            closeTime = '1300' if halfDay else '1600'
        else:
            closeTime = '1500'
        if 'every' in self.var.today_minute_funcs.keys():
            needDo = False
            if self.var._FRAMEWORK_MARKETTYPE == 'US':
                if barMinute >= '0930':
                    if barMinute <= closeTime:
                        needDo = True
            else:
                if barMinute >= '0930' and barMinute <= '1130' or barMinute >= '1300' and barMinute <= closeTime:
                    needDo = True
                if needDo:
                    for func in self.var.today_minute_funcs['every']:
                        self.execScheduleFunc(func)

        if barMinute in self.var.today_minute_funcs.keys():
            for func in self.var.today_minute_funcs[barMinute]:
                self.execScheduleFunc(func)

        if today in self.var.this_month_tradedays.values:
            if self.var._FRAMEWORK_MARKETTYPE == 'US':
                if barMinute >= '0930':
                    if barMinute <= closeTime:
                        self.execHandleData()
            elif barMinute >= '0930' and barMinute <= '1130' or barMinute >= '1300' and barMinute <= closeTime:
                self.execHandleData()
        self.var.context.clearPortfolioCache()

    def live_schedule_task(self, task_type):
        need_exit = False
        try:
            msg = ''
            try:
                if task_type == 1:
                    self.gen_month_funcs()
                else:
                    if task_type == 2:
                        self.gen_week_funcs()
                    else:
                        if task_type == 3:
                            self.gen_today_minute_funcs()
                        else:
                            self.var._FRAMEWORK_BT_CURRENTTIME = datetime.datetime.now(self.var._TIMEZONE)
                            self.execBar(self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%H%M'))
            except (PortfolioNotFoundException, PortfolioNotStartException, RestartException):
                need_exit = True
                msg = self.traceMsg()
            except ContinueException:
                msg = self.traceMsg()
            except Exception:
                if self.var._FRAMEWORK_EXCEPTIONHANDLE == 'RESTART':
                    need_exit = True
                msg = self.traceMsg()

            if msg != '':
                self.var.log.critical(msg)
                self.mailToDeveloper(msg)
        finally:
            if need_exit:
                os._exit(0)

    def gen_month_funcs_wrapper(self):
        self.live_schedule_task(1)

    def gen_month_funcs(self):
        self.var.this_monthstart_funcs.clear()
        self.var.this_monthend_funcs.clear()
        today = datetime.datetime.now(self.var._TIMEZONE)
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        firstDay = datetime.datetime(today.year, today.month, 1)
        lastDay = datetime.datetime(today.year, today.month, days_in_month)
        self.var.cal.append(firstDay.strftime('%Y%m%d'), lastDay.strftime('%Y%m%d'))
        self.var.this_month_tradedays = self.var.cal.slice(firstDay.strftime('%Y%m%d'), lastDay.strftime('%Y%m%d'))
        self.var.this_month_halfdays = self.var.this_month_tradedays[(self.var.this_month_tradedays.halfday == True)]
        self.var.this_month_tradedays = self.var.this_month_tradedays['date']
        for offset in self.var._framework_monthstart_funcs.keys():
            if offset < len(self.var.this_month_tradedays):
                self.var.this_monthstart_funcs[self.var.this_month_tradedays.iloc[offset]] = self.var._framework_monthstart_funcs[offset]

        for offset in self.var._framework_monthend_funcs.keys():
            if offset < len(self.var.this_month_tradedays):
                self.var.this_monthend_funcs[self.var.this_month_tradedays.iloc[(len(self.var.this_month_tradedays) - offset - 1)]] = self.var._framework_monthend_funcs[offset]

    def gen_week_funcs_wrapper(self):
        self.live_schedule_task(2)

    def gen_week_funcs(self):
        self.var.this_weekstart_funcs.clear()
        self.var.this_weekend_funcs.clear()
        today = datetime.datetime.now(self.var._TIMEZONE)
        firstDay = today - datetime.timedelta(days=(today.weekday()))
        lastDay = today + datetime.timedelta(days=(6 - today.weekday()))
        self.var.cal.append(firstDay.strftime('%Y%m%d'), lastDay.strftime('%Y%m%d'))
        week_tradedays = self.var.cal.slice(firstDay.strftime('%Y%m%d'), lastDay.strftime('%Y%m%d'))['date']
        for offset in self.var._framework_weekstart_funcs.keys():
            if offset < len(week_tradedays):
                self.var.this_weekstart_funcs[week_tradedays.iloc[offset]] = self.var._framework_weekstart_funcs[offset]

        for offset in self.var._framework_weekend_funcs.keys():
            if offset < len(week_tradedays):
                self.var.this_weekend_funcs[week_tradedays.iloc[(len(week_tradedays) - offset - 1)]] = self.var._framework_weekend_funcs[offset]

    def gen_today_minute_funcs_wrapper(self):
        self.live_schedule_task(3)

    def gen_today_minute_funcs(self):
        self.var.today_minute_funcs.clear()
        today = datetime.datetime.now(self.var._TIMEZONE).strftime('%Y%m%d')
        halfDay = today in self.var.this_month_halfdays.values
        if today in self.var.this_month_tradedays.values:
            self.gen_today_funcs(self.var._framework_everyday_funcs, halfDay)
        if today in self.var.this_monthstart_funcs.keys():
            self.gen_today_funcs(self.var.this_monthstart_funcs[today], halfDay)
        if today in self.var.this_monthend_funcs.keys():
            self.gen_today_funcs(self.var.this_monthend_funcs[today], halfDay)
        if today in self.var.this_weekstart_funcs.keys():
            self.gen_today_funcs(self.var.this_weekstart_funcs[today], halfDay)
        if today in self.var.this_weekend_funcs.keys():
            self.gen_today_funcs(self.var.this_weekend_funcs[today], halfDay)

    def gen_today_funcs(self, funcDict, halfDay):
        for key, funcList in funcDict.items():
            minute = ''
            if key[0] == 'o':
                dt = datetime.datetime(2000, 1, 1, 9, 30)
                dt = dt + datetime.timedelta(minutes=(int(key[1:])))
                minute = dt.strftime('%H%M')
            else:
                if key[0] == 'c':
                    if self.var._FRAMEWORK_MARKETTYPE == 'US':
                        dt = datetime.datetime(2000, 1, 1, 16, 0)
                        if halfDay:
                            dt = datetime.datetime(2000, 1, 1, 13, 0)
                    else:
                        dt = datetime.datetime(2000, 1, 1, 15, 0)
                    dt = dt + datetime.timedelta(minutes=(int(key[1:])))
                    minute = dt.strftime('%H%M')
                else:
                    if key[0] == 'every':
                        minute = 'every'
            self.add_func(minute, funcList)

    def add_func(self, key, funcList):
        funcs = []
        if key in self.var.today_minute_funcs.keys():
            funcs = self.var.today_minute_funcs[key]
        else:
            self.var.today_minute_funcs[key] = funcs
        funcs.extend(funcList)

    def _framework_livetrade(self):
        self.live_schedule_task(4)

    def elasticLog(self, log):
        try:
            self.var.ips_api._framework_elasticLog(log)
        except:
            msg = self.traceMsg()
            self.var.log.critical(msg)

    def mailToDeveloper(self, content):
        try:
            self.var.ips_api._framework_mailToDeveloper(content)
        except Exception:
            self.elasticLog(content)

    def traceMsg(self, _filter=False):
        msg = []
        msg.append('Exception occured in IES Runtime')
        info = sys.exc_info()
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            if not _filter or 'StrategyCode.py' in file:
                if 'StrategyCode.py' in file:
                    msg.append('File "Strategy Source Code", line ' + str(lineno) + ', in ' + function)
                else:
                    msg.append('File ' + file + ', line ' + str(lineno) + ', in ' + function)
                msg.append('    ' + text)

        msg.append(str(info[0]) + ' ' + str(info[1]))
        return '\n'.join(msg)

    def repr_(self, obj):
        try:
            return json.dumps(obj, cls=ObjectEncoder)
        except:
            return self.traceMsg()

    def skip_(self, path):
        try:
            if 'StrategyCode.py' in path:
                return False
            else:
                return True
        except:
            return True

    def choose_loader(self, column):
        if self.var._FRAMEWORK_MARKETTYPE == 'US':
            if column in USEquityPricing.columns:
                return self.usequityPricing_loader
            else:
                if column in USEquityFundamental.columns:
                    return self.usequityfundamental_loader
                if column in USEquityMarket1Daily.columns:
                    return self.usequityMarket1daily_loader
                if column in USEquityMarket1Weekly.columns:
                    return self.usequityMarket1weekly_loader
            if column in USEquityFundamentalMetrics.columns:
                return self.usequityIndicator_loader
        else:
            if column in AStockPricing.columns:
                return self.astockPricing_loader
        if column in AStockFundamental.columns:
            return self.astockFundamental_loader
        if column in AStockIndicator.columns:
            return self.astockIndicator_loader
        raise ValueError('No PipelineLoader registered for column %s.' % column)

    def init_TSP(self, universe, columns, name, screen=None, chunks=100):
        if len(universe) == 0:
            raise Exception("Universe of TSP can't be empty.")
        else:
            tsp = TSP(universe, columns, screen, self.var)
            if chunks < 1:
                chunks = 1
            else:
                if chunks > 500:
                    chunks = 500
                else:
                    chunks = int(chunks)
        if name in self.tsps.keys():
            self.tsp_cache.set(name, None, pd.Timestamp('19000101'))
            existTsp, _ = self.tsps[name]
            factorOutCache.remove(existTsp)
        self.tsps[name] = (
         tsp, chunks)
        return tsp

    def compute_TSP(self, name):
        try:
            tsp, chunks = self.tsps[name]
            today = pd.Timestamp(self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y-%m-%d'))
            try:
                tsp_data = self.tsp_cache.get(name, today)
            except KeyError:
                if self.var._FRAMEWORK_IS_BACKTEST:
                    if not self.var._FRAMEWORK_RUNNING_NOTEBOOK:
                        all_sessions = self.var.cal.all_sessions
                        start_date_loc = all_sessions.get_loc(today)
                        end_session = pd.Timestamp(self.var._FRAMEWORK_BT_ENDDATE)
                        end_loc = min(start_date_loc + chunks - 1, self.var.cal.get_first_idx(end_session))
                        end_session = all_sessions[end_loc]
                        tsp_data = self.engine.run_pipeline(tsp, today, end_session)
                        self.tsp_cache.set(name, tsp_data, end_session)
                else:
                    tsp_data = self.engine.run_pipeline(tsp, today, today)
                    self.tsp_cache.set(name, tsp_data, today)

            try:
                return tsp_data.loc[today]
            except KeyError:
                return pd.DataFrame(index=[], columns=(tsp_data.columns))

        except Exception as e:
            msg = self.traceMsg()
            self.var.log.critical(msg)
            raise e

    def run_TSP(self, tsp, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        idx = self.var.cal.get_first_ge_idx(start_date)
        start_date = self.var.cal[idx]
        end_date = pd.Timestamp(end_date)
        idx = self.var.cal.get_first_idx(end_date)
        end_date = self.var.cal[idx]
        return self.engine.run_pipeline(tsp, start_date, end_date)

    def startServer(self):
        try:
            self.var.log = logging.getLogger('IES')
            logHandler = IESLogHandler(self.var)
            logHandler.setFormatter(logging.Formatter('%(message)s'))
            self.var.log.addHandler(logHandler)
            self.var.log.setLevel(logging.DEBUG)
            if not self.var.IES_DEBUG:
                from qdb import set_trace, RemoteCommandManager
            if self.var._FRAMEWORK_IS_BACKTEST or self.var._FRAMEWORK_IS_LIVETRADE:
                if not self.var.IES_DEBUG:
                    self.var.ips_api._framework_getStrategyCode(self.var._FRAMEWORK_PORTFOLIOID)
                else:
                    if self.var._FRAMEWORK_IS_BACKTEST:
                        if self.var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY:
                            self.var._FRAMEWORK_BT_CURRENTTIME = self.var._TIMEZONE.localize(datetime.datetime.strptime(self.var._FRAMEWORK_TRAIN_STARTDATE + '0000', '%Y%m%d%H%M'))
                        else:
                            self.var._FRAMEWORK_BT_CURRENTTIME = self.var._TIMEZONE.localize(datetime.datetime.strptime(self.var._FRAMEWORK_BT_STARTDATE + '0000', '%Y%m%d%H%M'))
                    else:
                        if self.var._FRAMEWORK_IS_LIVETRADE:
                            self.var._FRAMEWORK_BT_CURRENTTIME = datetime.datetime.now(self.var._TIMEZONE)
                        self.var.strategyModule = __import__('strategy.StrategyCode', fromlist=['strategy'])
                        thedict = {'set_benchmark':self.var.api.set_benchmark,  'sid':self.var.api.sid,  'symbol':self.var.api.symbol,  'symbols':self.var.api.symbols,  'set_symbol_lookup_date':self.var.api.set_symbol_lookup_date,  'set_slippage':self.var.api.set_slippage,  'set_commission':self.var.api.set_commission, 
                         'get_open_orders':self.var.api.get_open_orders,  'get_order':self.var.api.get_order,  'schedule_function':self.var.api.schedule_function,  'order':self.var.api.order, 
                         'order_value':self.var.api.order_value,  'order_percent':self.var.api.order_percent,  'order_target':self.var.api.order_target,  'order_target_value':self.var.api.order_target_value,  'order_target_percent':self.var.api.order_target_percent, 
                         'set_target_portfolio':self.var.api.set_target_portfolio,  'record':self.var.api.record,  'set_adjusted_price':self.var.api.set_adjusted_price,  'date_rules':date_rules, 
                         'time_rules':time_rules,  'slippage':slippage,  'commission':commission,  'send_ida_indicator':self.var.api.send_tech_indicator,  'get_stock_watchlist':self.var.api.get_stock_watchlist,  'data':self.var.data,  'context':self.var.context,  'MarketOrder':MarketOrder, 
                         'LimitOrder':LimitOrder,  'StopOrder':StopOrder,  'StopLimitOrder':StopLimitOrder,  'log':self.var.log,  'save_data':self.var.api.save_data,  'load_data':self.var.api.load_data,  'init_TSP':self.init_TSP,  'compute_TSP':self.compute_TSP,  'run_TSP':self.run_TSP,  'create_subportfolio':self.var.api.create_subportfolio, 
                         'send_ida_complete':self.var.api.send_IDA_complete,  'get_EOD_latestdate':self.var.api.EOD_latestdate,  'Universe':self.universe,  'get_backtest_days':self.var.api.get_backtest_days,  'get_trade_calendar':self.var.api.get_trade_calendar,  'RestartException':RestartException, 
                         'ContinueException':ContinueException}
                        self.var.strategyModule.__dict__.update(thedict)
                        if self.var._FRAMEWORK_IS_BACKTEST:
                            days_in_month = calendar.monthrange(int(self.var._FRAMEWORK_BT_ENDDATE[0:4]), int(self.var._FRAMEWORK_BT_ENDDATE[4:6]))[1]
                            self.var.cal = Calendar(self.var, '20000101', self.var._FRAMEWORK_BT_ENDDATE[0:6] + str(days_in_month))
                    if self.var._FRAMEWORK_IS_LIVETRADE:
                        self.var.cal = Calendar(self.var, '20000101', '30000101')
                self.engine = SimplePipelineEngine(self.choose_loader, self.var.cal, None)
            if self.var._FRAMEWORK_IS_BACKTEST:
                if self.var._FRAMEWORK_REMOTEDEBUG:
                    self.var.ips_api._framework_readyToDebug()
                    set_trace(stop=True,
                      uuid=(str(self.var._FRAMEWORK_PORTFOLIOID)),
                      host=(self.var._FRAMEWORK_DEBUGSERVER),
                      port=(self.var._FRAMEWORK_TRACEPORT),
                      cmd_manager=(RemoteCommandManager()),
                      redirect_output=False,
                      repr_fn=(self.repr_),
                      skip_fn=(self.skip_))
                bt = _framework_BackTest(self)
                bt.start()
            if self.var._FRAMEWORK_IS_LIVETRADE:
                if hasattr(self.var.strategyModule, 'initialize'):
                    self.var.strategyModule.initialize(self.var.context)
                if hasattr(self.var.strategyModule, 'start'):
                    self.var.strategyModule.start(self.var.context)
                self.var.context.clearPortfolioCache()
                self.gen_month_funcs()
                self.gen_week_funcs()
                self.gen_today_minute_funcs()
                self._framework_scheduler.add_job((self._framework_livetrade), 'cron', id='_framework_livetrade', day_of_week='mon-fri', hour='1-23', minute='*/1', timezone=(self.var._TIMEZONE))
                self._framework_scheduler.add_job((self.gen_month_funcs_wrapper), 'cron', id='gen_month_funcs_wrapper', month='1-12', day=1, hour=0, minute=1, timezone=(self.var._TIMEZONE))
                self._framework_scheduler.add_job((self.gen_week_funcs_wrapper), 'cron', id='gen_week_funcs_wrapper', month='1-12', day_of_week=0, hour=0, minute=3, timezone=(self.var._TIMEZONE))
                self._framework_scheduler.add_job((self.gen_today_minute_funcs_wrapper), 'cron', id='gen_today_minute_funcs_wrapper', day_of_week='mon-fri', hour=0, minute=6, timezone=(self.var._TIMEZONE))
                self._framework_scheduler.start()
                self.mailToDeveloper('live trade start')
                urls = ()
                web.config.debug = False
                app = web.application(urls, globals())
                app.run()
        except:
            msg = self.traceMsg()
            self.var.log.critical(msg)
            logging.shutdown()
            if self.var._FRAMEWORK_IS_BACKTEST:
                self.var.ips_api._framework_cancelBacktest(self.var._FRAMEWORK_PORTFOLIOID)
            if self.var._FRAMEWORK_IS_LIVETRADE:
                self.mailToDeveloper(msg)


if __name__ == '__main__':
    ies_server = IESServer()
    ies_server.startServer()