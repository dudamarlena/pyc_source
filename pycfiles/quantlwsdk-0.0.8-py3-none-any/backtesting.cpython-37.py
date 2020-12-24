# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\broker\backtesting.py
# Compiled at: 2019-06-05 03:25:59
# Size of source mod 2**32: 34648 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, six
from pyalgotrade import broker
from pyalgotrade.broker import fillstrategy
from pyalgotrade import logger
import pyalgotrade.bar

@six.add_metaclass(abc.ABCMeta)
class Commission(object):
    __doc__ = 'Base class for implementing different commission schemes.\n\n    .. note::\n        This is a base class and should not be used directly.\n    '

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
    __doc__ = 'A :class:`Commission` class that always returns 0.'

    def calculate(self, order, price, quantity):
        return 0


class FixedPerTrade(Commission):
    __doc__ = 'A :class:`Commission` class that charges a fixed amount for the whole trade.\n\n    :param amount: The commission for an order.\n    :type amount: float.\n    '

    def __init__(self, amount):
        super(FixedPerTrade, self).__init__()
        self._FixedPerTrade__amount = amount

    def calculate(self, order, price, quantity):
        ret = 0
        if order.getExecutionInfo() is None:
            ret = self._FixedPerTrade__amount
        return ret


class TradePercentage(Commission):
    __doc__ = 'A :class:`Commission` class that charges a percentage of the whole trade.\n\n    :param percentage: The percentage to charge. 0.01 means 1%, and so on. It must be smaller than 1.\n    :type percentage: float.\n    '

    def __init__(self, percentage):
        super(TradePercentage, self).__init__()
        assert percentage < 1
        self._TradePercentage__percentage = percentage

    def calculate(self, order, price, quantity):
        return price * quantity * self._TradePercentage__percentage


class BacktestingOrder(object):

    def __init__(self, *args, **kwargs):
        self._BacktestingOrder__accepted = None

    def setAcceptedDateTime(self, dateTime):
        self._BacktestingOrder__accepted = dateTime

    def getAcceptedDateTime(self):
        return self._BacktestingOrder__accepted

    def process(self, broker_, bar_):
        raise NotImplementedError()


class MarketOrder(broker.MarketOrder, BacktestingOrder):

    def __init__(self, action, instrument, quantity, onClose, instrumentTraits):
        super(MarketOrder, self).__init__(action, instrument, quantity, onClose, instrumentTraits)

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillMarketOrder(broker_, self, bar_)


class LimitOrder(broker.LimitOrder, BacktestingOrder):

    def __init__(self, action, instrument, limitPrice, quantity, instrumentTraits):
        super(LimitOrder, self).__init__(action, instrument, limitPrice, quantity, instrumentTraits)

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillLimitOrder(broker_, self, bar_)


class StopOrder(broker.StopOrder, BacktestingOrder):

    def __init__(self, action, instrument, stopPrice, quantity, instrumentTraits):
        super(StopOrder, self).__init__(action, instrument, stopPrice, quantity, instrumentTraits)
        self._StopOrder__stopHit = False

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillStopOrder(broker_, self, bar_)

    def setStopHit(self, stopHit):
        self._StopOrder__stopHit = stopHit

    def getStopHit(self):
        return self._StopOrder__stopHit


class StopLimitOrder(broker.StopLimitOrder, BacktestingOrder):

    def __init__(self, action, instrument, stopPrice, limitPrice, quantity, instrumentTraits):
        super(StopLimitOrder, self).__init__(action, instrument, stopPrice, limitPrice, quantity, instrumentTraits)
        self._StopLimitOrder__stopHit = False

    def setStopHit(self, stopHit):
        self._StopLimitOrder__stopHit = stopHit

    def getStopHit(self):
        return self._StopLimitOrder__stopHit

    def isLimitOrderActive(self):
        return self._StopLimitOrder__stopHit

    def process(self, broker_, bar_):
        return broker_.getFillStrategy().fillStopLimitOrder(broker_, self, bar_)


class Broker(broker.Broker):
    __doc__ = 'Backtesting broker.\n\n    :param cash: The initial amount of cash.\n    :type cash: int/float.\n    :param barFeed: The bar feed that will provide the bars.\n    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`\n    :param commission: An object responsible for calculating order commissions.\n    :type commission: :class:`Commission`\n    '
    LOGGER_NAME = 'broker.backtesting'

    def __init__(self, cash, barFeed, commission=None):
        super(Broker, self).__init__()
        if not cash >= 0:
            raise AssertionError
        else:
            self._Broker__cash = cash
            if commission is None:
                self._Broker__commission = NoCommission()
            else:
                self._Broker__commission = commission
        self._Broker__shares = {}
        self._Broker__instrumentPrice = {}
        self._Broker__activeOrders = {}
        self._Broker__useAdjustedValues = False
        self._Broker__fillStrategy = fillstrategy.DefaultStrategy()
        self._Broker__logger = logger.getLogger(Broker.LOGGER_NAME)
        barFeed.getNewValuesEvent().subscribe(self.onBars)
        self._Broker__barFeed = barFeed
        self._Broker__allowNegativeCash = False
        self._Broker__nextOrderId = 1
        self._Broker__started = False

    def _getNextOrderId(self):
        ret = self._Broker__nextOrderId
        self._Broker__nextOrderId += 1
        return ret

    def _getBar(self, bars, instrument):
        ret = bars.getBar(instrument)
        if ret is None:
            ret = self._Broker__barFeed.getLastBar(instrument)
        return ret

    def _registerOrder(self, order):
        assert order.getId() not in self._Broker__activeOrders
        assert order.getId() is not None
        self._Broker__activeOrders[order.getId()] = order

    def _unregisterOrder(self, order):
        assert order.getId() in self._Broker__activeOrders
        assert order.getId() is not None
        del self._Broker__activeOrders[order.getId()]

    def getLogger(self):
        return self._Broker__logger

    def setAllowNegativeCash(self, allowNegativeCash):
        self._Broker__allowNegativeCash = allowNegativeCash

    def getCash(self, includeShort=True):
        ret = self._Broker__cash
        if not includeShort:
            if self._Broker__barFeed.getCurrentBars() is not None:
                bars = self._Broker__barFeed.getCurrentBars()
                for instrument, shares in six.iteritems(self._Broker__shares):
                    if shares < 0:
                        instrumentPrice = self._getBar(bars, instrument).getPrice()
                        ret += instrumentPrice * shares

        return ret

    def setCash(self, cash):
        self._Broker__cash = cash

    def getCommission(self):
        """Returns the strategy used to calculate order commissions.

        :rtype: :class:`Commission`.
        """
        return self._Broker__commission

    def setCommission(self, commission):
        """Sets the strategy to use to calculate order commissions.

        :param commission: An object responsible for calculating order commissions.
        :type commission: :class:`Commission`.
        """
        self._Broker__commission = commission

    def setFillStrategy(self, strategy):
        """Sets the :class:`pyalgotrade.broker.fillstrategy.FillStrategy` to use."""
        self._Broker__fillStrategy = strategy

    def getFillStrategy(self):
        """Returns the :class:`pyalgotrade.broker.fillstrategy.FillStrategy` currently set."""
        return self._Broker__fillStrategy

    def getUseAdjustedValues(self):
        return self._Broker__useAdjustedValues

    def setUseAdjustedValues(self, useAdjusted):
        if not self._Broker__barFeed.barsHaveAdjClose():
            raise Exception("The barfeed doesn't support adjusted close values")
        self._Broker__useAdjustedValues = useAdjusted

    def getActiveOrders(self, instrument=None):
        if instrument is None:
            ret = list(self._Broker__activeOrders.values())
        else:
            ret = [order for order in self._Broker__activeOrders.values() if order.getInstrument() == instrument]
        return ret

    def _getCurrentDateTime(self):
        return self._Broker__barFeed.getCurrentDateTime()

    def getInstrumentTraits(self, instrument):
        return broker.IntegerTraits()

    def getShares(self, instrument):
        return self._Broker__shares.get(instrument, 0)

    def setShares(self, instrument, quantity, price):
        """
        Set existing shares before the strategy starts executing.

        :param instrument: Instrument identifier.
        :param quantity: The number of shares for the given instrument.
        :param price: The price for each share.
        """
        if self._Broker__started:
            raise AssertionError("Can't setShares once the strategy started executing")
        self._Broker__shares[instrument] = quantity
        self._Broker__instrumentPrice[instrument] = price

    def getPositions(self):
        return self._Broker__shares

    def getActiveInstruments(self):
        return [instrument for instrument, shares in six.iteritems(self._Broker__shares) if shares != 0]

    def _getPriceForInstrument(self, instrument):
        ret = None
        lastBar = self._Broker__barFeed.getLastBar(instrument)
        if lastBar is not None:
            ret = lastBar.getPrice()
        else:
            ret = self._Broker__instrumentPrice.get(instrument)
        return ret

    def getEquity(self):
        """Returns the portfolio value (cash + shares * price)."""
        ret = self.getCash()
        for instrument, shares in six.iteritems(self._Broker__shares):
            instrumentPrice = self._getPriceForInstrument(instrument)
            assert instrumentPrice is not None, 'Price for %s is missing' % instrument
            ret += instrumentPrice * shares

        return ret

    def commitOrderExecution(self, order, dateTime, fillInfo):
        price = fillInfo.getPrice()
        quantity = fillInfo.getQuantity()
        if order.isBuy():
            cost = price * quantity * -1
            assert cost < 0
            sharesDelta = quantity
        else:
            if order.isSell():
                cost = price * quantity
                assert cost > 0
                sharesDelta = quantity * -1
            else:
                if not False:
                    raise AssertionError
                else:
                    commission = self.getCommission().calculate(order, price, quantity)
                    cost -= commission
                    resultingCash = self.getCash() + cost
                    if resultingCash >= 0 or self._Broker__allowNegativeCash:
                        orderExecutionInfo = broker.OrderExecutionInfo(price, quantity, commission, dateTime)
                        order.addExecutionInfo(orderExecutionInfo)
                        self._Broker__cash = resultingCash
                        updatedShares = order.getInstrumentTraits().roundQuantity(self.getShares(order.getInstrument()) + sharesDelta)
                        if updatedShares == 0:
                            del self._Broker__shares[order.getInstrument()]
                        else:
                            self._Broker__shares[order.getInstrument()] = updatedShares
                        self._Broker__fillStrategy.onOrderFilled(self, order)
                        if order.isFilled():
                            self._unregisterOrder(order)
                            self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.FILLED, orderExecutionInfo))
                        else:
                            if order.isPartiallyFilled():
                                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.PARTIALLY_FILLED, orderExecutionInfo))
                            else:
                                assert False
                    else:
                        self._Broker__logger.debug('Not enough cash to fill %s order [%s] for %s share/s' % (
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
            if self._Broker__barFeed.getFrequency() >= pyalgotrade.bar.Frequency.DAY:
                expired = bar_.getDateTime().date() >= order.getAcceptedDateTime().date()
            if expired:
                self._unregisterOrder(order)
                order.switchState(broker.Order.State.CANCELED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, 'Expired'))

    def __processOrder(self, order, bar_):
        if not self._Broker__preProcessOrder(order, bar_):
            return
        fillInfo = order.process(self, bar_)
        if fillInfo is not None:
            self.commitOrderExecution(order, bar_.getDateTime(), fillInfo)
        if order.isActive():
            self._Broker__postProcessOrder(order, bar_)

    def __onBarsImpl(self, order, bars):
        bar_ = bars.getBar(order.getInstrument())
        if bar_ is not None:
            if order.isSubmitted():
                order.setAcceptedDateTime(bar_.getDateTime())
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))
            if order.isActive():
                self._Broker__processOrder(order, bar_)
            else:
                assert order.isCanceled()
                assert order not in self._Broker__activeOrders

    def onBars(self, dateTime, bars):
        self._Broker__fillStrategy.onBars(self, bars)
        ordersToProcess = list(self._Broker__activeOrders.values())
        for order in ordersToProcess:
            self._Broker__onBarsImpl(order, bars)

    def start(self):
        super(Broker, self).start()
        self._Broker__started = True

    def stop(self):
        pass

    def join(self):
        pass

    def eof(self):
        return self._Broker__barFeed.eof()

    def dispatch(self):
        pass

    def peekDateTime(self):
        pass

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        if onClose is True:
            if self._Broker__barFeed.isIntraday():
                raise Exception('Market-on-close not supported with intraday feeds')
        return MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        return LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        return StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        return StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))

    def cancelOrder(self, order):
        activeOrder = self._Broker__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception('The order is not active anymore')
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")
        self._unregisterOrder(activeOrder)
        activeOrder.switchState(broker.Order.State.CANCELED)
        self.notifyOrderEvent(broker.OrderEvent(activeOrder, broker.OrderEvent.Type.CANCELED, 'User requested cancellation'))


class ChinaFutureBroker(broker.Broker):
    __doc__ = 'Backtesting broker.\n\n    :param cash: The initial amount of cash.\n    :type cash: int/float.\n    :param barFeed: The bar feed that will provide the bars.\n    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`\n    :param commission: An object responsible for calculating order commissions.\n    :type commission: :class:`Commission`\n    '
    LOGGER_NAME = 'ChinaFutureBroker.backtesting'

    def __init__(self, cash, barFeed, commission=None):
        super(Broker, self).__init__()
        if not cash >= 0:
            raise AssertionError
        else:
            self._ChinaFutureBroker__cash = cash
            if commission is None:
                self._ChinaFutureBroker__commission = NoCommission()
            else:
                self._ChinaFutureBroker__commission = commission
        self._ChinaFutureBroker__shares = {}
        self._ChinaFutureBroker__instrumentPrice = {}
        self._ChinaFutureBroker__activeOrders = {}
        self._ChinaFutureBroker__useAdjustedValues = False
        self._ChinaFutureBroker__fillStrategy = fillstrategy.DefaultStrategy()
        self._ChinaFutureBroker__logger = logger.getLogger(Broker.LOGGER_NAME)
        barFeed.getNewValuesEvent().subscribe(self.onBars)
        self._ChinaFutureBroker__barFeed = barFeed
        self._ChinaFutureBroker__allowNegativeCash = False
        self._ChinaFutureBroker__nextOrderId = 1
        self._ChinaFutureBroker__started = False

    def _getNextOrderId(self):
        ret = self._ChinaFutureBroker__nextOrderId
        self._ChinaFutureBroker__nextOrderId += 1
        return ret

    def _getBar(self, bars, instrument):
        ret = bars.getBar(instrument)
        if ret is None:
            ret = self._ChinaFutureBroker__barFeed.getLastBar(instrument)
        return ret

    def _registerOrder(self, order):
        assert order.getId() not in self._ChinaFutureBroker__activeOrders
        assert order.getId() is not None
        self._ChinaFutureBroker__activeOrders[order.getId()] = order

    def _unregisterOrder(self, order):
        assert order.getId() in self._ChinaFutureBroker__activeOrders
        assert order.getId() is not None
        del self._ChinaFutureBroker__activeOrders[order.getId()]

    def getLogger(self):
        return self._ChinaFutureBroker__logger

    def setAllowNegativeCash(self, allowNegativeCash):
        self._ChinaFutureBroker__allowNegativeCash = allowNegativeCash

    def getCash(self, includeShort=True):
        ret = self._ChinaFutureBroker__cash
        if not includeShort:
            if self._ChinaFutureBroker__barFeed.getCurrentBars() is not None:
                bars = self._ChinaFutureBroker__barFeed.getCurrentBars()
                for instrument, shares in six.iteritems(self._ChinaFutureBroker__shares):
                    if shares < 0:
                        instrumentPrice = self._getBar(bars, instrument).getPrice()
                        ret += instrumentPrice * shares

        return ret

    def setCash(self, cash):
        self._ChinaFutureBroker__cash = cash

    def getCommission(self):
        """Returns the strategy used to calculate order commissions.

        :rtype: :class:`Commission`.
        """
        return self._ChinaFutureBroker__commission

    def setCommission(self, commission):
        """Sets the strategy to use to calculate order commissions.

        :param commission: An object responsible for calculating order commissions.
        :type commission: :class:`Commission`.
        """
        self._ChinaFutureBroker__commission = commission

    def setFillStrategy(self, strategy):
        """Sets the :class:`pyalgotrade.broker.fillstrategy.FillStrategy` to use."""
        self._ChinaFutureBroker__fillStrategy = strategy

    def getFillStrategy(self):
        """Returns the :class:`pyalgotrade.broker.fillstrategy.FillStrategy` currently set."""
        return self._ChinaFutureBroker__fillStrategy

    def getUseAdjustedValues(self):
        return self._ChinaFutureBroker__useAdjustedValues

    def setUseAdjustedValues(self, useAdjusted):
        if not self._ChinaFutureBroker__barFeed.barsHaveAdjClose():
            raise Exception("The barfeed doesn't support adjusted close values")
        self._ChinaFutureBroker__useAdjustedValues = useAdjusted

    def getActiveOrders(self, instrument=None):
        if instrument is None:
            ret = list(self._ChinaFutureBroker__activeOrders.values())
        else:
            ret = [order for order in self._ChinaFutureBroker__activeOrders.values() if order.getInstrument() == instrument]
        return ret

    def _getCurrentDateTime(self):
        return self._ChinaFutureBroker__barFeed.getCurrentDateTime()

    def getInstrumentTraits(self, instrument):
        return broker.IntegerTraits()

    def getShares(self, instrument):
        return self._ChinaFutureBroker__shares.get(instrument, 0)

    def setShares(self, instrument, quantity, price):
        """
        Set existing shares before the strategy starts executing.

        :param instrument: Instrument identifier.
        :param quantity: The number of shares for the given instrument.
        :param price: The price for each share.
        """
        if self._ChinaFutureBroker__started:
            raise AssertionError("Can't setShares once the strategy started executing")
        self._ChinaFutureBroker__shares[instrument] = quantity
        self._ChinaFutureBroker__instrumentPrice[instrument] = price

    def getPositions(self):
        return self._ChinaFutureBroker__shares

    def getActiveInstruments(self):
        return [instrument for instrument, shares in six.iteritems(self._ChinaFutureBroker__shares) if shares != 0]

    def _getPriceForInstrument(self, instrument):
        ret = None
        lastBar = self._ChinaFutureBroker__barFeed.getLastBar(instrument)
        if lastBar is not None:
            ret = lastBar.getPrice()
        else:
            ret = self._ChinaFutureBroker__instrumentPrice.get(instrument)
        return ret

    def getEquity(self):
        """Returns the portfolio value (cash + shares * price)."""
        ret = self.getCash()
        for instrument, shares in six.iteritems(self._ChinaFutureBroker__shares):
            instrumentPrice = self._getPriceForInstrument(instrument)
            assert instrumentPrice is not None, 'Price for %s is missing' % instrument
            ret += instrumentPrice * shares

        return ret

    def commitOrderExecution(self, order, dateTime, fillInfo):
        price = fillInfo.getPrice()
        quantity = fillInfo.getQuantity()
        if order.isBuy():
            cost = price * quantity * -1
            assert cost < 0
            sharesDelta = quantity
        else:
            if order.isSell():
                cost = price * quantity
                assert cost > 0
                sharesDelta = quantity * -1
            else:
                if not False:
                    raise AssertionError
                else:
                    commission = self.getCommission().calculate(order, price, quantity)
                    cost -= commission
                    resultingCash = self.getCash() + cost
                    if resultingCash >= 0 or self._ChinaFutureBroker__allowNegativeCash:
                        orderExecutionInfo = broker.OrderExecutionInfo(price, quantity, commission, dateTime)
                        order.addExecutionInfo(orderExecutionInfo)
                        self._ChinaFutureBroker__cash = resultingCash
                        updatedShares = order.getInstrumentTraits().roundQuantity(self.getShares(order.getInstrument()) + sharesDelta)
                        if updatedShares == 0:
                            del self._ChinaFutureBroker__shares[order.getInstrument()]
                        else:
                            self._ChinaFutureBroker__shares[order.getInstrument()] = updatedShares
                        self._ChinaFutureBroker__fillStrategy.onOrderFilled(self, order)
                        if order.isFilled():
                            self._unregisterOrder(order)
                            self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.FILLED, orderExecutionInfo))
                        else:
                            if order.isPartiallyFilled():
                                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.PARTIALLY_FILLED, orderExecutionInfo))
                            else:
                                assert False
                    else:
                        self._ChinaFutureBroker__logger.debug('Not enough cash to fill %s order [%s] for %s share/s' % (
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
            if self._ChinaFutureBroker__barFeed.getFrequency() >= pyalgotrade.bar.Frequency.DAY:
                expired = bar_.getDateTime().date() >= order.getAcceptedDateTime().date()
            if expired:
                self._unregisterOrder(order)
                order.switchState(broker.Order.State.CANCELED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, 'Expired'))

    def __processOrder(self, order, bar_):
        if not self._ChinaFutureBroker__preProcessOrder(order, bar_):
            return
        fillInfo = order.process(self, bar_)
        if fillInfo is not None:
            self.commitOrderExecution(order, bar_.getDateTime(), fillInfo)
        if order.isActive():
            self._ChinaFutureBroker__postProcessOrder(order, bar_)

    def __onBarsImpl(self, order, bars):
        bar_ = bars.getBar(order.getInstrument())
        if bar_ is not None:
            if order.isSubmitted():
                order.setAcceptedDateTime(bar_.getDateTime())
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))
            if order.isActive():
                self._ChinaFutureBroker__processOrder(order, bar_)
            else:
                assert order.isCanceled()
                assert order not in self._ChinaFutureBroker__activeOrders

    def onBars(self, dateTime, bars):
        self._ChinaFutureBroker__fillStrategy.onBars(self, bars)
        ordersToProcess = list(self._ChinaFutureBroker__activeOrders.values())
        for order in ordersToProcess:
            self._ChinaFutureBroker__onBarsImpl(order, bars)

    def start(self):
        super(Broker, self).start()
        self._ChinaFutureBroker__started = True

    def stop(self):
        pass

    def join(self):
        pass

    def eof(self):
        return self._ChinaFutureBroker__barFeed.eof()

    def dispatch(self):
        pass

    def peekDateTime(self):
        pass

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        if onClose is True:
            if self._ChinaFutureBroker__barFeed.isIntraday():
                raise Exception('Market-on-close not supported with intraday feeds')
        return MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        return LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        return StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        return StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))

    def cancelOrder(self, order):
        activeOrder = self._ChinaFutureBroker__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception('The order is not active anymore')
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")
        self._unregisterOrder(activeOrder)
        activeOrder.switchState(broker.Order.State.CANCELED)
        self.notifyOrderEvent(broker.OrderEvent(activeOrder, broker.OrderEvent.Type.CANCELED, 'User requested cancellation'))