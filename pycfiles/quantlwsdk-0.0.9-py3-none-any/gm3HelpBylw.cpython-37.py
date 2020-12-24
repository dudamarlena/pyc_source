# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\gm3HelpBylw.py
# Compiled at: 2020-04-20 00:21:20
# Size of source mod 2**32: 62180 bytes
"""
Created on Fri Jan 19 11:33:56 2018

@author: SH
"""
from gm.api import *
import pandas as pd, time
from pandas.tseries.offsets import DateOffset
from pandas.tseries.offsets import Second
import datetime
from pyalgotrade import calendayBylw
from pyalgotrade.utils import gmEnum
from pyalgotrade import commonHelpBylw
from pyalgotrade import observer
from datetime import timezone
from datetime import timedelta
from pyalgotrade import loggerHelpbylw
month159CZCE = [
 'CZCE.TA', 'CZCE.SR', 'CZCE.CF', 'CZCE.OI', 'CZCE.MA',
 'CZCE.FG', 'CZCE.RM', 'CZCE.ZC', 'CZCE.SF', 'CZCE.SM']
month1510CZCE = ['CZCE.AP']
month159DCE = [
 'DCE.A', 'DCE.B', 'DCE.C', 'DCE.CS', 'DCE.I', 'DCE.J',
 'DCE.JD', 'DCE.JM', 'DCE.L', 'DCE.M', 'DCE.P',
 'DCE.PP', 'DCE.V', 'DCE.Y', 'DCE.EG']
month1to12INE = [
 'INE.SC']
month1to12SHFE = [
 'SHFE.AL', 'SHFE.CU', 'SHFE.PB', 'SHFE.ZN']
month159SHFE = [
 'SHFE.SN', 'SHFE.NI', 'SHFE.RU', 'SHFE.FU', 'SHFE.SP']
month1510SHFE = [
 'SHFE.HC', 'SHFE.RB']
month612SHFE = [
 'SHFE.AU', 'SHFE.BU', 'SHFE.AG']
allCon = [
 'CFFEX.IC', 'CFFEX.IH', 'CFFEX.IF', 'CFFEX.T', 'CFFEX.TF']

def isUnderlyingSymbl(aSym):
    allUnderLyingSymbol = month159CZCE + month1510CZCE + month159DCE + month1to12INE + month1to12SHFE + month159SHFE + month1510SHFE + month612SHFE + allCon
    return aSym in allUnderLyingSymbol


def getNextContractID(currContractID):
    newContractID = ''
    if 'CZCE.ZC' in currContractID:
        if currContractID[-2:] == '01':
            newContractID = currContractID[:-2] + '05'
        if currContractID[-2:] == '05':
            newContractID = currContractID[:-2] + '09'
        if currContractID[-2:] == '09':
            temp = str(int(currContractID[(-3)]) + 1)
            newContractID = currContractID[:-3] + temp + '01'
    return newContractID


def corrMatrixToPairs(corrMatrixOriginal):
    au_corr = corrMatrixOriginal.unstack()
    pairs_to_drop = set()
    cols = corrMatrixOriginal.columns
    for i in range(0, corrMatrixOriginal.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))

    au_corr = au_corr.drop(labels=pairs_to_drop).sort_values(ascending=False)
    au_corr.rename('corrCoeff', inplace=True)
    return au_corr


def getHSAStockBylw():
    stock300 = get_instruments(symbols=None, exchanges=None, sec_types=[SEC_TYPE_STOCK], names=None, skip_suspended=False, skip_st=False, fields='symbol,sec_type,exchange,sec_id,sec_name,listed_date,delisted_date,is_suspended', df=True)
    aStock = stock300.loc[((stock300['sec_id'].str[0] != '2') & (stock300['sec_id'].str[0] != '9'))]
    return list(aStock['symbol'].values)


def getExchangeFromGmSymbol(gmSymbol):
    return gmSymbol.split('.')[0]


def getContractsByUnderlyingSymbols(symbolsCode, sDateTime, eDateTime):
    exchangelist = []
    for asym in symbolsCode:
        exchangelist.append(getExchangeFromGmSymbol(asym))

    exchangelist = list(set(exchangelist))
    month159 = month159CZCE + month159DCE + month159SHFE
    month1to12 = month1to12SHFE + month1to12INE
    month1510 = month1510SHFE + month1510CZCE
    month612 = month612SHFE
    currAllFutureContract = get_instruments(symbols=None, exchanges=exchangelist, sec_types=[SEC_TYPE_FUTURE], names=None, skip_suspended=True, skip_st=True, fields='symbol,exchange,sec_id,listed_date,delisted_date', df=True)
    currAllFutureContract['listed_date'] = currAllFutureContract['listed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    currAllFutureContract['listed_date'] = currAllFutureContract['listed_date'].str[0:10]
    currAllFutureContract['delisted_date'] = currAllFutureContract['delisted_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    currAllFutureContract['delisted_date'] = currAllFutureContract['delisted_date'].str[0:10]
    if sDateTime:
        if eDateTime:
            currAllFutureContract = currAllFutureContract[((currAllFutureContract['listed_date'] <= sDateTime) & (currAllFutureContract['delisted_date'] >= eDateTime))]
    tempContract = currAllFutureContract
    finalDf = pd.DataFrame(columns=(currAllFutureContract.columns))
    for inx, row in tempContract.iterrows():
        underLyingSymbol = commonHelpBylw.getMainContinContract(row['symbol'])
        if underLyingSymbol in symbolsCode:
            if underLyingSymbol in month159:
                if row['sec_id'][-2:] in ('01', '05', '09'):
                    finalDf.loc[finalDf.shape[0]] = row
            if underLyingSymbol in month1to12:
                if row['sec_id'][-2:] in ('01', '03', '05', '07', '09', '11'):
                    finalDf.loc[finalDf.shape[0]] = row
        if underLyingSymbol in month1510:
            if row['sec_id'][-2:] in ('01', '05', '10'):
                finalDf.loc[finalDf.shape[0]] = row
        if underLyingSymbol in month612:
            if row['sec_id'][-2:] in ('06', '12'):
                finalDf.loc[finalDf.shape[0]] = row
            if underLyingSymbol in allCon:
                finalDf.loc[finalDf.shape[0]] = row

    i = 1
    return finalDf


def ratioSpreadCal(aPair, astartTime, aendTime):
    aData = history(symbol=(aPair[0]), frequency='1d', start_time=astartTime, end_time=aendTime, fields='close,symbol,eob', df=True)
    if aData.empty:
        print(aPair[0] + ' is empty')
        return pd.DataFrame()
    aData.rename(columns={'close': aPair[0]}, inplace=True)
    bData = history(symbol=(aPair[1]), frequency='1d', start_time=astartTime, end_time=aendTime, fields='close,symbol,eob', df=True)
    if bData.empty:
        print(aPair[1] + ' is empty')
        return pd.DataFrame()
    bData.rename(columns={'close': aPair[1]}, inplace=True)
    concatData = pd.merge(aData, bData, on='eob')
    if aPair[0] == 'CZCE.SM':
        if aPair[1] == 'DCE.J':
            iiid = 1
    concatData[aPair[0] + '-' + aPair[1]] = concatData[aPair[0]] - concatData[aPair[1]]
    concatData[aPair[0] + '/' + aPair[1]] = concatData[aPair[0]] / concatData[aPair[1]]
    return concatData


def getHQDataFromGm(symbol, sDateTime, eDateTime, fields=None):
    aaa = history(symbol=symbol, frequency='60s', start_time=sDateTime, end_time=eDateTime, fields=fields, df=True)
    return aaa


def getTradeMsg(OrderRes):
    if OrderRes[0].ord_rej_reason == gmEnum.OrderRejectReason_NoEnoughCash:
        tradeMsg = 'NoEnoughCash'
        return tradeMsg


class gmOrder:
    clearOrderEvent = observer.Event()
    aOrderConrolOBj = None

    def __init__(self):
        self.i = 1

    @classmethod
    def openLong(cls, symbol_, vol_, signalName, dt, clearReverse=False, orderType=2, **kwargs):
        context = kwargs.get('context', None)
        price = kwargs.get('price', None)
        if context.is_live_model():
            if orderType == 2:
                exchangeID = symbol_.split('.')[0]
                if exchangeID == 'SHFE':
                    pricesDF = getInstumInfo(symbol_, fields='symbol,trade_date,upper_limit,lower_limit')
                    upperLimitPrice = pricesDF['upper_limit'].iloc[0]
                    return (cls.openLong)(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1, price=upperLimitPrice, **kwargs)
        if clearReverse:
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
            if symbolHolding:
                if symbolHolding['available'] > 0:
                    vol1_ = symbolHolding['available']
                    context.clearPositionSignalNames = ['allShort']
                    if 'price' in kwargs:
                        del kwargs['price']
                    clearShortOrderRes = (cls.clearShort)(symbol_, vol1_, 'cshort', dt, orderType=2, **kwargs)
        orderLog = kwargs.get('orderLog', None)
        if orderType == 1:
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'ol', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Buy, 
                 'order_type':OrderType_Limit, 
                 'position_effect':PositionEffect_Open, 
                 'price':price}):
                    return
            openLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy, order_type=OrderType_Limit,
              position_effect=PositionEffect_Open,
              price=price)
        if orderType == 2:
            price = 0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'ol', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Buy, 
                 'order_type':OrderType_Market, 
                 'position_effect':PositionEffect_Open, 
                 'price':0}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            openLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy, order_type=OrderType_Market,
              position_effect=PositionEffect_Open,
              price=0)
        tradeMsg = getTradeMsg(openLongOrderRes)
        if orderLog is not None:
            if tradeMsg is not None:
                sigMsg = signalName + '-' + tradeMsg
            else:
                sigMsg = signalName
            orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
        return openLongOrderRes

    @classmethod
    def openShort(cls, symbol_, vol_, signalName, dt, clearReverse=False, orderType=2, **kwargs):
        context = kwargs.get('context', None)
        price = kwargs.get('price', None)
        if context.is_live_model():
            if orderType == 2:
                exchangeID = symbol_.split('.')[0]
                if exchangeID == 'SHFE':
                    pricesDF = getInstumInfo(symbol_, fields='symbol,trade_date,upper_limit,lower_limit')
                    lowerLimitPrice = pricesDF['lower_limit'].iloc[0]
                    return (cls.openShort)(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1, price=lowerLimitPrice, **kwargs)
        if clearReverse:
            context = kwargs.get('context', None)
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
            if symbolHolding:
                if symbolHolding['available'] > 0:
                    vol1_ = symbolHolding['available']
                    context.clearPositionSignalNames = ['allLong']
                    if 'price' in kwargs:
                        del kwargs['price']
                    clearLongOrderRes = (cls.clearLong)(symbol_, vol1_, 'clong', dt, orderType=2, **kwargs)
        orderLog = kwargs.get('orderLog', None)
        if orderType == 2:
            price = 0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'os', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Sell, 
                 'order_type':OrderType_Market, 
                 'position_effect':PositionEffect_Open, 
                 'price':0}):
                    return
            openShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell, order_type=OrderType_Market,
              position_effect=PositionEffect_Open,
              price=0)
        if orderType == 1:
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'os', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Sell, 
                 'order_type':OrderType_Limit, 
                 'position_effect':PositionEffect_Open, 
                 'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            openShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell, order_type=OrderType_Limit,
              position_effect=PositionEffect_Open,
              price=price)
        tradeMsg = getTradeMsg(openShortOrderRes)
        if orderLog is not None:
            if tradeMsg is not None:
                sigMsg = signalName + '-' + tradeMsg
            else:
                sigMsg = signalName
            orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
        return openShortOrderRes

    @classmethod
    def clearLong(cls, symbol_, vol_, signalName, dt, clearSignals=['allLong'], orderType=2, **kwargs):
        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
        if context.is_live_model():
            if orderType == 2:
                exchangeID = symbol_.split('.')[0]
                if exchangeID == 'SHFE':
                    pricesDF = getInstumInfo(symbol_, fields='symbol,trade_date,upper_limit,lower_limit')
                    lower_limit = pricesDF['lower_limit'].iloc[0]
                    return (cls.clearLong)(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1, price=lower_limit, **kwargs)
        if orderType == 1:
            price = kwargs.get('price', None)
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'cl', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Sell, 
                 'order_type':OrderType_Limit, 
                 'position_effect':PositionEffect_Close, 
                 'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            clearLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell, order_type=OrderType_Limit,
              position_effect=PositionEffect_Close,
              price=price)
        if orderType == 2:
            price = 0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'cl', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Sell, 
                 'order_type':OrderType_Market, 
                 'position_effect':PositionEffect_Close, 
                 'price':0}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            clearLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell, order_type=OrderType_Market,
              position_effect=PositionEffect_Close,
              price=0)
        if orderLog is not None:
            orderLog.info('%s,%s,%s', dt, symbol_, signalName + '-' + symbol_ + '-' + str(price))
        return clearLongOrderRes

    @classmethod
    def clearShort(cls, symbol_, vol_, signalName, dt, clearSignals=['allShort'], orderType=2, **kwargs):
        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
        if context.is_live_model():
            if orderType == 2:
                exchangeID = symbol_.split('.')[0]
                if exchangeID == 'SHFE':
                    pricesDF = getInstumInfo(symbol_, fields='symbol,trade_date,upper_limit,lower_limit')
                    upper_limit = pricesDF['upper_limit'].iloc[0]
                    return (cls.clearShort)(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1, price=upper_limit, **kwargs)
        if orderType == 2:
            price = 0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'cs', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Buy, 
                 'order_type':OrderType_Market, 
                 'position_effect':PositionEffect_Close, 
                 'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            clearShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy, order_type=OrderType_Market,
              position_effect=PositionEffect_Close,
              price=0)
        if orderType == 1:
            price = kwargs.get('price', None)
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'cs', order_volume, funkargs={'symbol':symbol_, 
                 'volume':vol_, 
                 'side':OrderSide_Buy, 
                 'order_type':OrderType_Limit, 
                 'position_effect':PositionEffect_Close, 
                 'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            clearShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy, order_type=OrderType_Limit,
              position_effect=PositionEffect_Close,
              price=price)
        if orderLog is not None:
            orderLog.info('%s,%s,%s', dt, symbol_, signalName + '-' + symbol_ + '-' + str(price))
        return clearShortOrderRes

    @classmethod
    def clearLongAllPo(cls, symbol_, signalName, dt, orderType=2, **kwargs):
        context = kwargs.get('context', None)
        symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
        if symbolHolding:
            if symbolHolding['available'] > 0:
                vol1_ = symbolHolding['available']
                clearLongOrderRes = (cls.clearLong)(symbol_, vol1_, signalName, dt, orderType=orderType, **kwargs)
                return clearLongOrderRes

    @classmethod
    def clearShortAllPo(cls, symbol_, signalName, dt, orderType=2, **kwargs):
        context = kwargs.get('context', None)
        symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
        if symbolHolding:
            if symbolHolding['available'] > 0:
                vol1_ = symbolHolding['available']
                clearShortOrderRes = (cls.clearShort)(symbol_, vol1_, signalName, dt, orderType=orderType, **kwargs)
                return clearShortOrderRes

    @classmethod
    def openLongWithCash(cls, symbol_, cash_, signalName, dt, clearReverse=False, orderType=2, **kwargs):
        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
        price = kwargs.get('price', None)
        if context.is_live_model():
            if orderType == 2:
                exchangeID = symbol_.split('.')[0]
                if exchangeID == 'SHFE':
                    pricesDF = getInstumInfo(symbol_, fields='symbol,trade_date,upper_limit,lower_limit')
                    upper_limit = pricesDF['upper_limit'].iloc[0]
                    return (cls.openLongWithCash)(symbol_, cash_, signalName, dt, clearReverse=False, orderType=1, price=upper_limit, **kwargs)
        if clearReverse:
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
            if symbolHolding:
                if symbolHolding['available'] > 0:
                    vol1_ = symbolHolding['available']
                    context.clearPositionSignalNames = ['allShort']
                    if 'price' in kwargs:
                        del kwargs['price']
                    clearShortOrderRes = (cls.clearShort)(symbol_, vol1_, 'cshort', dt, orderType=2, **kwargs)
        if orderType == 2:
            price = 0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'ol', order_value, funkargs={'symbol':symbol_, 
                 'value':cash_, 
                 'side':OrderSide_Buy, 
                 'order_type':OrderType_Market, 
                 'position_effect':PositionEffect_Open, 
                 'price':0}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            openLongOrderRes = order_value(symbol=symbol_, value=cash_, price=0, side=OrderSide_Buy, order_type=OrderType_Market, position_effect=PositionEffect_Open)
        if orderType == 1:
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'ol', order_value, funkargs={'symbol':symbol_, 
                 'value':cash_, 
                 'side':OrderSide_Buy, 
                 'order_type':OrderType_Limit, 
                 'position_effect':PositionEffect_Open, 
                 'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            openLongOrderRes = order_value(symbol=symbol_, value=cash_, price=price, side=OrderSide_Buy, order_type=OrderType_Limit,
              position_effect=PositionEffect_Open)
        tradeMsg = getTradeMsg(openLongOrderRes)
        if orderLog is not None:
            if tradeMsg is not None:
                sigMsg = signalName + '-' + tradeMsg
            else:
                sigMsg = signalName
            orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
        return openLongOrderRes

    @classmethod
    def openShortWithCash(cls, symbol_, cash_, signalName, dt, clearReverse=False, orderType=2, **kwargs):
        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
        price = kwargs.get('price', None)
        if context.is_live_model():
            if orderType == 2:
                exchangeID = symbol_.split('.')[0]
                if exchangeID == 'SHFE':
                    pricesDF = getInstumInfo(symbol_, fields='symbol,trade_date,upper_limit,lower_limit')
                    lower_limit = pricesDF['lower_limit'].iloc[0]
                    return (cls.openLongWithCash)(symbol_, cash_, signalName, dt, clearReverse=False, orderType=1, price=lower_limit, **kwargs)
        if clearReverse:
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
            if symbolHolding:
                if symbolHolding['available'] > 0:
                    vol1_ = symbolHolding['available']
                    context.clearPositionSignalNames = ['allLong']
                    if 'price' in kwargs:
                        del kwargs['price']
                    clearLongOrderRes = (cls.clearLong)(symbol_, vol1_, 'clong', dt, orderType=2, **kwargs)
        if orderType == 2:
            price = 0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'os', order_value, funkargs={'symbol':symbol_, 
                 'value':cash_, 
                 'side':OrderSide_Sell, 
                 'order_type':OrderType_Market, 
                 'position_effect':PositionEffect_Open}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            openShortOrderRes = order_value(symbol=symbol_, value=cash_, price=0, side=OrderSide_Sell, order_type=OrderType_Market, position_effect=PositionEffect_Open)
        if orderType == 1:
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_, 'os', order_value, funkargs={'symbol':symbol_, 
                 'value':cash_, 
                 'side':OrderSide_Sell, 
                 'order_type':OrderType_Limit, 
                 'position_effect':PositionEffect_Open, 
                 'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
                    return
            openShortOrderRes = order_value(symbol=symbol_, value=cash_, price=price, side=OrderSide_Sell, order_type=OrderType_Limit,
              position_effect=PositionEffect_Open)
        tradeMsg = getTradeMsg(openShortOrderRes)
        if orderLog is not None:
            if tradeMsg is not None:
                sigMsg = signalName + '-' + tradeMsg
            else:
                sigMsg = signalName
            orderLog.info('%s,%s,%s', dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(price))
        return openShortOrderRes

    def fengexian(self):
        i = 1

    @classmethod
    def openLongWithNdang(cls, symbol_, vol_, signalName, dt, clearReverse=False, pattern='ACITVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        openLongOrderRes = (cls.openLong)(symbol_, vol_, signalName, dt, clearReverse=clearReverse, orderType=1, price=price, **kwargs)
        return openLongOrderRes

    @classmethod
    def openShortWithNdang(cls, symbol_, vol_, signalName, dt, clearReverse=False, pattern='ACITVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        openShortOrderRes = (cls.openShort)(symbol_, vol_, signalName, dt, clearReverse=clearReverse, orderType=1, price=price, **kwargs)
        return openShortOrderRes

    @classmethod
    def clearLongAllPoWithNdang(cls, symbol_, signalName, dt, pattern='ACITVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        clearLongOrderRes = (cls.clearLongAllPo)(symbol_, signalName, dt, orderType=1, price=price, **kwargs)
        return clearLongOrderRes

    @classmethod
    def clearShortAllPoWithNdang(cls, symbol_, signalName, dt, pattern='ACITVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        clearShortOrderRes = (cls.clearShortAllPo)(symbol_, signalName, dt, orderType=1, price=price, **kwargs)
        return clearShortOrderRes

    @classmethod
    def openLongWithCashWithNdang(cls, symbol_, cash_, signalName, dt, clearReverse=False, pattern='ACTIVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        openLongOrderRes = (cls.openLongWithCash)(symbol_, cash_, signalName, dt, clearReverse=clearReverse, orderType=1, 
         price=price, **kwargs)
        return openLongOrderRes

    @classmethod
    def openShortWithCashWithNdang(cls, symbol_, cash_, signalName, dt, clearReverse=False, pattern='ACTIVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        openShortOrderRes = (cls.openShortWithCash)(symbol_, cash_, signalName, dt, clearReverse=clearReverse, orderType=1, 
         price=price, **kwargs)
        return openShortOrderRes

    @classmethod
    def clearLongWithNdang(cls, symbol_, vol_, signalName, dt, clearSignals=['allLong'], pattern='ACTIVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        clearLongOrderRes = (cls.clearLong)(symbol_, vol_, signalName, dt, clearSignals=clearSignals, orderType=1, 
         price=price, **kwargs)
        return clearLongOrderRes

    @classmethod
    def clearShortWithNdang(cls, symbol_, vol_, signalName, dt, clearSignals=['allShort'], pattern='ACTIVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        clearShortOrderRes = (cls.clearShort)(symbol_, vol_, signalName, dt, clearSignals=clearSignals, orderType=1, 
         price=price, **kwargs)
        return clearShortOrderRes

    def writeOrderToFile(self, side_, position_effect_, filename='order.txt'):
        """ 装饰器 """

        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                symbol_ = args[0]
                vol_ = args[1]
                signalName_ = args[2]
                if side_ == OrderSide_Buy:
                    strSide = 'buy'
                if side_ == OrderSide_Sell:
                    strSide = 'sell'
                if position_effect_ == PositionEffect_Open:
                    strPosEffect = 'open'
                if position_effect_ == PositionEffect_Close:
                    strPosEffect = 'close'
                msg = '%s,%s,%s,%s,%s' % (symbol_, str(vol_), strSide, strPosEffect, signalName_)
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                pathAndName = current_date + '-' + filename
                f = open(pathAndName, 'a')
                f.write(msg)
                f.close()
                res = func(*args, **kwargs)
                return res

            return wrapper

        return decorator


def getMainContractData_Fade(continuousContract, sDatetime, eDatetime):
    dateList = commonHelpBylw.splitDates(sDatetime, eDatetime)
    dfMainContract = pd.DataFrame(columns=['mainContract', 'symbol', 'datetime'])
    index_ = 0
    for aContinu in continuousContract:
        for sDtime_, eDtime_ in dateList:
            tempMainContract = get_continuous_contracts(csymbol=aContinu, start_date=sDtime_,
              end_date=eDtime_)
            for atem in tempMainContract:
                dfMainContract.loc[(index_, 'mainContract')] = aContinu
                dfMainContract.loc[(index_, 'symbol')] = atem['symbol']
                dfMainContract.loc[(index_, 'datetime')] = atem['trade_date']
                index_ = index_ + 1

            i = 1

    dfMainContract['datetime'] = dfMainContract['datetime'].dt.strftime('%Y-%m-%d')
    mainContractData = dfMainContract.pivot(index='datetime', columns='mainContract', values='symbol')
    return mainContractData


def getMainSymbolLastFinishTradingDate(underlySyms, lastDate):
    mainContractData = getMainContractData_Fade(underlySyms, lastDate, lastDate)
    if not mainContractData.empty:
        currNeedMainSymbol = mainContractData.to_numpy()[0].tolist()
        return currNeedMainSymbol


def getMulData(contractList, mulSDate, muleDate):
    mulDict = {}
    for aContract in contractList:
        aMul = get_history_instruments(aContract, fields=None, start_date=mulSDate,
          end_date=muleDate)
        symbolCode = aContract
        if len(aMul) == 0:
            print(aContract, ' has no mul from juejin')
            mulDict[symbolCode] = 1
            continue
        aMul = aMul[0]
        mulValue = aMul['multiplier']
        mulDict[symbolCode] = mulValue

    return mulDict


def getSlippageRatio(underLyingSymList):
    asym = getMainSymbolLastFinishTradingDate(underLyingSymList, '2020-03-04')
    ratioList = []
    for acontract in asym:
        ticks = getCurrentTick('2020-03-04 09:30:30', acontract)
        danghq_1 = ticks[0]
        buyPrice = danghq_1['bid_p']
        sellPrice = danghq_1['ask_p']
        spreadPrice = sellPrice - buyPrice
        ratio_ = 10000.0 * spreadPrice / buyPrice
        ratioList.append((acontract, ratio_))

    return pd.DataFrame.from_records(ratioList, columns=['symbol', 'slipRatio'])


def getHQData_Fade(symbolist, sDateTime, eDateTim, fre='60s', fields_='symbol,eob,open,high,low,close', adjust=1, adjust_end_time=''):
    if fre == 'tick':
        dateName = 'created_at'
    else:
        dateName = 'eob'
    dfData = pd.DataFrame()
    for symbol_ in symbolist:
        sDtime_ = sDateTime
        eDtime_ = eDateTim
        tempHQdata = history(symbol=symbol_, frequency=fre, start_time=sDtime_, end_time=eDtime_, fields=fields_,
          df=True,
          adjust=adjust,
          adjust_end_time=adjust_end_time)
        while not tempHQdata.empty:
            tempHQdata = tempHQdata.sort_values(dateName)
            dfData = dfData.append(tempHQdata)
            latestDateTime = tempHQdata[dateName].iloc[(-1)]
            nextDT = latestDateTime + Second()
            sDtime_ = nextDT.strftime('%Y-%m-%d %H:%M:%S')
            if sDtime_ <= eDtime_:
                tempHQdata = history(symbol=symbol_, frequency=fre, start_time=sDtime_, end_time=eDtime_, fields=fields_,
                  df=True,
                  adjust=adjust)
            else:
                break

    return dfData


def getHQ_dangwei(dt, symbol_, direction, dangweiNum):
    sdt = dt
    import datetime
    datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S')
    edt = datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=1)
    sdt = edt - datetime.timedelta(minutes=30)
    sdt = sdt.strftime('%Y-%m-%d %H:%M:%S')
    edt = edt.strftime('%Y-%m-%d %H:%M:%S')
    tickHq = getHQData_Fade([symbol_], sdt, edt, fre='tick', fields_='symbol,created_at,open,high,low,quotes')
    dangHQ = tickHq['quotes'].iloc[(-1)]
    danghq_1 = dangHQ[dangweiNum]
    if direction == 'buy':
        if 'bid_p' not in danghq_1 or danghq_1['bid_v'] == 0:
            return -888
        return danghq_1['bid_p']
    if direction == 'sell':
        if 'ask_p' not in danghq_1 or danghq_1['ask_v'] == 0:
            return -888
        return danghq_1['ask_p']


def getCurrentTick(dt, symbol_):
    sdt = dt
    import datetime
    datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S')
    edt = datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=1)
    sdt = edt - datetime.timedelta(minutes=30)
    sdt = sdt.strftime('%Y-%m-%d %H:%M:%S')
    edt = edt.strftime('%Y-%m-%d %H:%M:%S')
    tickHq = getHQData_Fade([symbol_], sdt, edt, fre='tick', fields_='symbol,created_at,open,high,low,quotes')
    dangHQ = tickHq['quotes'].iloc[(-1)]
    return dangHQ


def getHQDataOfMainContract_Fade(underlyingSymbolList, sDateTime, eDateTim, fre='60s', fields_='symbol,eob,open,high,low,close'):
    hqDF = getHQData_Fade(underlyingSymbolList, sDateTime, eDateTim, fre=fre, fields_=fields_)
    aNewTradeCalendar = calendayBylw.getACalendarInstance()
    hqDF['eob'] = hqDF['eob'].dt.strftime('%Y-%m-%d %H:%M:%S')
    hqDF['tradeDate'] = hqDF['eob'].apply((aNewTradeCalendar.tradeDateTimeTradingDateOffset), aoffset=0)
    mainContractDf = getMainContractData_Fade(underlyingSymbolList, sDateTime, eDateTim)
    mainContractDfAdjust = mainContractDf.stack().reset_index(name='symbol')
    mergeDf = pd.merge(hqDF, mainContractDfAdjust, left_on=['tradeDate', 'symbol'], right_on=['datetime', 'mainContract'])
    resulDf = mergeDf.copy()
    resulDf.rename(index=str, columns={'symbol_y': 'symbol'}, inplace=True)
    strList = fields_.split(',')
    resulDf = resulDf[strList]
    resulDf['eob'] = pd.to_datetime((resulDf['eob']), format='%Y-%m-%d %H:%M:%S')
    resulDf['eob'] = resulDf['eob'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))
    return resulDf


def getInstumInfo(symbols, fields='symbol,exchange,sec_id,listed_date,delisted_date'):
    instuInfo = get_instruments(symbols=symbols, fields=fields, df=True)
    return instuInfo


def dealwithGmTradeRecord(f):
    realTradeData = pd.read_csv(f, header=0, index_col=False)
    realTradeData.columns = realTradeData.columns.str.strip()
    tradeRecordDf = realTradeData[[
     'side', 'symbol', 'positionEffect', 'filledVolume', 'filledVwap', 'createdAt', 'filledCommission']]
    tradeRecordDf.columns = ['direction', 'symbol', 'PositionEffect', 'volume', 'tradePrice', 'tradeDateTime',
     'commission']
    tradeRecordDf = tradeRecordDf.dropna()
    tradeRecordDf['tradeDateTime'] = pd.to_datetime((tradeRecordDf['tradeDateTime']), format='%Y-%m-%dT%H:%M:%SZ')
    tradeRecordDf['tradeDateTime'] = tradeRecordDf['tradeDateTime'].dt.tz_localize(tz=(timezone.utc))
    tradeRecordDf['tradeDateTime'] = tradeRecordDf['tradeDateTime'].dt.tz_convert(tz=(timezone(timedelta(hours=8))))
    tradeRecordDf['tradeDateTime'] = tradeRecordDf['tradeDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    tradeRecordDf = tradeRecordDf.sort_values('tradeDateTime', kind='mergesort')
    tradeRecordDf = tradeRecordDf.replace({'direction':{1:'买', 
      2:'卖'}, 
     'PositionEffect':{1:'开仓',  2:'平仓',  3:'平今仓',  4:'平昨仓'}})
    return tradeRecordDf


def writeTradeRecordToMongo(gmTrade):
    i = 1