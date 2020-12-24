# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/broker/fillstrategy.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import abc
from pyalgotrade import broker
import pyalgotrade.bar, slippage

def get_limit_price_trigger(action, limitPrice, useAdjustedValues, bar):
    ret = None
    open_ = bar.getOpen(useAdjustedValues)
    high = bar.getHigh(useAdjustedValues)
    low = bar.getLow(useAdjustedValues)
    if action in [broker.Order.Action.BUY, broker.Order.Action.BUY_TO_COVER]:
        if high < limitPrice:
            ret = open_
        elif limitPrice >= low:
            if open_ < limitPrice:
                ret = open_
            else:
                ret = limitPrice
    elif action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
        if low > limitPrice:
            ret = open_
        elif limitPrice <= high:
            if open_ > limitPrice:
                ret = open_
            else:
                ret = limitPrice
    else:
        assert False
    return ret


def get_stop_price_trigger(action, stopPrice, useAdjustedValues, bar):
    ret = None
    open_ = bar.getOpen(useAdjustedValues)
    high = bar.getHigh(useAdjustedValues)
    low = bar.getLow(useAdjustedValues)
    if action in [broker.Order.Action.BUY, broker.Order.Action.BUY_TO_COVER]:
        if low > stopPrice:
            ret = open_
        elif stopPrice <= high:
            if open_ > stopPrice:
                ret = open_
            else:
                ret = stopPrice
    elif action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
        if high < stopPrice:
            ret = open_
        elif stopPrice >= low:
            if open_ < stopPrice:
                ret = open_
            else:
                ret = stopPrice
    else:
        assert False
    return ret


class FillInfo(object):

    def __init__(self, price, quantity):
        self.__price = price
        self.__quantity = quantity

    def getPrice(self):
        return self.__price

    def getQuantity(self):
        return self.__quantity


class FillStrategy(object):
    """Base class for order filling strategies for the backtester."""
    __metaclass__ = abc.ABCMeta

    def onBars(self, broker_, bars):
        """
        Override (optional) to get notified when the broker is about to process new bars.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param bars: The current bars.
        :type bars: :class:`pyalgotrade.bar.Bars`
        """
        pass

    def onOrderFilled(self, broker_, order):
        """
        Override (optional) to get notified when an order was filled, or partially filled.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order filled.
        :type order: :class:`pyalgotrade.broker.Order`
        """
        pass

    @abc.abstractmethod
    def fillMarketOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a market order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.MarketOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fillLimitOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a limit order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.LimitOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fillStopOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a stop order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.StopOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fillStopLimitOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a stop limit order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.StopLimitOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()


class DefaultStrategy(FillStrategy):
    """
    Default fill strategy.

    :param volumeLimit: The proportion of the volume that orders can take up in a bar. Must be > 0 and <= 1.
        If None, then volume limit is not checked.
    :type volumeLimit: float

    This strategy works as follows:

    * A :class:`pyalgotrade.broker.MarketOrder` is always filled using the open/close price.
    * A :class:`pyalgotrade.broker.LimitOrder` will be filled like this:
        * If the limit price was penetrated with the open price, then the open price is used.
        * If the bar includes the limit price, then the limit price is used.
        * Note that when buying the price is penetrated if it gets <= the limit price, and when selling the price
          is penetrated if it gets >= the limit price
    * A :class:`pyalgotrade.broker.StopOrder` will be filled like this:
        * If the stop price was penetrated with the open price, then the open price is used.
        * If the bar includes the stop price, then the stop price is used.
        * Note that when buying the price is penetrated if it gets >= the stop price, and when selling the price
          is penetrated if it gets <= the stop price
    * A :class:`pyalgotrade.broker.StopLimitOrder` will be filled like this:
        * If the stop price was penetrated with the open price, or if the bar includes the stop price, then the limit
          order becomes active.
        * If the limit order is active:
            * If the limit order was activated in this same bar and the limit price is penetrated as well, then the
              best between the stop price and the limit fill price (as described earlier) is used.
            * If the limit order was activated at a previous bar then the limit fill price (as described earlier)
              is used.

    .. note::
        * This is the default strategy used by the Broker.
        * It uses :class:`pyalgotrade.broker.slippage.NoSlippage` slippage model by default.
        * If volumeLimit is 0.25, and a certain bar's volume is 100, then no more than 25 shares can be used by all
          orders that get processed at that bar.
        * If using trade bars, then all the volume from that bar can be used.
    """

    def __init__(self, volumeLimit=0.25):
        super(DefaultStrategy, self).__init__()
        self.__volumeLeft = {}
        self.__volumeUsed = {}
        self.setVolumeLimit(volumeLimit)
        self.setSlippageModel(slippage.NoSlippage())

    def onBars(self, broker_, bars):
        volumeLeft = {}
        for instrument in bars.getInstruments():
            bar = bars[instrument]
            if bar.getFrequency() == pyalgotrade.bar.Frequency.TRADE:
                volumeLeft[instrument] = bar.getVolume()
            elif self.__volumeLimit is not None:
                volumeLeft[instrument] = bar.getVolume() * self.__volumeLimit
            self.__volumeUsed[instrument] = 0.0

        self.__volumeLeft = volumeLeft
        return

    def getVolumeLeft(self):
        return self.__volumeLeft

    def getVolumeUsed(self):
        return self.__volumeUsed

    def onOrderFilled(self, broker_, order):
        if self.__volumeLimit is not None:
            volumeLeft = order.getInstrumentTraits().roundQuantity(self.__volumeLeft[order.getInstrument()])
            fillQuantity = order.getExecutionInfo().getQuantity()
            assert volumeLeft >= fillQuantity, 'Invalid fill quantity %s. Not enough volume left %s' % (fillQuantity, volumeLeft)
            self.__volumeLeft[order.getInstrument()] = order.getInstrumentTraits().roundQuantity(volumeLeft - fillQuantity)
        self.__volumeUsed[order.getInstrument()] = order.getInstrumentTraits().roundQuantity(self.__volumeUsed[order.getInstrument()] + order.getExecutionInfo().getQuantity())
        return

    def setVolumeLimit(self, volumeLimit):
        """
        Set the volume limit.

        :param volumeLimit: The proportion of the volume that orders can take up in a bar. Must be > 0 and <= 1.
            If None, then volume limit is not checked.
        :type volumeLimit: float
        """
        assert volumeLimit is not None and volumeLimit > 0 and volumeLimit <= 1, 'Invalid volume limit'
        self.__volumeLimit = volumeLimit
        return

    def setSlippageModel(self, slippageModel):
        """
        Set the slippage model to use.

        :param slippageModel: The slippage model.
        :type slippageModel: :class:`pyalgotrade.broker.slippage.SlippageModel`
        """
        self.__slippageModel = slippageModel

    def __calculateFillSize(self, broker_, order, bar):
        ret = 0
        if self.__volumeLimit is not None:
            maxVolume = self.__volumeLeft.get(order.getInstrument(), 0)
            maxVolume = order.getInstrumentTraits().roundQuantity(maxVolume)
        else:
            maxVolume = order.getRemaining()
        if not order.getAllOrNone():
            ret = min(maxVolume, order.getRemaining())
        elif order.getRemaining() <= maxVolume:
            ret = order.getRemaining()
        return ret

    def fillMarketOrder(self, broker_, order, bar):
        fillSize = self.__calculateFillSize(broker_, order, bar)
        if fillSize == 0:
            broker_.getLogger().debug('Not enough volume to fill %s market order [%s] for %s share/s' % (
             order.getInstrument(),
             order.getId(),
             order.getRemaining()))
            return
        else:
            if order.getFillOnClose():
                price = bar.getClose(broker_.getUseAdjustedValues())
            else:
                price = bar.getOpen(broker_.getUseAdjustedValues())
            assert price is not None
            if bar.getFrequency() != pyalgotrade.bar.Frequency.TRADE:
                price = self.__slippageModel.calculatePrice(order, price, fillSize, bar, self.__volumeUsed[order.getInstrument()])
            return FillInfo(price, fillSize)

    def fillLimitOrder(self, broker_, order, bar):
        fillSize = self.__calculateFillSize(broker_, order, bar)
        if fillSize == 0:
            broker_.getLogger().debug('Not enough volume to fill %s limit order [%s] for %s share/s' % (
             order.getInstrument(), order.getId(), order.getRemaining()))
            return
        else:
            ret = None
            price = get_limit_price_trigger(order.getAction(), order.getLimitPrice(), broker_.getUseAdjustedValues(), bar)
            if price is not None:
                ret = FillInfo(price, fillSize)
            return ret

    def fillStopOrder(self, broker_, order, bar):
        ret = None
        stopPriceTrigger = None
        if not order.getStopHit():
            stopPriceTrigger = get_stop_price_trigger(order.getAction(), order.getStopPrice(), broker_.getUseAdjustedValues(), bar)
            order.setStopHit(stopPriceTrigger is not None)
        if order.getStopHit():
            fillSize = self.__calculateFillSize(broker_, order, bar)
            if fillSize == 0:
                broker_.getLogger().debug('Not enough volume to fill %s stop order [%s] for %s share/s' % (
                 order.getInstrument(),
                 order.getId(),
                 order.getRemaining()))
                return
            if stopPriceTrigger is not None:
                price = stopPriceTrigger
            else:
                price = bar.getOpen(broker_.getUseAdjustedValues())
            assert price is not None
            if bar.getFrequency() != pyalgotrade.bar.Frequency.TRADE:
                price = self.__slippageModel.calculatePrice(order, price, fillSize, bar, self.__volumeUsed[order.getInstrument()])
            ret = FillInfo(price, fillSize)
        return ret

    def fillStopLimitOrder(self, broker_, order, bar):
        ret = None
        stopPriceTrigger = None
        if not order.getStopHit():
            stopPriceTrigger = get_stop_price_trigger(order.getAction(), order.getStopPrice(), broker_.getUseAdjustedValues(), bar)
            order.setStopHit(stopPriceTrigger is not None)
        if order.getStopHit():
            fillSize = self.__calculateFillSize(broker_, order, bar)
            if fillSize == 0:
                broker_.getLogger().debug('Not enough volume to fill %s stop limit order [%s] for %s share/s' % (
                 order.getInstrument(),
                 order.getId(),
                 order.getRemaining()))
                return
            price = get_limit_price_trigger(order.getAction(), order.getLimitPrice(), broker_.getUseAdjustedValues(), bar)
            if price is not None:
                if stopPriceTrigger is not None:
                    if order.isBuy():
                        price = min(stopPriceTrigger, order.getLimitPrice())
                    else:
                        price = max(stopPriceTrigger, order.getLimitPrice())
                ret = FillInfo(price, fillSize)
        return ret