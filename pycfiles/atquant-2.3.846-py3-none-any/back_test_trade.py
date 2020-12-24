# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\trade\back_test_trade.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 39768 bytes
import numpy as np, pandas as pd, atquant.api as API, atquant.data.basic_data as bd, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR, atquant.utils.internal_util as UTILS_UTIL
from atquant.data.const_data import GACV
from atquant.run_mode import trader_run_back_test
from atquant.utils.internal_exception import ToolBoxErrors

def TradeOrder(orderIDA, barHighA, barLowA, barOpenA, barVolA, targetPriceAssign=None, filledTimeAssign=None):
    """
    模拟券商的功能，冻结保证金，手续费，多空仓位等等，
    模拟交易所的功能，根据下单的价格是否在当前bar的最高价和最低价之间进行判断是否进行交易

    :param orderIDA: numpy.ndarray, 订单号
    :param barHighA: numpy.ndarray, 高
    :param barLowA: numpy.ndarray, 低
    :param barOpenA: numpy.ndarray, 开
    :param barVolA: numpy.ndarray, 成交量
    :param targetPriceAssign: numpy.ndarray, 
    :param filledTimeAssign: numpy.ndarray,
    :return: numpy.ndarry 
    """
    orderIDA = orderIDA.ravel()
    orderStatus = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderIDA)]
    preHoldP = orderStatus == GACV.OrderStatus_PreHolding
    zeroOpenFPP = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OpenFrozenPrice, orderIDA)] == 0
    setP = np.logical_and(preHoldP, zeroOpenFPP)
    if setP.any():
        GVAR.g_ATraderSimOrders[(GACV.SimOrder_OpenFrozenPrice, orderIDA[setP])] = barOpenA[setP]
    _t = GVAR.g_ATraderSimOrders[:, orderIDA].reshape((-1, orderIDA.size))
    marginFrozen, feeFrozen = OrderMarginFee(_t)
    Info_df = API.traderGetFutureInfoV2(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderIDA)])
    for i in range(orderIDA.size):
        tradePrice = 0
        orderID = orderIDA[i]
        barHigh = barHighA[i]
        barLow = barLowA[i]
        barOpen = barOpenA[i]
        barVol = barVolA[i]
        if orderStatus[i] == GACV.OrderStatus_Cancelled:
            pass
        elif barVol < 1:
            if not GVAR.g_ATraderMarketOrderHolding and GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderCtg, orderID)] == GACV.OrderCtg_Market:
                GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Cancelled
                orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
            continue
            if targetPriceAssign is not None and targetPriceAssign.size > 0:
                if filledTimeAssign is None or filledTimeAssign.size < 1:
                    raise ValueError('filledTimeAssign is None or filledTimeAssign.size<1')
                targetPrice = targetPriceAssign.ravel()[i]
                filledTime = filledTimeAssign.ravel()[i]
            else:
                targetPrice = np.nan
                filledTime = GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderSimCurBarFresh - 1)]
            if GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] == GACV.OrderStatus_PreHolding:
                if barOpen == 0:
                    GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Denied
                    orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                    continue
                    ContractLimit = 2000000000.0
                    if ContractLimit < GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)]:
                        GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Denied
                        orderStatus[i] = GACV.OrderStatus_Denied
                        continue
                else:
                    if atIsStockV2(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderID)]) and GACV.OffsetFlag_Open == GVAR.g_ATraderSimOrders[(GACV.SimOrder_OffsetFlag, orderID)] and np.fmod(GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)], 100):
                        GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Denied
                        orderStatus[i] = GACV.OrderStatus_Denied
                        continue
                    HandleIdx = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_HandleIdx, orderID)])
                    if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OffsetFlag, orderID)] == GACV.OffsetFlag_Open:
                        if GVAR.atGetTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_ValidCash) <= marginFrozen[i] + feeFrozen[i]:
                            GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Denied
                            orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                            continue
                        else:
                            GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_ValidCash, -(marginFrozen[i] + feeFrozen[i]))
                            GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_OrderFrozen, marginFrozen[i] + feeFrozen[i])
                    elif GVAR.g_ATraderSimOrders[(GACV.SimOrder_OffsetFlag, orderID)] == GACV.OffsetFlag_Close:
                        HandleIdx = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_HandleIdx, orderID)])
                        TargetIdx = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderID)]) + 1
                        if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)] == GACV.OrderAct_Buy:
                            if GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos) < GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)]:
                                GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Denied
                                orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                                continue
                            else:
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos, -GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)])
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortFrozen, GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)])
                        else:
                            if GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos) < GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)]:
                                GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Denied
                                orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                                continue
                            else:
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos, -GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)])
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongFrozen, GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)])
                        GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Holding
                        orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                    if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderCtg, orderID)] == GACV.OrderCtg_Limit:
                        orderAct = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)]
                        if barLow <= GVAR.g_ATraderSimOrders[(GACV.SimOrder_Price, orderID)] <= barHigh:
                            tradePrice = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Price, orderID)]
                            orderPrice = tradePrice
                        else:
                            if orderAct == GACV.OrderAct_Sell and GVAR.g_ATraderSimOrders[(GACV.SimOrder_Price, orderID)] < barLow or orderAct == GACV.OrderAct_Buy and GVAR.g_ATraderSimOrders[(GACV.SimOrder_Price, orderID)] > barHigh:
                                tradePrice = barOpen
                                orderPrice = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Price, orderID)]
                            elif bool(GVAR.g_ATraderLimitType):
                                GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Cancelled
                                orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                    else:
                        if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderCtg, orderID)] == GACV.OrderCtg_Market:
                            if np.isnan(targetPrice):
                                if GVAR.g_ATraderPriceLoc == 1:
                                    orderPrice = barOpen
                                else:
                                    if GVAR.g_ATraderPriceLoc == 0:
                                        _, _, _, orderPrice, _ = bd.GetFreshBarByOffset(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderID)], -1)
                                    else:
                                        orderPrice = barOpen
                                    orderAct = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)]
                                    if orderAct == GACV.OrderAct_Sell:
                                        tradePrice = orderPrice - GVAR.g_ATraderSlidePrice
                                    else:
                                        if orderAct == GACV.OrderAct_Buy:
                                            tradePrice = orderPrice + GVAR.g_ATraderSlidePrice
                                        else:
                                            ToolBoxErrors.unexpect_switch_error('orderact')
                                tradePrice = tradePrice - np.fmod(tradePrice, Info_df.iloc[:, i].loc['MinMove'])
                        else:
                            orderPrice = targetPrice
                            tradePrice = targetPrice - np.fmod(targetPrice, Info_df.iloc[:, i].loc['MinMove'])
                if tradePrice > 0:
                    GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Filled
                    GVAR.g_ATraderSimOrders[(GACV.SimOrder_Price, orderID)] = orderPrice
                    orderStatus[i] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)]
                    GVAR.g_ATraderSimOrders[(GACV.SimOrder_FilledTime, orderID)] = filledTime
                    temp_array = np.zeros((GVAR.atSimTradeItemsLen(), 1))
                    temp_array[GACV.SimTrade_FilledTime] = filledTime
                    temp_array[GACV.SimTrade_HandleIdx] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_HandleIdx, orderID)]
                    temp_array[GACV.SimTrade_OrderID] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderID, orderID)]
                    temp_array[GACV.SimTrade_TargetIdx] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderID)]
                    temp_array[GACV.SimTrade_Contracts] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)]
                    temp_array[GACV.SimTrade_Price] = tradePrice
                    temp_array[GACV.SimTrade_OrderCtg] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderCtg, orderID)]
                    temp_array[GACV.SimTrade_OrderAct] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)]
                    temp_array[GACV.SimTrade_OffsetFlag] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OffsetFlag, orderID)]
                    temp_array[GACV.SimTrade_OrderTag] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderTag, orderID)]
                    tradeIdx = GVAR.g_ATraderSimTrades.shape[1] if len(GVAR.g_ATraderSimTrades.shape) == 2 else 0
                    GVAR.g_ATraderSimTrades = UTILS_UTIL.append_or_assign_2d_array_axis1(GVAR.g_ATraderSimTrades, temp_array, tradeIdx)
                    HandleIdx = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_HandleIdx, orderID)])
                    TargetIdx = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderID)] + 1)
                    if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OffsetFlag, orderID)] == GACV.OffsetFlag_Open:
                        GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_OrderFrozen, -(marginFrozen[i] + feeFrozen[i]))
                        GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_MarginFrozen, marginFrozen[i])
                        order_contracts = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)]
                        if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)] == GACV.OrderAct_Buy:
                            long_frozen = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongFrozen)
                            long_avg = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongAvg)
                            long_pos = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos)
                            GVAR.atSetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongAvg, (long_avg * (long_pos + long_frozen) + tradePrice * order_contracts) / (long_pos + long_frozen + order_contracts))
                            GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos, order_contracts)
                        elif GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)] == GACV.OrderAct_Sell:
                            short_avg = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortAvg)
                            short_pos = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos)
                            short_frozen = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortFrozen)
                            GVAR.atSetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortAvg, (short_avg * (short_pos + short_frozen) + tradePrice * order_contracts) / (short_pos + short_frozen + order_contracts))
                            GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos, order_contracts)
                    else:
                        if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OffsetFlag, orderID)] == GACV.OffsetFlag_Close:
                            order_contracts = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, orderID)]
                            if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)] == GACV.OrderAct_Buy:
                                short_avg = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortAvg)
                                CloseMarginFrozen = short_avg * order_contracts * Info_df.iloc[:, i].loc['Multiple'] * Info_df.iloc[:, i].loc['ShortMargin']
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_MarginFrozen, -CloseMarginFrozen)
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_ValidCash, CloseMarginFrozen + (short_avg - tradePrice) * order_contracts * Info_df.iloc[:, i].loc['Multiple'] - feeFrozen[i])
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortFrozen, -order_contracts)
                                if GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortFrozen) + GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos) == 0:
                                    GVAR.atSetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortAvg, 0)
                                    EraseAccuracyError(HandleIdx)
                        else:
                            if GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, orderID)] == GACV.OrderAct_Sell:
                                long_avg = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongAvg)
                                CloseMarginFrozen = long_avg * order_contracts * Info_df.iloc[:, i].loc['Multiple'] * Info_df.iloc[:, i].loc['LongMargin']
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_MarginFrozen, -CloseMarginFrozen)
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_ValidCash, CloseMarginFrozen + (tradePrice - long_avg) * order_contracts * Info_df.iloc[:, i].loc['Multiple'] - feeFrozen[i])
                                GVAR.atAddTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongFrozen, -order_contracts)
                                if GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongFrozen) + GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos) == 0:
                                    GVAR.atSetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongAvg, 0)
                                    EraseAccuracyError(HandleIdx)
                            else:
                                raise ValueError(const_da.Enum_Const.ERROR_UNKNOW_OFFSETFLAG.value)
                            SetTargetPriceOfStopOrders(orderID, tradePrice)

    return orderStatus


def atIsStockV2(TargetIdxA):
    infos = API.traderGetTargetInfoV2(TargetIdxA)
    bIsStockA = np.all(infos.loc['Type'] == 1)
    return bIsStockA


def ClearUnfilledOrder():
    """
    清除前一天未完成的订单【将g_ATraderSimOrders中未完成的订单清除】，重置冻结资金
    """
    if GVAR.g_ATraderSimUnfilledOrders.size > 0:
        for i in range(len(GVAR.g_ATraderSimUnfilledOrders)):
            orderID = int(GVAR.g_ATraderSimUnfilledOrders[i])
            t_g_s_o_s = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)])
            if t_g_s_o_s in (GACV.OrderStatus_PreHolding, GACV.OrderStatus_Holding):
                GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, orderID)] = GACV.OrderStatus_Cancelled
            if GVAR.g_ATraderSimUnfiredStopOrders.size > 0:
                sOrderSameT = np.where(GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID] == orderID)[0]
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, sOrderSameT)] = GACV.StopOrderStatus_Cancelled
                GVAR.g_ATraderSimStopOrders = np.append(GVAR.g_ATraderSimStopOrders, GVAR.g_ATraderSimUnfiredStopOrders[:, sOrderSameT], axis=1)

        GVAR.g_ATraderSimUnfilledOrders = np.array([], dtype=np.int)
        GVAR.g_ATraderSimUnfiredStopOrders = np.array([], dtype=np.int)
    HandleLen, ItemLen, temp_tuple = GVAR.g_ATraderAccountMatrix.shape
    for i in range(HandleLen):
        for j in range(ItemLen):
            if j == 0:
                GVAR.atAddTraderAccountMatrixValue(i, 0, GACV.ACMatrix_ValidCash, GVAR.atGetTraderAccountMatrixValue(i, 0, GACV.ACMatrix_OrderFrozen))
            else:
                GVAR.atAddTraderAccountMatrixValue(i, j, GACV.ACMatrix_LongPos, GVAR.atGetTraderAccountMatrixValue(i, j, GACV.ACMatrix_LongFrozen))
                GVAR.atAddTraderAccountMatrixValue(i, j, GACV.ACMatrix_ShortPos, GVAR.atGetTraderAccountMatrixValue(i, j, GACV.ACMatrix_ShortFrozen))


def DealTrade():
    """
    交易处理主函数
    """
    filledOrderIdx = np.array([])
    filledOrderID = np.array([])
    DCOrderIdx = np.array([])
    GVAR.g_ATraderSimUnfilledOrders = GVAR.g_ATraderSimUnfilledOrders.astype(np.int)
    if GVAR.g_ATraderSimUnfilledOrders.size > 0:
        orderID = GVAR.g_ATraderSimUnfilledOrders.flatten().astype(np.int)
        barOpen, barHigh, barLow, barclose, barVol = bd.GetFreshBarByOffset(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, orderID)], 0)
        orderStatus = TradeOrder(orderID, barHigh, barLow, barOpen, barVol, np.array([]), np.array([]))
        Canceld = np.where(orderStatus == GACV.OrderStatus_Cancelled)[0]
        Filled = np.where(orderStatus == GACV.OrderStatus_Filled)[0]
        Denied = np.where(orderStatus == GACV.OrderStatus_Denied)[0]
        filledOrderIdx = Filled.astype(np.int64)
        DCOrderIdx = np.append(Canceld, values=Denied, axis=0)
    if DCOrderIdx.size > 0 and GVAR.g_ATraderSimUnfiredStopOrders.size > 0:
        dcOrderIDs = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderID, GVAR.g_ATraderSimUnfilledOrders[DCOrderIdx])]
        for targetOrderID in dcOrderIDs:
            sameTargetStopOrders = np.where(GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID] == targetOrderID)[0]
            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, sameTargetStopOrders)] = GACV.StopOrderStatus_Cancelled
            if GVAR.g_ATraderSimStopOrders.size < 1:
                GVAR.g_ATraderSimStopOrders = GVAR.g_ATraderSimUnfiredStopOrders[:, sameTargetStopOrders].copy()
            else:
                GVAR.g_ATraderSimStopOrders = np.append(GVAR.g_ATraderSimStopOrders, GVAR.g_ATraderSimUnfiredStopOrders[:, sameTargetStopOrders], axis=1)
            GVAR.g_ATraderSimUnfiredStopOrders = np.delete(GVAR.g_ATraderSimUnfiredStopOrders, sameTargetStopOrders, axis=1)

    if GVAR.g_ATraderSimOrders.size > 0 and filledOrderIdx.size > 0:
        filledOrderID = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderID, GVAR.g_ATraderSimUnfilledOrders[filledOrderIdx])]
    delete_idx = np.append(filledOrderIdx, values=DCOrderIdx, axis=0)
    GVAR.g_ATraderSimUnfilledOrders = np.delete(GVAR.g_ATraderSimUnfilledOrders, delete_idx)
    if GVAR.g_ATraderSimUnfiredStopOrders.size < 1:
        return
    TargetOrderIDs = pd.unique(GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID]).astype(np.int)
    TargetOrderIDs.sort()
    for targetOrder in TargetOrderIDs:
        if np.isnan(targetOrder):
            sameTargetStopOrdersPos = np.array([])
        else:
            sameTargetStopOrdersPos = np.where(GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID] == targetOrder)[0]
            barOpen, barHigh, barLow, _, barVol = bd.GetFreshBarByOffset(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, targetOrder)], 0)
        if barVol < 1:
            pass
        else:
            _t1 = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_HandleIdx, targetOrder)])
            _t2 = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, targetOrder)])
            _orderact = int(GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, targetOrder)])
            if _orderact == GACV.OrderAct_Buy:
                Position, _, _ = API.traderGetAccountPositionDirV2(_t1, _t2, 'Long')
            else:
                if _orderact == GACV.OrderAct_Sell:
                    Position, _, _ = API.traderGetAccountPositionDirV2(_t1, _t2, 'Short')
                else:
                    raise Exception(const_da.Enum_Const.ERROR_NOTSUPPORT_ORDER_DIRECT.value)
                mayFirePos, mustTickCheckPos = trader_run_back_test.JudgeStopOrdersByBar(barHigh, barLow, Position[(0,
                                                                                                                    0)], sameTargetStopOrdersPos)
                theFireOnePos = np.array([])
                _d = GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx]
                curBarTime = _d.Matrix[(GACV.KMatrixPos_TimeLine, _d.CurrentBar[GVAR.g_ATraderSimCurBarFresh])]
                if len(GVAR.g_ATraderSimUnfiredStopOrders.shape) != 2:
                    GVAR.g_ATraderSimUnfiredStopOrders = GVAR.g_ATraderSimUnfiredStopOrders.reshape((-1,
                                                                                                     1))
            if mustTickCheckPos.size >= 1 or mayFirePos.size >= 2 or mayFirePos.size > 0 and not bool(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBarBegin, int(mayFirePos[0]))]):
                if GVAR.g_ATraderStraInputInfo.KFrequencyI == GACV.KFreq_Tick and GVAR.g_ATraderStraInputInfo.KFreNum == 1:
                    theFireOnePos = mustTickCheckPos
                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_FireTime, theFireOnePos)] = curBarTime
                else:
                    _s = np.append(mustTickCheckPos, mayFirePos, axis=0).astype(np.int)
                    theFireOnePos, barOpen, barHigh, barLow, barVol = trader_run_back_test.JudgeStopOrdersByTick(_s)
            elif mayFirePos.size > 0:
                theFireOnePos = mayFirePos
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_FireTime, theFireOnePos)] = curBarTime
            if theFireOnePos.size > 0:
                orderID, targetPrice, fireTime = fireStopOrder(theFireOnePos)
                orderStatus = TradeOrder(orderID, barHigh, barLow, barOpen, barVol, targetPrice, fireTime)
                if orderStatus == GACV.OrderStatus_Cancelled or orderStatus == GACV.OrderStatus_Filled or orderStatus == GACV.OrderStatus_Denied:
                    filledOrderID = np.append(filledOrderID, [orderID])

    for i in range(len(filledOrderID)):
        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBarBegin, GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID] == filledOrderID[i])] = True

    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_IsBeginTrailing] == True)] = False


def fireStopOrder(stopOrderIdx):
    """
    将被触发的止盈止损单转换为order，并将此订单对应的止盈止损单全部清空
    
    :param stopOrderIdx: numpy.ndarray(1)
    :return: orderID,targetPrice
    ::
        
        orderID, numpy.ndarry(1*1),生成的订单号
        targetPrice numpy.ndarry(1*1),生成订单号的成交价
    ..
    """
    if isinstance(stopOrderIdx, np.ndarray):
        stopOrderIdx = int(stopOrderIdx.ravel()[0])
    else:
        stopOrderIdx = int(stopOrderIdx)
    orderID = GVAR.g_ATraderSimOrders.shape[1] if len(GVAR.g_ATraderSimOrders.shape) == 2 else 0
    fireTime = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_FireTime, stopOrderIdx)]
    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, stopOrderIdx)] = GACV.StopOrderStatus_Fired
    if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopOrderType, stopOrderIdx)] == GACV.StopOrderType_Trailing:
        targetPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderIdx)]
    else:
        targetPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderIdx)]
    temp_array = np.zeros((GVAR.atSimOrderItemsLen(),))
    temp_array[GACV.SimOrder_OrderID] = orderID
    temp_array[GACV.SimOrder_Price] = 0
    temp_array[GACV.SimOrder_OrderTag] = 0
    temp_array[GACV.SimOrder_FilledTime] = 0
    temp_array[GACV.SimOrder_OffsetFlag] = GACV.OffsetFlag_Close
    temp_array[GACV.SimOrder_Status] = GACV.OrderStatus_PreHolding
    temp_array[GACV.SimOrder_HandleIdx] = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_HandleIdx, stopOrderIdx)]
    temp_array[GACV.SimOrder_OrderTime] = fireTime
    temp_array[GACV.SimOrder_TargetIdx] = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetIdx, stopOrderIdx)]
    temp_array[GACV.SimOrder_Contracts] = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Contracts, stopOrderIdx)]
    temp_array[GACV.SimOrder_OrderCtg] = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderCtg, stopOrderIdx)]
    orderAct = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx)]
    temp_array[GACV.SimOrder_OrderAct] = GACV.OrderAct_Sell if orderAct == GACV.OrderAct_Buy else GACV.OrderAct_Buy
    temp_array[GACV.SimOrder_RemainNum] = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Contracts, stopOrderIdx)]
    if GVAR.g_ATraderSimOrders.size < 1 or len(GVAR.g_ATraderSimOrders.shape) != 2:
        GVAR.g_ATraderSimOrders = temp_array.reshape((-1, 1)).copy()
    else:
        GVAR.g_ATraderSimOrders = np.append(GVAR.g_ATraderSimOrders, temp_array.reshape((-1,
                                                                                         1)), axis=1)
    if not np.isnan(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetOrderID, stopOrderIdx)]):
        TargetOrderID = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetOrderID, stopOrderIdx)]
        sameTOrder = np.where(GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID] == TargetOrderID)[0]
        for i in range(len(sameTOrder)):
            if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, sameTOrder[i])] == GACV.StopOrderStatus_Holding:
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, sameTOrder[i])] = GACV.StopOrderStatus_Cancelled
            GVAR.g_ATraderSimStopOrders = UTILS_UTIL.append_or_assign_2d_array_axis1(GVAR.g_ATraderSimStopOrders, GVAR.g_ATraderSimUnfiredStopOrders[:, sameTOrder[i]], GVAR.g_ApendEnoughConstNum)

        GVAR.g_ATraderSimUnfiredStopOrders = np.delete(GVAR.g_ATraderSimUnfiredStopOrders, sameTOrder, axis=1)
    else:
        GVAR.g_ATraderSimStopOrders = UTILS_UTIL.append_or_assign_2d_array_axis1(GVAR.g_ATraderSimStopOrders, GVAR.g_ATraderSimUnfiredStopOrders[:, stopOrderIdx], GVAR.g_ApendEnoughConstNum)
        GVAR.g_ATraderSimUnfiredStopOrders = np.delete(GVAR.g_ATraderSimUnfiredStopOrders, stopOrderIdx, axis=1)
    return (np.array([orderID], dtype=np.int).ravel(), np.array([targetPrice]).ravel(), np.array([fireTime]).ravel())


def EraseAccuracyError(HandleIdx):
    _r = GVAR.g_ATraderAccountMatrix[HandleIdx, 1:, [GACV.ACMatrix_LongPos, GACV.ACMatrix_LongFrozen, GACV.ACMatrix_ShortPos, GACV.ACMatrix_ShortFrozen]]
    if ~np.any(np.any(_r, axis=1), axis=0):
        GVAR.atAddTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_ValidCash, GVAR.atGetTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_MarginFrozen))
        GVAR.atSetTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_MarginFrozen, 0)


def OrderMarginFee(order):
    """
    计算需要冻结的保证金以及手续费
    
    :param order: numpy.ndarray, 某一订单Id的数据 
    :return: marginFrozen, feeFrozen
    """
    orderLen = order.shape[1]
    margin = np.zeros((orderLen,))
    marginFrozen = np.zeros((orderLen,))
    feeFrozen = np.zeros((orderLen,))
    Info_df = API.traderGetFutureInfoV2(order[GACV.SimOrder_TargetIdx])
    buyP = np.array(np.equal(order[GACV.SimOrder_OrderAct], GACV.OrderAct_Buy))
    if buyP.size == 0:
        buyP = np.zeros((orderLen,), dtype=np.bool)
    InfoBuyP = np.arange(len(buyP), dtype=np.int)
    InfoSellP = np.arange(len(buyP), dtype=np.int)
    InfoBuyP = InfoBuyP[buyP]
    sellP = np.logical_not(buyP)
    InfoSellP = InfoSellP[sellP]
    if np.any(buyP):
        margin[buyP] = np.array(Info_df.iloc[:, InfoBuyP].loc['LongMargin'])
    if np.any(sellP):
        margin[sellP] = np.array(Info_df.iloc[:, InfoSellP].loc['ShortMargin'])
    openP = np.equal(order[GACV.SimOrder_OffsetFlag], GACV.OffsetFlag_Open)
    if openP.size == 0:
        buyP = np.zeros((orderLen,), dtype=np.bool)
    closeP = np.logical_not(openP)
    InfoOpenP = np.arange(len(openP))
    InfoCloseP = np.arange(len(openP))
    InfoOpenP = InfoOpenP[openP]
    InfoCloseP = InfoCloseP[closeP]
    if np.any(openP):
        marginFrozen[openP] = order[(GACV.SimOrder_OpenFrozenPrice, openP)] * order[(GACV.SimOrder_Contracts, openP)] * np.array(Info_df.iloc[:, InfoOpenP].loc['Multiple']) * margin[openP]
    if np.any(closeP):
        marginFrozen[closeP] = order[(GACV.SimOrder_OpenFrozenPrice, closeP)] * order[(GACV.SimOrder_Contracts, closeP)] * np.array(Info_df.iloc[:, InfoCloseP].loc['Multiple']) * margin[closeP]
    feeOpen1 = np.array([])
    for i in Info_df.columns:
        if np.any(Info_df[i].loc['TradingFeeOpen'] > 0.1):
            feeOpen1 = np.insert(feeOpen1, len(feeOpen1), values=[True], axis=0)
        else:
            feeOpen1 = np.insert(feeOpen1, len(feeOpen1), values=[False], axis=0)

    if feeOpen1.size == 0:
        feeOpen1 = np.zeros((orderLen,), dtype=np.bool)
    else:
        feeOpen1 = feeOpen1.astype(np.bool)
    feeOpen2 = np.logical_not(feeOpen1)
    FO1 = np.logical_and(openP, feeOpen1)
    FO2 = np.logical_and(openP, feeOpen2)
    InfoFO1P = np.arange(len(FO1))
    InfoFO2P = np.arange(len(FO2))
    InfoFO1P = InfoFO1P[FO1]
    InfoFO2P = InfoFO2P[FO2]
    if np.any(FO1):
        FO1_index = np.where(FO1 == True)[0]
        feeFrozen[FO1_index] = order[GACV.SimOrder_Contracts][FO1] * np.array(Info_df.iloc[:, InfoFO1P].loc['TradingFeeOpen'])
    if np.any(FO2):
        FO2_index = np.where(FO2 == True)[0]
        feeFrozen[FO2_index] = order[(GACV.SimOrder_Contracts, FO2)] * order[(GACV.SimOrder_OpenFrozenPrice, FO2)] * np.array(Info_df.iloc[:, InfoFO2P].loc['TradingFeeOpen']) * np.array(Info_df.iloc[:, InfoFO2P].loc['Multiple'])
    feeClose1 = np.array([])
    for i in Info_df.columns:
        if np.any(Info_df[i].loc['TradingFeeClose'] > 0.1):
            feeClose1 = np.insert(feeClose1, len(feeClose1), values=[True], axis=0)
        else:
            feeClose1 = np.insert(feeClose1, len(feeClose1), values=[False], axis=0)

    if feeClose1.size == 0:
        feeClose1 = np.zeros((orderLen,), dtype=np.bool)
    else:
        feeClose1 = feeClose1.astype(np.bool)
    feeClose2 = np.logical_not(feeClose1)
    FC1 = np.logical_and(closeP, feeClose1)
    FC2 = np.logical_and(closeP, feeClose2)
    InfoFC1P = np.arange(len(FC1))
    InfoFC2P = np.arange(len(FC2))
    InfoFC1P = InfoFC1P[FC1]
    InfoFC2P = InfoFC2P[FC2]
    if np.any(FC1):
        FC1_index = np.where(FC1 == True)[0]
        feeFrozen[FC1_index] = order[GACV.SimOrder_Contracts][FC1] * np.array(Info_df.iloc[:, InfoFC1P].loc['TradingFeeClose'])
    if np.any(FC2):
        FC2_index = np.where(FC2 == True)[0]
        feeFrozen[FC2_index] = order[GACV.SimOrder_Contracts][FC2] * order[GACV.SimOrder_OpenFrozenPrice][FC2] * np.array(Info_df.iloc[:, InfoFC2P].loc['TradingFeeClose']) * np.array(Info_df.iloc[:, InfoFC2P].loc['Multiple'])
    return (marginFrozen, feeFrozen)


def SetTargetPriceOfStopOrders(targetOrderID, targetTradePrice):
    if GVAR.g_ATraderSimUnfiredStopOrders.size < 1:
        return
    stopOrderIdx = np.where(GVAR.g_ATraderSimUnfiredStopOrders[GACV.SimStopOrder_TargetOrderID, :] == GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderID, targetOrderID)])[0]
    if stopOrderIdx.size < 1:
        return
    for j in range(len(stopOrderIdx)):
        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBarBegin, stopOrderIdx[j])] = False
        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetPrice, stopOrderIdx[j])] = targetTradePrice
        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderIdx[j])] = targetTradePrice
        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderIdx[j])] = targetTradePrice
        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, stopOrderIdx[j])] = GACV.StopOrderStatus_Holding
        _ordertype = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopOrderType, stopOrderIdx[j])])
        if _ordertype == GACV.StopOrderType_Loss:
            if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx[j])] == GACV.OrderAct_Buy:
                GapDirection = -1
            else:
                if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx[j])] == GACV.OrderAct_Sell:
                    GapDirection = 1
                else:
                    ToolBoxErrors.unexpect_switch_error('orderact')
            if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGapType, stopOrderIdx[j])] == GACV.StopGapType_Point:
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderIdx[j])] = targetTradePrice + GapDirection * GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGap, stopOrderIdx[j])]
            else:
                if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGapType, stopOrderIdx[j])] == GACV.StopGapType_Percent:
                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderIdx[j])] = targetTradePrice * (1 + GapDirection * GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGap, stopOrderIdx[j])] / 100)
                else:
                    ToolBoxErrors.unexpect_switch_error('stopgap')
        else:
            if _ordertype == GACV.StopOrderType_Profit:
                if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx[j])] == GACV.OrderAct_Buy:
                    GapDirection = 1
                else:
                    if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx[j])] == GACV.OrderAct_Sell:
                        GapDirection = -1
                    else:
                        ToolBoxErrors.unexpect_switch_error('orderact')
                if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGapType, stopOrderIdx[j])] == GACV.StopGapType_Point:
                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderIdx[j])] = targetTradePrice + GapDirection * GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGap, stopOrderIdx[j])]
                else:
                    if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGapType, stopOrderIdx[j])] == GACV.StopGapType_Percent:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderIdx[j])] = targetTradePrice * (1 + GapDirection * GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGap, stopOrderIdx[j])] / 100)
                    else:
                        ToolBoxErrors.unexpect_switch_error('stopgap')
            else:
                if _ordertype == GACV.StopOrderType_Trailing:
                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetPrice, stopOrderIdx[j])] = targetTradePrice
                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderIdx[j])] = targetTradePrice
                    if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx[j])] == GACV.OrderAct_Buy:
                        GapDirection = 1
                    else:
                        if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderIdx[j])] == GACV.OrderAct_Sell:
                            GapDirection = -1
                        else:
                            ToolBoxErrors.unexpect_switch_error('orderact')
                    if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingType, stopOrderIdx[j])] == GACV.StopGapType_Point:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_BeginTrailingPrice, stopOrderIdx[j])] = targetTradePrice + GapDirection * GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingGap, stopOrderIdx[j])]
                    else:
                        if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingType, stopOrderIdx[j])] == GACV.StopGapType_Percent:
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_BeginTrailingPrice, stopOrderIdx[j])] = targetTradePrice * (1 + GapDirection * GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingGap, stopOrderIdx[j])] / 100)
                        else:
                            ToolBoxErrors.unexpect_switch_error('stopgap')
                else:
                    ToolBoxErrors.unexpect_switch_error('stoporder')