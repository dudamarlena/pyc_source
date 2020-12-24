# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/broker/backtesting.py
# Compiled at: 2016-11-30 04:57:04
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import abc
from pyalgotrade import broker
from pyalgotrade.broker import fillstrategy
from pyalgotrade import logger
import pyalgotrade.bar

class Commission(object):
    """Base class for implementing different commission schemes.

    .. note::
        This is a base class and should not be used directly.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate(self, order, price, quantity):
        """Calculates the commission for an order execution.

        :param order: The order being executed.
        :type order: :class:`pyalgotrade.broker.Order`.
        :param price: The price for each share.
        :type price: float.
        :param quantity: The order size.
        :type quantity: float.
        :rtype: float.
        """
        raise NotImplementedError()


class NoCommission(Commission):
    """A :class:`Commission` class that always returns 0."""

    def calculate(self, order, price, quantity):
        return 0


class FixedPerTrade(Commission):
    """A :class:`Commission` class that charges a fixed amount for the whole trade.

    :param amount: The commission for an order.
    :type amount: float.
    """

    def __init__(self, amount):
        super(FixedPerTrade, self).__init__()
        self.__amount = amount

    def calculate(self, order, price, quantity):
        ret = 0
        if order.getExecutionInfo() is None:
            ret = self.__amount
        return ret


class TradePercentage(Commission):
    """A :class:`Commission` class that charges a percentage of the whole trade.

    :param percentage: The percentage to charge. 0.01 means 1%, and so on. It must be smaller than 1.
    :type percentage: float.
    """

    def __init__(self, percentage):
        super(TradePercentage, self).__init__()
        assert percentage < 1
        self.__percentage = percentage

    def calculate(self, order, price, quantity):
        return price * quantity * self.__percentage


class BacktestingOrder(object):

    def __init__(self, *args, **kwargs):
        self.__accepted = None
        return

    def setAcceptedDateTime(self, dateTime):
        self.__accepted = dateTime

    def getAcceptedDateTime(self):
        return self.__accepted

    def process(self, broker_, bar_):
        raise NotImplementedError()


class MarketOrder(broker.MarketOrder, BacktestingOrder):

    def __init__(self, action, instrument, quantity, onClose, instrumentTraits):
        super(MarketOrder, self).__init__(action, instrument, quantity, onClose, instrumentTraits)

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillMarketOrder(broker_, self, bar_)


class CashMarketOrder(broker.MarketOrder, BacktestingOrder):

    def __init__(self, action, instrument, cashAmount, onClose, instrumentTraits):
        super(CashMarketOrder, self).__init__(action, instrument, quantity=None, onClose=onClose, instrumentTraits=instrumentTraits)
        self._quantity_caculated = False
        self.__cash_amount = cashAmount
        return

    def getCashAmount(self):
        return self.__cash_amount

    def process(self, broker_, bar_):
        if not self._quantity_caculated:
            if self.getFillOnClose():
                price = bar_.getClose(broker_.getUseAdjustedValues())
            else:
                price = bar_.getOpen(broker_.getUseAdjustedValues())
            self._setQuantity(self.cash2quantity(price, self.__cash_amount))
            self._quantity_caculated = True
        fill_info = broker_.getFillStrategy().fillCashMarketOrder(broker_, self, bar_, self.getCashAmount())
        return fill_info

    def cash2quantity(self, price, cash):
        return round(cash / float(price), 4)


class LimitOrder(broker.LimitOrder, BacktestingOrder):

    def __init__(self, action, instrument, limitPrice, quantity, instrumentTraits):
        super(LimitOrder, self).__init__(action, instrument, limitPrice, quantity, instrumentTraits)

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillLimitOrder(broker_, self, bar_)


class StopOrder(broker.StopOrder, BacktestingOrder):

    def __init__(self, action, instrument, stopPrice, quantity, instrumentTraits):
        super(StopOrder, self).__init__(action, instrument, stopPrice, quantity, instrumentTraits)
        self.__stopHit = False

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillStopOrder(broker_, self, bar_)

    def setStopHit(self, stopHit):
        self.__stopHit = stopHit

    def getStopHit(self):
        return self.__stopHit


class StopLimitOrder(broker.StopLimitOrder, BacktestingOrder):

    def __init__(self, action, instrument, stopPrice, limitPrice, quantity, instrumentTraits):
        super(StopLimitOrder, self).__init__(action, instrument, stopPrice, limitPrice, quantity, instrumentTraits)
        self.__stopHit = False

    def setStopHit(self, stopHit):
        self.__stopHit = stopHit

    def getStopHit(self):
        return self.__stopHit

    def isLimitOrderActive(self):
        return self.__stopHit

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillStopLimitOrder(broker_, self, bar_)


class Broker(broker.Broker):
    """Backtesting broker.

    :param cash: The initial amount of cash.
    :type cash: int/float.
    :param barFeed: The bar feed that will provide the bars.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`
    :param commission: An object responsible for calculating order commissions.
    :type commission: :class:`Commission`
    """
    LOGGER_NAME = 'broker.backtesting'

    def __init__(self, cash, barFeed, commission=None):
        super(Broker, self).__init__()
        assert cash >= 0
        self.__cash = cash
        if commission is None:
            self.__commission = NoCommission()
        else:
            self.__commission = commission
        self.__shares = {}
        self.__activeOrders = {}
        self.__useAdjustedValues = False
        self.__fillStrategy = fillstrategy.DefaultStrategy()
        self.__logger = logger.getLogger(Broker.LOGGER_NAME)
        barFeed.getNewValuesEvent().subscribe(self.onBars)
        self.__barFeed = barFeed
        self.__allowNegativeCash = False
        self.__nextOrderId = 1
        return

    def _getNextOrderId(self):
        ret = self.__nextOrderId
        self.__nextOrderId += 1
        return ret

    def _getBar(self, bars, instrument):
        ret = bars.getBar(instrument)
        if ret is None:
            ret = self.__barFeed.getLastBar(instrument)
        return ret

    def _registerOrder(self, order):
        assert order.getId() not in self.__activeOrders
        assert order.getId() is not None
        self.__activeOrders[order.getId()] = order
        return

    def _unregisterOrder(self, order):
        assert order.getId() in self.__activeOrders
        assert order.getId() is not None
        del self.__activeOrders[order.getId()]
        return

    def getLogger(self):
        return self.__logger

    def setAllowNegativeCash(self, allowNegativeCash):
        self.__allowNegativeCash = allowNegativeCash

    def getCash(self, includeShort=True):
        ret = self.__cash
        if not includeShort and self.__barFeed.getCurrentBars() is not None:
            bars = self.__barFeed.getCurrentBars()
            for instrument, shares in self.__shares.iteritems():
                if shares < 0:
                    instrumentPrice = self._getBar(bars, instrument).getClose(self.getUseAdjustedValues())
                    ret += instrumentPrice * shares

        return ret

    def setCash(self, cash):
        self.__cash = cash

    def getCommission(self):
        """Returns the strategy used to calculate order commissions.

        :rtype: :class:`Commission`.
        """
        return self.__commission

    def setCommission(self, commission):
        """Sets the strategy to use to calculate order commissions.

        :param commission: An object responsible for calculating order commissions.
        :type commission: :class:`Commission`.
        """
        self.__commission = commission

    def setFillStrategy(self, strategy):
        """Sets the :class:`pyalgotrade.broker.fillstrategy.FillStrategy` to use."""
        self.__fillStrategy = strategy

    def getFillStrategy(self):
        """Returns the :class:`pyalgotrade.broker.fillstrategy.FillStrategy` currently set."""
        return self.__fillStrategy

    def getUseAdjustedValues(self):
        return self.__useAdjustedValues

    def setUseAdjustedValues(self, useAdjusted):
        if not self.__barFeed.barsHaveAdjClose():
            raise Exception("The barfeed doesn't support adjusted close values")
        self.__useAdjustedValues = useAdjusted

    def getActiveOrders(self, instrument=None):
        if instrument is None:
            ret = self.__activeOrders.values()
        else:
            ret = [ order for order in self.__activeOrders.values() if order.getInstrument() == instrument ]
        return ret

    def _getCurrentDateTime(self):
        return self.__barFeed.getCurrentDateTime()

    def getInstrumentTraits(self, instrument):
        return broker.IntegerTraits()

    def getShares(self, instrument):
        return self.__shares.get(instrument, 0)

    def setShares(self, instrument, value):
        """
        This method should only works on asset init.
        :param instrument: the security name.
        :param value: how much you have of given instrument.
        """
        self.__shares[instrument] = value

    def getPositions(self):
        return self.__shares

    def getActiveInstruments(self):
        return [ instrument for instrument, shares in self.__shares.iteritems() if shares != 0 ]

    def __getEquityWithBars(self, bars):
        ret = self.getCash()
        if bars is not None:
            for instrument, shares in self.__shares.iteritems():
                instrumentPrice = self._getBar(bars, instrument).getClose(self.getUseAdjustedValues())
                ret += instrumentPrice * shares

        return ret

    def getEquity(self):
        """Returns the portfolio value (cash + shares)."""
        return self.__getEquityWithBars(self.__barFeed.getCurrentBars())

    def commitOrderExecution(self, order, dateTime, fillInfo):
        price = fillInfo.getPrice()
        quantity = fillInfo.getQuantity()
        if order.isBuy():
            cost = price * quantity * -1
            assert cost < 0
            sharesDelta = quantity
        elif order.isSell():
            cost = price * quantity
            assert cost > 0
            sharesDelta = quantity * -1
        else:
            assert False
        commission = self.getCommission().calculate(order, price, quantity)
        cost -= commission
        resultingCash = self.getCash() + cost
        if resultingCash >= 0 or self.__allowNegativeCash:
            orderExecutionInfo = broker.OrderExecutionInfo(price, quantity, commission, dateTime)
            order.addExecutionInfo(orderExecutionInfo)
            self.__cash = resultingCash
            updatedShares = order.getInstrumentTraits().roundQuantity(self.getShares(order.getInstrument()) + sharesDelta)
            if updatedShares == 0:
                del self.__shares[order.getInstrument()]
            else:
                self.__shares[order.getInstrument()] = updatedShares
            self.__fillStrategy.onOrderFilled(self, order)
            if order.isFilled():
                self._unregisterOrder(order)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.FILLED, orderExecutionInfo))
            elif order.isPartiallyFilled():
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.PARTIALLY_FILLED, orderExecutionInfo))
            else:
                assert False
        else:
            self.__logger.debug('Not enough cash to fill %s order [%s] for %s share/s' % (
             order.getInstrument(),
             order.getId(),
             order.getRemaining()))

    def submitOrder(self, order):
        if order.isInitial():
            order.setSubmitted(self._getNextOrderId(), self._getCurrentDateTime())
            self._registerOrder(order)
            order.switchState(broker.Order.State.SUBMITTED)
            self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.SUBMITTED, None))
        else:
            raise Exception('The order was already processed')
        return

    def __preProcessOrder(self, order, bar_):
        ret = True
        if not order.getGoodTillCanceled():
            expired = bar_.getDateTime().date() > order.getAcceptedDateTime().date()
            if expired:
                ret = False
                self._unregisterOrder(order)
                order.switchState(broker.Order.State.CANCELED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, 'Expired'))
        return ret

    def __postProcessOrder(self, order, bar_):
        if not order.getGoodTillCanceled():
            expired = False
            if self.__barFeed.getFrequency() >= pyalgotrade.bar.Frequency.DAY:
                expired = bar_.getDateTime().date() >= order.getAcceptedDateTime().date()
            if expired:
                self._unregisterOrder(order)
                order.switchState(broker.Order.State.CANCELED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, 'Expired'))

    def __processOrder(self, order, bar_):
        if not self.__preProcessOrder(order, bar_):
            return
        else:
            fillInfo = order.process(self, bar_)
            if fillInfo is not None:
                self.commitOrderExecution(order, bar_.getDateTime(), fillInfo)
            if order.isActive():
                self.__postProcessOrder(order, bar_)
            return

    def __onBarsImpl(self, order, bars):
        bar_ = bars.getBar(order.getInstrument())
        if bar_ is not None:
            if order.isSubmitted():
                order.setAcceptedDateTime(bar_.getDateTime())
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))
            if order.isActive():
                self.__processOrder(order, bar_)
            else:
                assert order.isCanceled()
                assert order not in self.__activeOrders
        return

    def onBars(self, dateTime, bars):
        self.__fillStrategy.onBars(self, bars)
        ordersToProcess = self.__activeOrders.values()
        for order in ordersToProcess:
            self.__onBarsImpl(order, bars)

    def start(self):
        super(Broker, self).start()

    def stop(self):
        pass

    def join(self):
        pass

    def eof(self):
        return self.__barFeed.eof()

    def dispatch(self):
        pass

    def peekDateTime(self):
        return

    def createCashBuyMarketOrder(self, action, instrument, cashAmount, onClose=False):
        if onClose is True and self.__barFeed.isIntraday():
            raise Exception('Market-on-close not supported with intraday feeds')
        return CashMarketOrder(action, instrument, cashAmount, onClose, self.getInstrumentTraits(instrument))

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        if onClose is True and self.__barFeed.isIntraday():
            raise Exception('Market-on-close not supported with intraday feeds')
        return MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        return LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        return StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        return StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))

    def cancelOrder(self, order):
        activeOrder = self.__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception('The order is not active anymore')
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")
        self._unregisterOrder(activeOrder)
        activeOrder.switchState(broker.Order.State.CANCELED)
        self.notifyOrderEvent(broker.OrderEvent(activeOrder, broker.OrderEvent.Type.CANCELED, 'User requested cancellation'))
        return