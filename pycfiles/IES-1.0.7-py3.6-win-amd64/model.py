# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\model.py
# Compiled at: 2018-10-19 02:44:00
# Size of source mod 2**32: 11234 bytes
"""
@author: sharon
"""
import json, datetime, logging, sys
from strategycontainer.exception import PortfolioNotFoundException, PortfolioNotStartException

class Context:

    def __init__(self, var):
        self.var = var
        self.portfolio_cache = {}

    def clearPortfolioCache(self):
        self.portfolio_cache.clear()

    def getPortfolio(self, parent_portfolio_id, sub_portfolio_id):
        data = self.var.ips_api._framework_getPortfolio(parent_portfolio_id, sub_portfolio_id)
        _portfolioDict = json.loads(data)
        _portfolio = Portfolio()
        _portfolio.starting_cash = _portfolioDict['starting_cash']
        _portfolio.portfolio_value = _portfolioDict['portfolio_value']
        _portfolio.cash = _portfolioDict['cash']
        _portfolio.start_date = _portfolioDict['start_date']
        _portfolio.long_value = _portfolioDict['long_value']
        _portfolio.short_value = _portfolioDict['short_value']
        _portfolio.stock_value = _portfolioDict['stock_value']
        _portfolio.benchmark_cumreturn = _portfolioDict['benchmark_cumreturn']
        _portfolio.benchmark_annualreturn = _portfolioDict['benchmark_annualreturn']
        _portfolio.benchmark_CARG = _portfolioDict['benchmark_CARG']
        _portfolio.benchmark_maxdd = _portfolioDict['benchmark_maxdd']
        _portfolio.benchmark_sharpe = _portfolioDict['benchmark_sharpe']
        _portfolio.benchmark_volatility = _portfolioDict['benchmark_volatility']
        _portfolio.benchmark_sortino = _portfolioDict['benchmark_sortino']
        _portfolio.cumreturn = _portfolioDict['cumreturn']
        _portfolio.annualreturn = _portfolioDict['annualreturn']
        _portfolio.CARG = _portfolioDict['CARG']
        _portfolio.maxdd = _portfolioDict['maxdd']
        _portfolio.sharpe = _portfolioDict['sharpe']
        _portfolio.volatility = _portfolioDict['volatility']
        _portfolio.sortino = _portfolioDict['sortino']
        _portfolio.information_ratio = _portfolioDict['inforatio']
        _positionList = _portfolioDict['positions']
        for _positionDict in _positionList:
            asset = self.var.api.sid(_positionDict['sid'])
            position = Position(asset)
            position.amount = _positionDict['amount']
            position.cost_basis = _positionDict['cost_basis']
            position.market_price = _positionDict['market_price']
            position.last_sale_price = _positionDict['last_sale_price']
            _portfolio.positions[asset] = position

        return _portfolio

    @property
    def portfolio(self):
        if self.var._FRAMEWORK_PORTFOLIOID not in self.portfolio_cache.keys():
            self.portfolio_cache[self.var._FRAMEWORK_PORTFOLIOID] = self.getPortfolio(self.var._FRAMEWORK_PORTFOLIOID, None)
        return self.portfolio_cache[self.var._FRAMEWORK_PORTFOLIOID]

    def subportfolio(self, sub_portfolio_id):
        if sub_portfolio_id not in self.portfolio_cache.keys():
            self.portfolio_cache[sub_portfolio_id] = self.getPortfolio(self.var._FRAMEWORK_PORTFOLIOID, sub_portfolio_id)
        return self.portfolio_cache[sub_portfolio_id]


class Portfolio(object):

    def __init__(self):
        self.starting_cash = 0.0
        self.portfolio_value = 0.0
        self.cash = 0.0
        self.positions = Positions()
        self.start_date = None

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return 'Portfolio({0})'.format(self.__dict__)


class Position(object):

    def __init__(self, sid):
        self.sid = sid
        self.amount = 0
        self.cost_basis = 0.0
        self.last_sale_price = 0.0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return 'Position({0})'.format(self.__dict__)


class Positions(dict):
    pass


class Order:

    def __eq__(self, other):
        if other is None:
            return False
        else:
            if not isinstance(other, Order):
                return False
            return self.oid == other.oid

    def __hash__(self):
        return self.oid.__hash__()


class Equity:

    def __init__(self, sid, symbol, start_date=None, end_date=None, sec_type=None):
        self.sid = sid
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.sec_type = sec_type

    def __eq__(self, other):
        if other is None:
            return False
        else:
            if not isinstance(other, Equity):
                return False
            return self.sid == other.sid

    def __ne__(self, other):
        if other is None:
            return True
        else:
            return self.sid != other.sid

    def __lt__(self, other):
        return self.symbol < other.symbol

    def __le__(self, other):
        return self.symbol <= other.symbol

    def __gt__(self, other):
        return self.symbol > other.symbol

    def __ge__(self, other):
        return self.symbol >= other.symbol

    def __hash__(self):
        return self.sid.__hash__()

    def __repr__(self):
        return 'Equity(' + str(self.sid) + ' [' + self.symbol + '])'


class DateRule:

    def __init__(self, ruleType, n):
        self.ruleType = ruleType
        self.days_offset = n


class date_rules(object):

    @staticmethod
    def every_day():
        return DateRule(0, 0)

    @staticmethod
    def month_start(days_offset=0):
        return DateRule(1, days_offset)

    @staticmethod
    def month_end(days_offset=0):
        return DateRule(2, days_offset)

    @staticmethod
    def week_start(days_offset=0):
        return DateRule(3, days_offset)

    @staticmethod
    def week_end(days_offset=0):
        return DateRule(4, days_offset)


class TimeRule:

    def __init__(self, ruleType, n):
        self.ruleType = ruleType
        self.minutes_offset = n


class time_rules(object):

    @staticmethod
    def every_minute():
        return TimeRule(0, -9999)

    @staticmethod
    def market_open(minutes):
        return TimeRule(1, minutes)

    @staticmethod
    def market_close(minutes):
        return TimeRule(2, minutes)


class MarketOrder:
    __doc__ = '\n    Class encapsulating an order to be placed at the current market price.\n    '

    def __init__(self, exchange=None):
        self._exchange = exchange


class LimitOrder:
    __doc__ = '\n    Execution style representing an order to be executed at a price equal to or\n    better than a specified limit price.\n    '

    def __init__(self, limit_price, exchange=None):
        """
        Store the given price.
        """
        self.limit_price = limit_price
        self._exchange = exchange


class StopOrder:
    __doc__ = '\n    Execution style representing an order to be placed once the market price\n    reaches a specified stop price.\n    '

    def __init__(self, stop_price, exchange=None):
        """
        Store the given price.
        """
        self.stop_price = stop_price
        self._exchange = exchange


class StopLimitOrder:
    __doc__ = '\n    Execution style representing a limit order to be placed with a specified\n    limit price once the market reaches a specified stop price.\n    '

    def __init__(self, limit_price, stop_price, exchange=None):
        """
        Store the given prices
        """
        self.limit_price = limit_price
        self.stop_price = stop_price
        self._exchange = exchange


class IESLogHandler(logging.Handler):

    def __init__(self, var):
        logging.Handler.__init__(self)
        self.var = var
        self.level = logging.DEBUG
        self.stopSend = False

    def emit(self, record):
        if self.stopSend:
            return
        else:
            log = {}
            log['line'] = record.lineno
            log['class'] = record.funcName
            log['content'] = self.format(record)
            level = -1
            if record.levelno == logging.DEBUG:
                level = 0
            else:
                if record.levelno == logging.INFO:
                    level = 1
                else:
                    if record.levelno == logging.WARN:
                        level = 2
                    else:
                        if record.levelno == logging.ERROR:
                            level = 3
                        else:
                            log['level'] = level
                            if self.var.IES_DEBUG:
                                if level == 3 or level == -1:
                                    sys.stderr.write(log['content'] + '\n')
                            if self.var._FRAMEWORK_IS_BACKTEST:
                                if level == -1:
                                    log['time'] = datetime.datetime.now(self.var._TIMEZONE).strftime('%Y%m%d%H%M%S')
                                else:
                                    try:
                                        log['time'] = self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%Y%m%d%H%M')
                                    except:
                                        log['time'] = datetime.datetime.now(self.var._TIMEZONE).strftime('%Y%m%d%H%M%S')

                        try:
                            if self.var._FRAMEWORK_IS_BACKTEST or self.var._FRAMEWORK_IS_LIVETRADE:
                                self.var.ips_api._framework_log(self.var._FRAMEWORK_PORTFOLIOID, json.dumps([log]))
                        except PortfolioNotFoundException as e:
                            self.stopSend = True
                            raise e
                        except PortfolioNotStartException as e:
                            self.stopSend = True
                            raise e
                        except Exception as msg:
                            print(str(msg))

    def flush(self):
        self.stopSend = True


if __name__ == '__main__':
    pass