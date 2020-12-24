# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\broker\stopLossProfit_broker_3rdAccount.py
# Compiled at: 2020-04-20 23:45:04
# Size of source mod 2**32: 16089 bytes
"""

lw李文写的
模拟能够处理止盈止损指令的broker。
"""
from pyalgotrade.const import ORDER_TYPE, ORDER_STATUS, STOP_PROFIT_LOSS_ORDER_STATUS, POSITION_SIDE
from pyalgotrade.stoplossorder_3rdAccount import StopProfitOrder, StopLossOrder, trailingOrder
from gm.api import get_orders, OrderSide_Buy, OrderSide_Sell, PositionEffect_Open, PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday
from pyalgotrade import observer
from pyalgotrade.utils import createCusPositionFromGmPosition, cusPositionSideToGMPositionSide

class SimulationStopLossProfitBroker:

    def __init__(self, bTestID, positionObj=None, orderLog=None, stopOrderLog=None, subfunList=None, unsubfunList=None):
        self.bTestID = bTestID
        self.orderLog = orderLog
        self.stopOrderLog = stopOrderLog
        self._stoploss_orders = []
        self._condition_orders_dict = {}
        self._positions = positionObj
        self.stoplossOrderCreatedEvent = observer.Event()

    def setOrderLog(self, orderLog):
        self.orderLog = orderLog

    def setStopOrderLog(self, stopOrderLog):
        self.stopOrderLog = stopOrderLog

    def setPositions(self, positionsObj):
        self._positions = positionsObj

    def getSLOrdersSymbols(self):
        return set(list(self._condition_orders_dict.keys()))

    def getConditionOrders(self):
        return self._condition_orders_dict

    def addStopOrder(self, o):
        sym = o.getSymbol()
        if sym not in self._condition_orders_dict:
            self._condition_orders_dict[sym] = []
        self._condition_orders_dict[sym].append(o)

    def deleteSLOrders(self, sym):
        currSymOrders = self._condition_orders_dict[sym]
        self._condition_orders_dict[sym] = [o for o in currSymOrders if not o.is_final()]

    def deleteOrdersBySpecialHolding(self, sym, side_):
        currSymOrders = self._condition_orders_dict.setdefault(sym, [])
        self._condition_orders_dict[sym] = [o for o in currSymOrders if o.getOrderPositionObj().getPositionSide() != side_]
        print(currSymOrders)
        for o in currSymOrders:
            print(o.getOrderPositionObj().getPositionSide())

        print('deletPositonOrder: ', sym, ' ', side_)
        print('now curr sym orders: ', self._condition_orders_dict.setdefault(sym, []))

    def getSLOrders(self, sym):
        currSymOrders = self._condition_orders_dict.setdefault(sym, [])
        return currSymOrders

    def ontick(self, tick, context=None):
        asymbol = tick.symbol
        matchOrders = self._condition_orders_dict.setdefault(asymbol, [])
        for aspOrder in matchOrders:
            aspOrder.on_tick_hq(tick, context=context)

        self.deleteSLOrders(asymbol)

    def onbar(self, bar, context=None):
        asymbol = bar.symbol
        matchOrders = self._condition_orders_dict.setdefault(asymbol, [])
        for aspOrder in matchOrders:
            aspOrder.on_bar_hq(bar, context=context)

        self.deleteSLOrders(asymbol)

    def onOrderRsp(self, gmOrderObj, context):
        if gmOrderObj.positionEffect in [PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday]:
            symbol_ = gmOrderObj.symbol
            side_ = gmOrderObj.getPositionSide()
            gmside = cusPositionSideToGMPositionSide(side_)
            gmposi = context.account().position(symbol_, gmside)
            if gmposi is None:
                for aOrders in self._stoploss_orders:
                    if symbol_ == aOrders.getSymbol() and side_ == aOrders.getOrderPositionObj().getPositionSide():
                        aOrders.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED)

                self.deleteSLOrders()
        if gmOrderObj.positionEffect in [PositionEffect_Open]:
            symbol_ = gmOrderObj.symbol
            side_ = gmOrderObj.getPositionSide()
            gmside = cusPositionSideToGMPositionSide(side_)
            gmposi = context.account().position(symbol_, gmside)
            if gmposi is None:
                print(symbol_, ' ', gmside, ' ', gmOrderObj.positionEffect, ' ', gmOrderObj.created_at)
            if gmposi:
                if gmposi['available'] > 0:
                    aposi = createCusPositionFromGmPosition(gmposi)
                    context._createSOrder(aposi, context.bTestParams, self, context.now.strftime('%Y-%m-%d %H:%M:%S'))

    def onTradeRsp(self, gmTrade, context, account=None):
        positionSide_ = gmTrade.getTargetPositionSide()
        symbol_ = gmTrade.getSymbol()
        side_ = gmTrade.getSide()
        cusposi = self._positions.getHolding(symbol_, str(positionSide_))
        if gmTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
         PositionEffect_CloseYesterday]:
            if cusposi is None:
                currsymOrders = self.getSLOrders(symbol_)
                for aOrders in currsymOrders:
                    if symbol_ == aOrders.getSymbol() and side_ == aOrders.getOrderPositionObj().getPositionSide():
                        aOrders.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED)

                self.deleteOrdersBySpecialHolding(symbol_, positionSide_)
        if gmTrade.getPositionEffect() in [PositionEffect_Open]:
            gmposi = context.account().position(symbol_, positionSide_)
            self._positions.setAvailableVolume(symbol_, positionSide_, gmposi['available'])
            cusposi = self._positions.getHolding(symbol_, str(positionSide_))
            if cusposi is None:
                print('stopOrder on tradeRsp  ', symbol_, ' ', positionSide_, ' ', gmTrade.getPositionEffect(), ' ', gmTrade.getTradeTime())
            if cusposi:
                if cusposi.getAvailableVolume() > 0:
                    self.deleteOrdersBySpecialHolding(symbol_, positionSide_)
                    context._createSOrder(cusposi, context.bTestParams, self, context.now.strftime('%Y-%m-%d %H:%M:%S'))

    def create_stop_order(self, aOrderPosition, stopThresh, currhqDateTime, stopCommand='stoploss', orderType=2, subfunList=[], unsubfunList=[]):
        if stopCommand == 'stoploss':
            o = StopLossOrder.__from_create__(aOrderPosition, 'percent', stopThresh, order_type=orderType, orderLog=(self.orderLog))
            if self.stopOrderLog is not None:
                orderInfo = o.getOrderInfo()
                msgStr = 'stopLoss  symbol:' + orderInfo['symbol'] + ' cost:' + str(round(orderInfo['cost'], 2)) + ' clearPrice:' + str(round(orderInfo['clearPrice'], 2)) + ' posiVol:' + str(orderInfo['posiNum']) + ' status:' + orderInfo['status'].value
                self.stopOrderLog.info('%s,%s', currhqDateTime, msgStr)
        if stopCommand == 'stopprofit':
            o = StopProfitOrder.__from_create__(aOrderPosition, 'percent', stopThresh, order_type=orderType, orderLog=(self.orderLog))
            if self.stopOrderLog is not None:
                orderInfo = o.getOrderInfo()
                msgStr = 'stopProfit  symbol:' + orderInfo['symbol'] + ' cost:' + str(round(orderInfo['cost'], 2)) + ' clearPrice:' + str(round(orderInfo['clearPrice'], 2)) + ' posiVol:' + str(orderInfo['posiNum']) + ' status:' + orderInfo['status'].value
                self.stopOrderLog.info('%s,%s', currhqDateTime, msgStr)
        self._subHQ(o.getSymbol(), subfunList)
        self._unsubHQ(o, unsubfunList)
        self.addStopOrder(o)

    def _subHQ(self, symbol, subfunList):
        for afun in subfunList:
            afun(symbol)

    def _unsubHQ(self, o, unsubfunList):
        for afun in unsubfunList:
            o.getOrderInvalidEvent().subscribe(afun)

    def create_trailing_order(self, aOrderPosition, trailing_type, trailingThresh, stop_type, stopThresh, currhqDateTime, subfunList=[], unsubfunList=[], orderType=2):
        o = trailingOrder(aOrderPosition, stop_type, stopThresh, trailing_type, trailingThresh, currhqDateTime, order_type=orderType,
          orderLog=(self.orderLog))
        if self.stopOrderLog is not None:
            orderInfo = o.getOrderInfo()
            msgStr = 'stopTrailing  symbol:' + orderInfo['symbol'] + ' cost:' + str(round(orderInfo['cost'], 2)) + ' trailingPrice:' + str(round(orderInfo['trailingPrice'], 2)) + ' status:' + orderInfo['status'].value + ' posiVol:' + str(orderInfo['posiNum']) + ' hh:' + str(orderInfo['hh']) + ' ll:' + str(orderInfo['ll'])
            self.stopOrderLog.info('%s,%s', currhqDateTime, msgStr)
        self._subHQ(o.getSymbol(), subfunList)
        self._unsubHQ(o, unsubfunList)
        self.addStopOrder(o)