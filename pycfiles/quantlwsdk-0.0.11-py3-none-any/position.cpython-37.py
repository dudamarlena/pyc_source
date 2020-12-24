# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\strategy\position.py
# Compiled at: 2019-11-01 23:06:06
# Size of source mod 2**32: 23018 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import warninghelpers
from pyalgotrade import broker
import datetime

class PositionState(object):

    def onEnter(self, position):
        pass

    def canSubmitOrder(self, position, order):
        raise NotImplementedError()

    def onOrderEvent(self, position, orderEvent):
        raise NotImplementedError()

    def isOpen(self, position):
        raise NotImplementedError()

    def exit(self, position, stopPrice=None, limitPrice=None, goodTillCanceled=None):
        raise NotImplementedError()


class WaitingEntryState(PositionState):

    def canSubmitOrder(self, position, order):
        if position.entryActive():
            raise Exception('The entry order is still active')

    def onOrderEvent(self, position, orderEvent):
        if not position.getEntryOrder().getId() == orderEvent.getOrder().getId():
            raise AssertionError
        elif orderEvent.getEventType() in (broker.OrderEvent.Type.FILLED, broker.OrderEvent.Type.PARTIALLY_FILLED):
            position.switchState(OpenState())
            position.getStrategy().onEnterOk(position)
        else:
            if orderEvent.getEventType() == broker.OrderEvent.Type.CANCELED:
                assert position.getEntryOrder().getFilled() == 0
                position.switchState(ClosedState())
                position.getStrategy().onEnterCanceled(position)

    def isOpen(self, position):
        return True

    def exit(self, position, stopPrice=None, limitPrice=None, goodTillCanceled=None):
        assert position.getShares() == 0
        assert position.getEntryOrder().isActive()
        position.getStrategy().getBroker().cancelOrder(position.getEntryOrder())


class OpenState(PositionState):

    def onEnter(self, position):
        entryDateTime = position.getEntryOrder().getExecutionInfo().getDateTime()
        position.setEntryDateTime(entryDateTime)

    def canSubmitOrder(self, position, order):
        pass

    def onOrderEvent(self, position, orderEvent):
        if position.getExitOrder():
            if position.getExitOrder().getId() == orderEvent.getOrder().getId():
                if orderEvent.getEventType() == broker.OrderEvent.Type.FILLED:
                    if position.getShares() == 0:
                        position.switchState(ClosedState())
                        position.getStrategy().onExitOk(position)
                elif orderEvent.getEventType() == broker.OrderEvent.Type.CANCELED:
                    if not position.getShares() != 0:
                        raise AssertionError
            else:
                position.getStrategy().onExitCanceled(position)
        else:
            if position.getEntryOrder().getId() == orderEvent.getOrder().getId() and not position.getShares() != 0:
                raise AssertionError
            else:
                raise Exception("Invalid order event '%s' in OpenState" % orderEvent.getEventType())

    def isOpen(self, position):
        return True

    def exit(self, position, stopPrice=None, limitPrice=None, goodTillCanceled=None):
        assert position.getShares() != 0
        if position.exitActive():
            raise Exception('Exit order is active and it should be canceled first')
        if position.entryActive():
            position.getStrategy().getBroker().cancelOrder(position.getEntryOrder())
        position._submitExitOrder(stopPrice, limitPrice, goodTillCanceled)


class ClosedState(PositionState):

    def onEnter(self, position):
        if position.exitFilled():
            exitDateTime = position.getExitOrder().getExecutionInfo().getDateTime()
            position.setExitDateTime(exitDateTime)
        assert position.getShares() == 0
        position.getStrategy().unregisterPosition(position)

    def canSubmitOrder(self, position, order):
        raise Exception('The position is closed')

    def onOrderEvent(self, position, orderEvent):
        raise Exception("Invalid order event '%s' in ClosedState" % orderEvent.getEventType())

    def isOpen(self, position):
        return False

    def exit(self, position, stopPrice=None, limitPrice=None, goodTillCanceled=None):
        pass


class Position(object):
    __doc__ = 'Base class for positions.\n\n    Positions are higher level abstractions for placing orders.\n    They are escentially a pair of entry-exit orders and allow\n    to track returns and PnL easier that placing orders manually.\n\n    :param strategy: The strategy that this position belongs to.\n    :type strategy: :class:`pyalgotrade.strategy.BaseStrategy`.\n    :param entryOrder: The order used to enter the position.\n    :type entryOrder: :class:`pyalgotrade.broker.Order`\n    :param goodTillCanceled: True if the entry order should be set as good till canceled.\n    :type goodTillCanceled: boolean.\n    :param allOrNone: True if the orders should be completely filled or not at all.\n    :type allOrNone: boolean.\n\n    .. note::\n        This is a base class and should not be used directly.\n    '

    def __init__(self, strategy, entryOrder, goodTillCanceled, allOrNone):
        assert entryOrder.isInitial()
        self._Position__state = None
        self._Position__activeOrders = {}
        self._Position__shares = 0
        self._Position__strategy = strategy
        self._Position__entryOrder = None
        self._Position__entryDateTime = None
        self._Position__exitOrder = None
        self._Position__exitDateTime = None
        self._Position__posTracker = returns.PositionTracker(entryOrder.getInstrumentTraits())
        self._Position__allOrNone = allOrNone
        self.switchState(WaitingEntryState())
        entryOrder.setGoodTillCanceled(goodTillCanceled)
        entryOrder.setAllOrNone(allOrNone)
        self._Position__submitAndRegisterOrder(entryOrder)
        self._Position__entryOrder = entryOrder

    def __submitAndRegisterOrder(self, order):
        assert order.isInitial()
        self._Position__state.canSubmitOrder(self, order)
        self.getStrategy().getBroker().submitOrder(order)
        self._Position__activeOrders[order.getId()] = order
        self.getStrategy().registerPositionOrder(self, order)

    def setEntryDateTime(self, dateTime):
        self._Position__entryDateTime = dateTime

    def setExitDateTime(self, dateTime):
        self._Position__exitDateTime = dateTime

    def switchState(self, newState):
        self._Position__state = newState
        self._Position__state.onEnter(self)

    def getStrategy(self):
        return self._Position__strategy

    def getLastPrice(self):
        return self._Position__strategy.getLastPrice(self.getInstrument())

    def getActiveOrders(self):
        return list(self._Position__activeOrders.values())

    def getShares(self):
        """Returns the number of shares.
        This will be a possitive number for a long position, and a negative number for a short position.

        .. note::
            If the entry order was not filled, or if the position is closed, then the number of shares will be 0.
        """
        return self._Position__shares

    def entryActive(self):
        """Returns True if the entry order is active."""
        return self._Position__entryOrder is not None and self._Position__entryOrder.isActive()

    def entryFilled(self):
        """Returns True if the entry order was filled."""
        return self._Position__entryOrder is not None and self._Position__entryOrder.isFilled()

    def exitActive(self):
        """Returns True if the exit order is active."""
        return self._Position__exitOrder is not None and self._Position__exitOrder.isActive()

    def exitFilled(self):
        """Returns True if the exit order was filled."""
        return self._Position__exitOrder is not None and self._Position__exitOrder.isFilled()

    def getEntryOrder(self):
        """Returns the :class:`pyalgotrade.broker.Order` used to enter the position."""
        return self._Position__entryOrder

    def getExitOrder(self):
        """Returns the :class:`pyalgotrade.broker.Order` used to exit the position. If this position hasn't been closed yet, None is returned."""
        return self._Position__exitOrder

    def getInstrument(self):
        """Returns the instrument used for this position."""
        return self._Position__entryOrder.getInstrument()

    def getReturn(self, includeCommissions=True):
        """
        Calculates cumulative percentage returns up to this point.
        If the position is not closed, these will be unrealized returns.
        """
        if includeCommissions is False:
            warninghelpers.deprecation_warning('includeCommissions will be deprecated in the next version.', stacklevel=2)
        ret = 0
        price = self.getLastPrice()
        if price is not None:
            ret = self._Position__posTracker.getReturn(price, includeCommissions)
        return ret

    def getPnL(self, includeCommissions=True):
        """
        Calculates PnL up to this point.
        If the position is not closed, these will be unrealized PnL.
        """
        if includeCommissions is False:
            warninghelpers.deprecation_warning('includeCommissions will be deprecated in the next version.', stacklevel=2)
        ret = 0
        price = self.getLastPrice()
        if price is not None:
            ret = self._Position__posTracker.getPnL(price=price, includeCommissions=includeCommissions)
        return ret

    def cancelEntry(self):
        """Cancels the entry order if its active."""
        if self.entryActive():
            self.getStrategy().getBroker().cancelOrder(self.getEntryOrder())

    def cancelExit(self):
        """Cancels the exit order if its active."""
        if self.exitActive():
            self.getStrategy().getBroker().cancelOrder(self.getExitOrder())

    def exitMarket(self, goodTillCanceled=None):
        """Submits a market order to close this position.

        :param goodTillCanceled: True if the exit order is good till canceled. If False then the order gets automatically canceled when the session closes. If None, then it will match the entry order.
        :type goodTillCanceled: boolean.

        .. note::
            * If the position is closed (entry canceled or exit filled) this won't have any effect.
            * If the exit order for this position is pending, an exception will be raised. The exit order should be canceled first.
            * If the entry order is active, cancellation will be requested.
        """
        self._Position__state.exit(self, None, None, goodTillCanceled)

    def exitLimit(self, limitPrice, goodTillCanceled=None):
        """Submits a limit order to close this position.

        :param limitPrice: The limit price.
        :type limitPrice: float.
        :param goodTillCanceled: True if the exit order is good till canceled. If False then the order gets automatically canceled when the session closes. If None, then it will match the entry order.
        :type goodTillCanceled: boolean.

        .. note::
            * If the position is closed (entry canceled or exit filled) this won't have any effect.
            * If the exit order for this position is pending, an exception will be raised. The exit order should be canceled first.
            * If the entry order is active, cancellation will be requested.
        """
        self._Position__state.exit(self, None, limitPrice, goodTillCanceled)

    def exitStop(self, stopPrice, goodTillCanceled=None):
        """Submits a stop order to close this position.

        :param stopPrice: The stop price.
        :type stopPrice: float.
        :param goodTillCanceled: True if the exit order is good till canceled. If False then the order gets automatically canceled when the session closes. If None, then it will match the entry order.
        :type goodTillCanceled: boolean.

        .. note::
            * If the position is closed (entry canceled or exit filled) this won't have any effect.
            * If the exit order for this position is pending, an exception will be raised. The exit order should be canceled first.
            * If the entry order is active, cancellation will be requested.
        """
        self._Position__state.exit(self, stopPrice, None, goodTillCanceled)

    def exitStopLimit(self, stopPrice, limitPrice, goodTillCanceled=None):
        """Submits a stop limit order to close this position.

        :param stopPrice: The stop price.
        :type stopPrice: float.
        :param limitPrice: The limit price.
        :type limitPrice: float.
        :param goodTillCanceled: True if the exit order is good till canceled. If False then the order gets automatically canceled when the session closes. If None, then it will match the entry order.
        :type goodTillCanceled: boolean.

        .. note::
            * If the position is closed (entry canceled or exit filled) this won't have any effect.
            * If the exit order for this position is pending, an exception will be raised. The exit order should be canceled first.
            * If the entry order is active, cancellation will be requested.
        """
        self._Position__state.exit(self, stopPrice, limitPrice, goodTillCanceled)

    def _submitExitOrder(self, stopPrice, limitPrice, goodTillCanceled):
        assert not self.exitActive()
        exitOrder = self.buildExitOrder(stopPrice, limitPrice)
        if goodTillCanceled is None:
            goodTillCanceled = self._Position__entryOrder.getGoodTillCanceled()
        exitOrder.setGoodTillCanceled(goodTillCanceled)
        exitOrder.setAllOrNone(self._Position__allOrNone)
        self._Position__submitAndRegisterOrder(exitOrder)
        self._Position__exitOrder = exitOrder

    def onOrderEvent(self, orderEvent):
        self._Position__updatePosTracker(orderEvent)
        order = orderEvent.getOrder()
        if not order.isActive():
            del self._Position__activeOrders[order.getId()]
        elif orderEvent.getEventType() in (broker.OrderEvent.Type.PARTIALLY_FILLED, broker.OrderEvent.Type.FILLED):
            execInfo = orderEvent.getEventInfo()
            if order.isBuy():
                self._Position__shares = order.getInstrumentTraits().roundQuantity(self._Position__shares + execInfo.getQuantity())
            else:
                self._Position__shares = order.getInstrumentTraits().roundQuantity(self._Position__shares - execInfo.getQuantity())
        self._Position__state.onOrderEvent(self, orderEvent)

    def __updatePosTracker(self, orderEvent):
        if orderEvent.getEventType() in (broker.OrderEvent.Type.PARTIALLY_FILLED, broker.OrderEvent.Type.FILLED):
            order = orderEvent.getOrder()
            execInfo = orderEvent.getEventInfo()
            if order.isBuy():
                self._Position__posTracker.buy(execInfo.getQuantity(), execInfo.getPrice(), execInfo.getCommission())
            else:
                self._Position__posTracker.sell(execInfo.getQuantity(), execInfo.getPrice(), execInfo.getCommission())

    def buildExitOrder(self, stopPrice, limitPrice):
        raise NotImplementedError()

    def isOpen(self):
        """Returns True if the position is open."""
        return self._Position__state.isOpen(self)

    def getAge(self):
        """Returns the duration in open state.

        :rtype: datetime.timedelta.

        .. note::
            * If the position is open, then the difference between the entry datetime and the datetime of the last bar is returned.
            * If the position is closed, then the difference between the entry datetime and the exit datetime is returned.
        """
        ret = datetime.timedelta()
        if self._Position__entryDateTime is not None:
            if self._Position__exitDateTime is not None:
                last = self._Position__exitDateTime
            else:
                last = self._Position__strategy.getCurrentDateTime()
            ret = last - self._Position__entryDateTime
        return ret


class LongPosition(Position):

    def __init__(self, strategy, instrument, stopPrice, limitPrice, quantity, goodTillCanceled, allOrNone):
        if limitPrice is None and stopPrice is None:
            entryOrder = strategy.getBroker().createMarketOrder(broker.Order.Action.BUY, instrument, quantity, False)
        else:
            if limitPrice is not None and stopPrice is None:
                entryOrder = strategy.getBroker().createLimitOrder(broker.Order.Action.BUY, instrument, limitPrice, quantity)
            else:
                if limitPrice is None and stopPrice is not None:
                    entryOrder = strategy.getBroker().createStopOrder(broker.Order.Action.BUY, instrument, stopPrice, quantity)
                else:
                    if limitPrice is not None and stopPrice is not None:
                        entryOrder = strategy.getBroker().createStopLimitOrder(broker.Order.Action.BUY, instrument, stopPrice, limitPrice, quantity)
                    else:
                        assert False
        super(LongPosition, self).__init__(strategy, entryOrder, goodTillCanceled, allOrNone)

    def buildExitOrder(self, stopPrice, limitPrice):
        quantity = self.getShares()
        assert quantity > 0
        if limitPrice is None and stopPrice is None:
            ret = self.getStrategy().getBroker().createMarketOrder(broker.Order.Action.SELL, self.getInstrument(), quantity, False)
        else:
            if limitPrice is not None and stopPrice is None:
                ret = self.getStrategy().getBroker().createLimitOrder(broker.Order.Action.SELL, self.getInstrument(), limitPrice, quantity)
            else:
                if limitPrice is None and stopPrice is not None:
                    ret = self.getStrategy().getBroker().createStopOrder(broker.Order.Action.SELL, self.getInstrument(), stopPrice, quantity)
                else:
                    if limitPrice is not None and stopPrice is not None:
                        ret = self.getStrategy().getBroker().createStopLimitOrder(broker.Order.Action.SELL, self.getInstrument(), stopPrice, limitPrice, quantity)
                    else:
                        assert False
        return ret


class ShortPosition(Position):

    def __init__(self, strategy, instrument, stopPrice, limitPrice, quantity, goodTillCanceled, allOrNone):
        if limitPrice is None and stopPrice is None:
            entryOrder = strategy.getBroker().createMarketOrder(broker.Order.Action.SELL_SHORT, instrument, quantity, False)
        else:
            if limitPrice is not None and stopPrice is None:
                entryOrder = strategy.getBroker().createLimitOrder(broker.Order.Action.SELL_SHORT, instrument, limitPrice, quantity)
            else:
                if limitPrice is None and stopPrice is not None:
                    entryOrder = strategy.getBroker().createStopOrder(broker.Order.Action.SELL_SHORT, instrument, stopPrice, quantity)
                else:
                    if limitPrice is not None and stopPrice is not None:
                        entryOrder = strategy.getBroker().createStopLimitOrder(broker.Order.Action.SELL_SHORT, instrument, stopPrice, limitPrice, quantity)
                    else:
                        assert False
        super(ShortPosition, self).__init__(strategy, entryOrder, goodTillCanceled, allOrNone)

    def buildExitOrder(self, stopPrice, limitPrice):
        quantity = self.getShares() * -1
        assert quantity > 0
        if limitPrice is None and stopPrice is None:
            ret = self.getStrategy().getBroker().createMarketOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), quantity, False)
        else:
            if limitPrice is not None and stopPrice is None:
                ret = self.getStrategy().getBroker().createLimitOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), limitPrice, quantity)
            else:
                if limitPrice is None and stopPrice is not None:
                    ret = self.getStrategy().getBroker().createStopOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), stopPrice, quantity)
                else:
                    if limitPrice is not None and stopPrice is not None:
                        ret = self.getStrategy().getBroker().createStopLimitOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), stopPrice, limitPrice, quantity)
                    else:
                        assert False
        return ret