# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\stoplossorder.py
# Compiled at: 2019-11-15 23:55:54
# Size of source mod 2**32: 21164 bytes
import time
from decimal import Decimal
import numpy as np
from gm.api import get_orders, OrderSide_Buy, OrderSide_Sell, PositionEffect_Open, PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday
from gm.api import OrderStatus_Filled
from pyalgotrade.const import STOP_PROFIT_LOSS_ORDER_STATUS, ORDER_STATUS
from pyalgotrade import gm3HelpBylw
from functools import partial
from pyalgotrade.utils import id_gen
from pyalgotrade import observer
from pyalgotrade.const import ORDER_TYPE, ORDER_STATUS, STOP_PROFIT_LOSS_ORDER_STATUS, POSITION_SIDE
import abc

class riskStopOrder:
    order_id_gen = id_gen(int(time.time()) * 10000)

    def __init__(self):
        self._order_id = None
        self.orderLog = None
        self.target_order_position = None
        self._targetSymbol = None
        self._stop_type = None
        self._stop_gap = None
        self._target_order_cost = None
        self._clear_price = None
        self._status = None

    @classmethod
    def __from_create__(cls, target_order_position, stop_type, stop_gap, orderLog=None):
        stop_loss_order = cls()
        stop_loss_order.orderLog = orderLog
        stop_loss_order._stop_loss_order_id = next(cls.order_id_gen)
        stop_loss_order.target_order_position = target_order_position
        stop_loss_order._targetSymbol = target_order_position.symbol
        stop_loss_order._stop_type = stop_type
        stop_loss_order._stop_gap = stop_gap
        stop_loss_order._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
        stop_loss_order._target_order_cost = target_order_position.vwap
        stop_loss_order.init_excute_fun()
        target_order_position.positionClearedEvent.subscribe(stop_loss_order.onPositionClear)
        target_order_position.set_start_stop_position(True)
        return stop_loss_order

    @abc.abstractmethod
    def init_excute_fun(self):
        raise NotImplementedError

    def onPositionClear(self):
        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def is_final(self):
        return self._status in {
         STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED}


class StopLossOrder(riskStopOrder):

    def __init__(self):
        super(StopLossOrder, self).__init__()

    def init_excute_fun(self):
        if self.target_order_position.positionSide == POSITION_SIDE.LONG:
            if self._stop_type == 'percent':
                self._clear_price = self._target_order_cost * (1 - self._stop_gap)
                signalName = 'stopLoss-cLong'
                self._excute_fun = partial((gm3HelpBylw.gmOrder.clearLong), (self._targetSymbol), (self.target_order_position.volume),
                  signalName,
                  orderlog=(self.orderLog))
        if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
            if self._stop_type == 'percent':
                self._clear_price = self._target_order_cost * (1 + self._stop_gap)
                signalName = 'stopLoss-cShort'
                self._excute_fun = partial((gm3HelpBylw.gmOrder.clearShort), (self._targetSymbol), (self.target_order_position.volume),
                  signalName,
                  orderlog=(self.orderLog))

    def on_tick_hq(self, tick_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
                if tick_.price >= self._clear_price:
                    context.clearPositionSignalNames = [
                     self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
            if self.target_order_position.positionSide == POSITION_SIDE.LONG:
                if tick_.price <= self._clear_price:
                    context.clearPositionSignalNames = [
                     self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED


class StopProfitOrder(riskStopOrder):

    def __init__(self):
        super(StopProfitOrder, self).__init__()

    def init_excute_fun(self):
        if self.target_order_position.positionSide == POSITION_SIDE.LONG:
            if self._stop_type == 'percent':
                self._clear_price = self._target_order_cost * (1 + self._stop_gap)
                signalName = 'stopProfit-cLong'
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearLong, self._targetSymbol, self.target_order_position.volume, signalName)
        if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
            if self._stop_type == 'percent':
                self._clear_price = self._target_order_cost * (1 - self._stop_gap)
                signalName = 'stopProfit-cShort'
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol, self.target_order_position.volume, signalName)

    def on_tick_hq(self, tick_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
                if tick_.price <= self._clear_price:
                    context.clearPositionSignalNames = [
                     self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
            if self.target_order_position.positionSide == POSITION_SIDE.LONG:
                if tick_.price >= self._clear_price:
                    context.clearPositionSignalNames = [
                     self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED


def stop_loss_by_order(target_order_position, stop_type, stop_gap):
    stopLossOrder = StopLossOrder.__from_create__(target_order_position, stop_type=stop_type,
      stop_gap=stop_gap)
    return stopLossOrder


class trailingOrder:
    order_id_gen = id_gen(int(time.time()) * 10000)

    def __init__(self, target_order_position, stop_type, stop_gap, trailing_type, trailing_gap, order_type=2, orderLog=None):
        self.ordrLog = orderLog
        self._stop_loss_order_id = next(trailingOrder.order_id_gen)
        self.target_order_position = target_order_position
        self._targetSymbol = target_order_position.symbol
        self._stop_type = stop_type
        self._stop_gap = stop_gap
        self._trailing_type = trailing_type
        self._trailing_gap = trailing_gap
        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING
        self._target_order_cost = target_order_position.vwap
        if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_order_cost * (1 - self._trailing_gap)
        if self.target_order_position.positionSide == POSITION_SIDE.LONG:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_order_cost * (1 + self._trailing_gap)
        target_order_position.positionClearedEvent.subscribe(self.onPositionClear)
        target_order_position.set_start_stop_position(True)

    def onPositionClear(self):
        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def on_tick_hq(self, tick_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
                if self._stop_type == 'percent':
                    clear_price = self._ll * (1 + self._stop_gap)
                if tick_.price >= clear_price:
                    context.clearPositionSignalNames = [
                     self.target_order_position.postionSigalName]
                    gm3HelpBylw.gmOrder.clearShort((self._targetSymbol), (self.target_order_position.volume), 'trailing-cshort',
                      (tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), orderLog=(self.ordrLog))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
            if self.target_order_position.positionSide == POSITION_SIDE.LONG:
                if self._stop_type == 'percent':
                    clear_long_price = self._hh * (1 - self._stop_gap)
                if tick_.price <= clear_long_price:
                    context.clearPositionSignalNames = [
                     self.target_order_position.postionSigalName]
                    gm3HelpBylw.gmOrder.clearLong((self._targetSymbol), (self.target_order_position.volume), 'trailing-clong',
                      (tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), orderLog=(self.ordrLog))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
            self._hh = max(self._hh, tick_.price)
            self._ll = min(self._ll, tick_.price)
        elif self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.TRAILING:
            if self.target_order_position.positionSide == POSITION_SIDE.SHORT:
                if tick_.price <= self.trailing_target_price:
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
                    self._hh = tick_.price
                    self._ll = tick_.price
            if self.target_order_position.positionSide == POSITION_SIDE.LONG:
                if tick_.price >= self.trailing_target_price:
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
                    self._hh = tick_.price
                    self._ll = tick_.price

    def is_final(self):
        return self._status in {
         STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED}


class tradeOrder:

    def __init__(self, orderID, symbol, quantity, side, type, position_effect, signalName):
        self.orderID = orderID
        self.signalName = signalName
        self.symbol = symbol
        self.volume = quantity
        self.side = side
        self.type = type
        self.position_effect = position_effect
        self.gm_filled_volume = 0
        self.gm_filled_vwap = 0
        self.filled_volume = 0
        self.filled_vwap = 0
        self.avgPriceWithCost = 0
        self.cost = 0
        self.status = ORDER_STATUS.PENDING_NEW
        self.orderTotalFIlledEvent = observer.Event()

    def fill(self, tradeDict):
        if not self.status != ORDER_STATUS.FILLED:
            raise AssertionError
        else:
            quantity = tradeDict['volume']
            assert self.filled_volume + quantity <= tradeDict['volume']
            new_quantity = self.filled_volume + quantity
            self.filled_vwap = (self.filled_vwap * self.filled_volume + tradeDict['price'] * quantity) / new_quantity
            self.cost += tradeDict['commission'] + tradeDict['tax']
            self.filled_volume = new_quantity
            self.avgPriceWithCost = (self.filled_vwap * self.filled_volume + self.cost) / self.filled_volume
            if self.volume - self.filled_volume == 0:
                self.status = ORDER_STATUS.FILLED
                self.orderTotalFIlledEvent.emit(self)

    def is_final(self):
        return self.status in {
         ORDER_STATUS.FILLED}


class OrderHoldingPostion:

    def __init__(self, order_, createTime=None):
        if not order_.status == ORDER_STATUS.FILLED:
            raise AssertionError
        else:
            self.orderId = order_.orderID
            orderSignalList = order_.signalName.split('-')
            self.postionSigalName = orderSignalList[0]
            self.postionSigalAction = orderSignalList[1]
            self.symbol = order_.symbol
            if order_.side == OrderSide_Buy:
                self.positionSide = POSITION_SIDE.LONG
            if order_.side == OrderSide_Sell:
                self.positionSide = POSITION_SIDE.SHORT
        self.volume = order_.filled_volume
        self.vwap = order_.filled_vwap
        self.avgPriceWithCost = order_.avgPriceWithCost
        self.cost = order_.cost
        self._OrderHoldingPostion__barsSinceEntry = None
        self._OrderHoldingPostion__createTime = createTime
        self.clearOrderID = []
        self.positionClearedEvent = observer.Event()
        self.start_stop_position = False
        self.startStopEvent = observer.Event()

    def set_start_stop_position(self, boolFlag):
        if boolFlag:
            if not self.start_stop_position:
                self.startStopEvent.emit(self.symbol)
                self.start_stop_position = True

    def onClearOrder(self, clearGmOrderObj, clearPositionSignalNames):
        if not clearGmOrderObj.position_effect in [PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday]:
            raise AssertionError
        else:
            if self.positionSide == POSITION_SIDE.LONG:
                if clearGmOrderObj.symbol == self.symbol:
                    if clearPositionSignalNames[0] == 'allLong' or self.postionSigalName in clearPositionSignalNames:
                        self.clearOrderID.append(clearGmOrderObj.cl_ord_id)
            if self.positionSide == POSITION_SIDE.SHORT:
                if clearGmOrderObj.symbol == self.symbol:
                    if clearPositionSignalNames[0] == 'allShort' or self.postionSigalName in clearPositionSignalNames:
                        self.clearOrderID.append(clearGmOrderObj.cl_ord_id)

    def onTrade(self, tradedict):
        if len(self.clearOrderID) != 0:
            if tradedict['orderID'] in self.clearOrderID:
                if not tradedict['position_effect'] in [PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday]:
                    raise AssertionError
                else:
                    if not tradedict['symbol'] == self.symbol:
                        raise AssertionError
                    elif self.positionSide == POSITION_SIDE.LONG:
                        if tradedict['side'] != OrderSide_Sell:
                            i = 1
                    else:
                        assert tradedict['side'] == OrderSide_Sell
                        if self.positionSide == POSITION_SIDE.SHORT:
                            assert tradedict['side'] == OrderSide_Buy
                    assert self.volume >= tradedict['volume']
                self.volume = self.volume - tradedict['volume']
                if self.volume == 0:
                    self.positionClearedEvent.emit()