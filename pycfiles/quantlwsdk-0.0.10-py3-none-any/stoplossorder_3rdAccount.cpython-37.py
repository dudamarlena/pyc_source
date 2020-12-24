# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\stoplossorder_3rdAccount.py
# Compiled at: 2020-04-18 02:01:31
# Size of source mod 2**32: 27071 bytes
"""

本模块，针对第三方账户系统。即账户系统 由掘金或者其他平台提供。账户的持仓等字段，不由自己维护，由他们维护

"""
import time
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
        self.target_order_position = None
        self._targetSymbol = None
        self._stop_type = None
        self._stop_gap = None
        self._order_type = None
        self._target_posi_cost = None
        self._clear_price = None
        self._signalName = None
        self._status = None
        self.orderInvalidEvent = observer.Event()

    def getOrderInvalidEvent(self):
        return self.orderInvalidEvent

    def setStatus(self, status):
        self._status = status
        if self.is_final():
            self.orderInvalidEvent.emit(self._targetSymbol)

    def getSymbol(self):
        return self._targetSymbol

    def getOrderPositionObj(self):
        return self.target_order_position

    def getOrderInfo(self):
        infodict = {}
        infodict['symbol'] = self._targetSymbol
        infodict['cost'] = self._target_posi_cost
        infodict['clearPrice'] = self._clear_price
        infodict['status'] = self._status
        infodict['posiNum'] = self.target_order_position.getVolume()
        return infodict

    @classmethod
    def __from_create__(cls, target_order_position, stop_type, stop_gap, orderLog=None, order_type=2):
        stop_loss_order = cls()
        stop_loss_order.orderLog = orderLog
        stop_loss_order._stop_loss_order_id = next(cls.order_id_gen)
        stop_loss_order.target_order_position = target_order_position
        stop_loss_order._targetSymbol = target_order_position.getSymbol()
        stop_loss_order._stop_type = stop_type
        stop_loss_order._stop_gap = stop_gap
        stop_loss_order._order_type = order_type
        stop_loss_order._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
        stop_loss_order._target_posi_cost = target_order_position.getVwap()
        stop_loss_order.init_excute_fun()
        return stop_loss_order

    @abc.abstractmethod
    def _prePareMsg(self):
        raise NotImplementedError

    def init_excute_fun(self):
        self._prePareMsg()
        if self.target_order_position.getPositionSide() == 1:
            if self._order_type == 2:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearLong, self._targetSymbol, self.target_order_position.getAvailableVolume(), self._signalName)
            if self._order_type == 1:
                self._excute_fun = partial((gm3HelpBylw.gmOrder.clearLong), (self._targetSymbol), (self.target_order_position.getAvailableVolume()),
                  (self._signalName),
                  orderType=(self._order_type), price=(self._clear_price))
        if self.target_order_position.getPositionSide() == 2:
            if self._order_type == 2:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol, self.target_order_position.getAvailableVolume(), self._signalName)
            if self._order_type == 1:
                self._excute_fun = partial((gm3HelpBylw.gmOrder.clearShort), (self._targetSymbol), (self.target_order_position.getAvailableVolume()),
                  (self._signalName),
                  orderType=(self._order_type), price=(self._clear_price))

    def is_final(self):
        return self._status in {
         STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED}


class StopLossOrder(riskStopOrder):

    def __init__(self):
        super(StopLossOrder, self).__init__()

    def _prePareMsg(self):
        if self.target_order_position.getPositionSide() == 1:
            self._signalName = 'stopLoss-cLong'
            if self._stop_type == 'percent':
                self._clear_price = self._target_posi_cost * (1 - self._stop_gap)
        if self.target_order_position.getPositionSide() == 2:
            self._signalName = 'stopLoss-cShort'
            if self._stop_type == 'percent':
                self._clear_price = self._target_posi_cost * (1 + self._stop_gap)

    def on_tick_hq(self, tick_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            if self.target_order_position.getPositionSide() == 2:
                if tick_.price >= self._clear_price:
                    gmorderRe = self._excute_fun((tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
            if self.target_order_position.getPositionSide() == 1:
                if tick_.price <= self._clear_price:
                    gmorderRe = self._excute_fun((tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

    def on_bar_hq(self, bar_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            if self.target_order_position.getPositionSide() == 2:
                if bar_.high >= self._clear_price:
                    gmorderRe = self._excute_fun((bar_.eob.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
            if self.target_order_position.getPositionSide() == 1:
                if bar_.low <= self._clear_price:
                    gmorderRe = self._excute_fun((bar_.eob.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)


class StopProfitOrder(riskStopOrder):

    def __init__(self):
        super(StopProfitOrder, self).__init__()

    def _prePareMsg(self):
        if self.target_order_position.getPositionSide() == 1:
            self._signalName = 'stopProfit-cLong'
            if self._stop_type == 'percent':
                self._clear_price = self._target_posi_cost * (1 + self._stop_gap)
        if self.target_order_position.getPositionSide() == 2:
            self._signalName = 'stopProfit-cShort'
            if self._stop_type == 'percent':
                self._clear_price = self._target_posi_cost * (1 - self._stop_gap)

    def on_tick_hq(self, tick_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            danghq_1 = tick_.quotes[0]
            if self.target_order_position.getPositionSide() == 2:
                if 'bid_p' not in danghq_1:
                    return
                if tick_.price <= self._clear_price:
                    gmorderRe = self._excute_fun((tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
            if self.target_order_position.getPositionSide() == 1:
                if 'ask_p' not in danghq_1:
                    return
                if tick_.price >= self._clear_price:
                    gmorderRe = self._excute_fun((tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

    def on_bar_hq(self, bar_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            if self.target_order_position.getPositionSide() == 2:
                if bar_.low <= self._clear_price:
                    gmorderRe = self._excute_fun((bar_.eob.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
            if self.target_order_position.getPositionSide() == 1:
                if bar_.high >= self._clear_price:
                    gmorderRe = self._excute_fun((bar_.eob.strftime('%Y-%m-%d %H:%M:%S')), context=context, orderLog=(context.orderLog))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)


def stop_loss_by_order(target_order_position, stop_type, stop_gap):
    stopLossOrder = StopLossOrder.__from_create__(target_order_position, stop_type=stop_type,
      stop_gap=stop_gap)
    return stopLossOrder


class trailingOrder:
    order_id_gen = id_gen(int(time.time()) * 10000)

    def __init__(self, target_order_position, stop_type, stop_gap, trailing_type, trailing_gap, currhqDateTime, order_type=2, orderLog=None):
        self.orderInvalidEvent = observer.Event()
        self._stop_loss_order_id = next(trailingOrder.order_id_gen)
        self.target_order_position = target_order_position
        self._order_type = order_type
        self._targetSymbol = target_order_position.getSymbol()
        self._stop_type = stop_type
        self._stop_gap = stop_gap
        self._trailing_type = trailing_type
        self._trailing_gap = trailing_gap
        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING
        self._target_posi_cost = target_order_position.getVwap()
        if self.target_order_position.getPositionSide() == 2:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_posi_cost * (1 - self._trailing_gap)
        if self.target_order_position.getPositionSide() == 1:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_posi_cost * (1 + self._trailing_gap)
        self._hh = None
        self._ll = None
        self.setRealStatus(currhqDateTime)

    def getSymbol(self):
        return self._targetSymbol

    def getOrderPositionObj(self):
        return self.target_order_position

    def getOrderInvalidEvent(self):
        return self.orderInvalidEvent

    def setStatus(self, status):
        self._status = status
        if self.is_final():
            self.orderInvalidEvent.emit(self._targetSymbol)

    def setRealStatus(self, currhqDateTime):
        dt = self.target_order_position.getUpdateTime().strftime('%Y-%m-%d %H:%M:%S')
        dtnow = currhqDateTime
        hq = gm3HelpBylw.getHQData_Fade([self._targetSymbol], dt, dtnow)
        if hq.empty:
            return
        hh = hq['high'].max()
        ll = hq['low'].min()
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING:
            if self.target_order_position.getPositionSide() == 2:
                if ll <= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = hh
                    self._ll = ll
            if self.target_order_position.getPositionSide() == 1:
                if hh >= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = hh
                    self._ll = ll

    def on_tick_hq(self, tick_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE:
            if self.target_order_position.getPositionSide() == 2:
                if self._stop_type == 'percent':
                    clear_price = self._ll * (1 + self._stop_gap)
                if tick_.price >= clear_price:
                    if self._order_type == 2:
                        gm3HelpBylw.gmOrder.clearShort((self._targetSymbol), (self.target_order_position.getAvailableVolume()), 'trailing-cshort',
                          (tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), orderLog=(context.orderLog), context=context)
                    if self._order_type == 1:
                        gm3HelpBylw.gmOrder.clearShort((self._targetSymbol), (self.target_order_position.getAvailableVolume()), 'trailing-cshort',
                          (tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')),
                          orderType=(self._order_type),
                          price=clear_price,
                          orderLog=(context.orderLog),
                          context=context)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
            if self.target_order_position.getPositionSide() == 1:
                if self._stop_type == 'percent':
                    clear_long_price = self._hh * (1 - self._stop_gap)
                if tick_.price <= clear_long_price:
                    if self._order_type == 2:
                        gm3HelpBylw.gmOrder.clearLong((self._targetSymbol), (self.target_order_position.getAvailableVolume()), 'trailing-clong',
                          (tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), orderLog=(context.orderLog), context=context)
                    if self._order_type == 1:
                        gm3HelpBylw.gmOrder.clearLong((self._targetSymbol), (self.target_order_position.getAvailableVolume()), 'trailing-clong',
                          (tick_.created_at.strftime('%Y-%m-%d %H:%M:%S')), orderType=(self._order_type),
                          price=clear_long_price,
                          orderLog=(context.orderLog),
                          context=context)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
                self._hh = max(self._hh, tick_.price)
                self._ll = min(self._ll, tick_.price)
            else:
                pass
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING:
            if self.target_order_position.getPositionSide() == 2:
                if tick_.price <= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = tick_.price
                    self._ll = tick_.price
            if self.target_order_position.getPositionSide() == 1:
                if tick_.price >= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = tick_.price
                    self._ll = tick_.price

    def on_bar_hq(self, bar_, context=None):
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE:
            if self.target_order_position.getPositionSide() == 2:
                if self._stop_type == 'percent':
                    clear_price = self._ll * (1 + self._stop_gap)
                if bar_.high >= clear_price:
                    gm3HelpBylw.gmOrder.clearShort((self._targetSymbol), (self.target_order_position.getAvailableVolume()), 'trailing-cshort',
                      (bar_.eob.strftime('%Y-%m-%d %H:%M:%S')), orderLog=(context.orderLog), context=context)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
                elif self.target_order_position.getPositionSide() == 1:
                    if self._stop_type == 'percent':
                        clear_long_price = self._hh * (1 - self._stop_gap)
                    if bar_.low <= clear_long_price:
                        gm3HelpBylw.gmOrder.clearLong((self._targetSymbol), (self.target_order_position.getAvailableVolume()), 'trailing-clong',
                          (bar_.eob.strftime('%Y-%m-%d %H:%M:%S')), orderLog=(context.orderLog), context=context)
                        self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)
                self._hh = max(self._hh, bar_.high)
                self._ll = min(self._ll, bar_.low)
            else:
                pass
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING:
            if self.target_order_position.getPositionSide() == 2:
                if bar_.low <= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = bar_.high
                    self._ll = bar_.low
            if self.target_order_position.getPositionSide() == 1:
                if bar_.high >= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = bar_.high
                    self._ll = bar_.low

    def getOrderInfo(self):
        infodict = {}
        infodict['symbol'] = self._targetSymbol
        infodict['cost'] = self._target_posi_cost
        infodict['trailingPrice'] = self.trailing_target_price
        infodict['status'] = self._status
        infodict['posiNum'] = self.target_order_position.getVolume()
        infodict['hh'] = self._hh
        infodict['ll'] = self._ll
        return infodict

    def is_final(self):
        return self._status in {
         STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED}