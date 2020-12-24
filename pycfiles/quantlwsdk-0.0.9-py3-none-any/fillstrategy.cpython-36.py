# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\broker\fillstrategy.py
# Compiled at: 2019-06-05 03:26:00
# Size of source mod 2**32: 18082 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, six
from pyalgotrade import broker
import pyalgotrade.bar
from . import slippage

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
    else:
        if action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
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
    else:
        if action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
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
        self._FillInfo__price = price
        self._FillInfo__quantity = quantity

    def getPrice(self):
        return self._FillInfo__price

    def getQuantity(self):
        return self._FillInfo__quantity


@six.add_metaclass(abc.ABCMeta)
class FillStrategy(object):
    __doc__ = 'Base class for order filling strategies for the backtester.'

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
    __doc__ = "\n    Default fill strategy.\n\n    :param volumeLimit: The proportion of the volume that orders can take up in a bar. Must be > 0 and <= 1.\n        If None, then volume limit is not checked.\n    :type volumeLimit: float\n\n    This strategy works as follows:\n\n    * A :class:`pyalgotrade.broker.MarketOrder` is always filled using the open/close price.\n    * A :class:`pyalgotrade.broker.LimitOrder` will be filled like this:\n        * If the limit price was penetrated with the open price, then the open price is used.\n        * If the bar includes the limit price, then the limit price is used.\n        * Note that when buying the price is penetrated if it gets <= the limit price, and when selling the price\n          is penetrated if it gets >= the limit price\n    * A :class:`pyalgotrade.broker.StopOrder` will be filled like this:\n        * If the stop price was penetrated with the open price, then the open price is used.\n        * If the bar includes the stop price, then the stop price is used.\n        * Note that when buying the price is penetrated if it gets >= the stop price, and when selling the price\n          is penetrated if it gets <= the stop price\n    * A :class:`pyalgotrade.broker.StopLimitOrder` will be filled like this:\n        * If the stop price was penetrated with the open price, or if the bar includes the stop price, then the limit\n          order becomes active.\n        * If the limit order is active:\n            * If the limit order was activated in this same bar and the limit price is penetrated as well, then the\n              best between the stop price and the limit fill price (as described earlier) is used.\n            * If the limit order was activated at a previous bar then the limit fill price (as described earlier)\n              is used.\n\n    .. note::\n        * This is the default strategy used by the Broker.\n        * It uses :class:`pyalgotrade.broker.slippage.NoSlippage` slippage model by default.\n        * If volumeLimit is 0.25, and a certain bar's volume is 100, then no more than 25 shares can be used by all\n          orders that get processed at that bar.\n        * If using trade bars, then all the volume from that bar can be used.\n    "

    def __init__(self, volumeLimit=0.25):
        super(DefaultStrategy, self).__init__()
        self._DefaultStrategy__volumeLeft = {}
        self._DefaultStrategy__volumeUsed = {}
        self.setVolumeLimit(volumeLimit)
        self.setSlippageModel(slippage.NoSlippage())

    def onBars(self, broker_, bars):
        volumeLeft = {}
        for instrument in bars.getInstruments():
            bar = bars[instrument]
            if bar.getFrequency() == pyalgotrade.bar.Frequency.TRADE:
                volumeLeft[instrument] = bar.getVolume()
            else:
                if self._DefaultStrategy__volumeLimit is not None:
                    volumeLeft[instrument] = bar.getVolume() * self._DefaultStrategy__volumeLimit
            self._DefaultStrategy__volumeUsed[instrument] = 0.0

        self._DefaultStrategy__volumeLeft = volumeLeft

    def getVolumeLeft(self):
        return self._DefaultStrategy__volumeLeft

    def getVolumeUsed(self):
        return self._DefaultStrategy__volumeUsed

    def onOrderFilled(self, broker_, order):
        if self._DefaultStrategy__volumeLimit is not None:
            volumeLeft = order.getInstrumentTraits().roundQuantity(self._DefaultStrategy__volumeLeft[order.getInstrument()])
            fillQuantity = order.getExecutionInfo().getQuantity()
            assert volumeLeft >= fillQuantity, 'Invalid fill quantity %s. Not enough volume left %s' % (fillQuantity, volumeLeft)
            self._DefaultStrategy__volumeLeft[order.getInstrument()] = order.getInstrumentTraits().roundQuantity(volumeLeft - fillQuantity)
        self._DefaultStrategy__volumeUsed[order.getInstrument()] = order.getInstrumentTraits().roundQuantity(self._DefaultStrategy__volumeUsed[order.getInstrument()] + order.getExecutionInfo().getQuantity())

    def setVolumeLimit(self, volumeLimit):
        """
        Set the volume limit.

        :param volumeLimit: The proportion of the volume that orders can take up in a bar. Must be > 0 and <= 1.
            If None, then volume limit is not checked.
        :type volumeLimit: float
        """
        if volumeLimit is not None:
            if not (volumeLimit > 0 and volumeLimit <= 1):
                raise AssertionError('Invalid volume limit')
        self._DefaultStrategy__volumeLimit = volumeLimit

    def setSlippageModel(self, slippageModel):
        """
        Set the slippage model to use.

        :param slippageModel: The slippage model.
        :type slippageModel: :class:`pyalgotrade.broker.slippage.SlippageModel`
        """
        self._DefaultStrategy__slippageModel = slippageModel

    def __calculateFillSize(self, broker_, order, bar):
        ret = 0
        if self._DefaultStrategy__volumeLimit is not None:
            maxVolume = self._DefaultStrategy__volumeLeft.get(order.getInstrument(), 0)
            maxVolume = order.getInstrumentTraits().roundQuantity(maxVolume)
        else:
            maxVolume = order.getRemaining()
        if not order.getAllOrNone():
            ret = min(maxVolume, order.getRemaining())
        else:
            if order.getRemaining() <= maxVolume:
                ret = order.getRemaining()
        return ret

    def fillMarketOrder(self, broker_, order, bar):
        fillSize = self._DefaultStrategy__calculateFillSize(broker_, order, bar)
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
                price = self._DefaultStrategy__slippageModel.calculatePrice(order, price, fillSize, bar, self._DefaultStrategy__volumeUsed[order.getInstrument()])
            return FillInfo(price, fillSize)

    def fillLimitOrder(self, broker_, order, bar):
        fillSize = self._DefaultStrategy__calculateFillSize(broker_, order, bar)
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
            fillSize = self._DefaultStrategy__calculateFillSize(broker_, order, bar)
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
                price = self._DefaultStrategy__slippageModel.calculatePrice(order, price, fillSize, bar, self._DefaultStrategy__volumeUsed[order.getInstrument()])
            ret = FillInfo(price, fillSize)
        return ret

    def fillStopLimitOrder(self, broker_, order, bar):
        ret = None
        stopPriceTrigger = None
        if not order.getStopHit():
            stopPriceTrigger = get_stop_price_trigger(order.getAction(), order.getStopPrice(), broker_.getUseAdjustedValues(), bar)
            order.setStopHit(stopPriceTrigger is not None)
        if order.getStopHit():
            fillSize = self._DefaultStrategy__calculateFillSize(broker_, order, bar)
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