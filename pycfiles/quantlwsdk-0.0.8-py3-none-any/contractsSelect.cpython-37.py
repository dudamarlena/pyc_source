# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\contractsSelect.py
# Compiled at: 2020-04-04 05:11:32
# Size of source mod 2**32: 17848 bytes
"""
.. moduleauthor:: lw
"""
from gm.api import *
import datetime
from pyalgotrade import commonHelpBylw
from pyalgotrade import gm3HelpBylw

class BaseStrategy4gmHot:
    __doc__ = 'lw李文实现的，用来封装策略中的换月动作的，基于掘金的下单函数的.\n\n    :param barFeed: The bar feed to use to backtest the strategy.\n    :type barFeed: :class:`pyalgotrade.barfeed.BaseBarFeed`.\n    :param cash_or_brk: The starting capital or a broker instance.\n    :type cash_or_brk: int/float or :class:`pyalgotrade.broker.Broker`.\n\n    .. note::\n        This is a base class and should not be used directly.\n    '

    def __init__(self, symbol, feed, context):
        self.symbol = symbol
        self.context = context
        self.feed = feed

    def hotChangeAction(self, aSymbol, cBarSDateTime):
        clearShortOrderRes = None
        openLongOrderRes = None
        clearLongOrderRes = None
        openShortOrderRes = None
        symbolHolding = self.context.account().positions(symbol=aSymbol)
        if symbolHolding:
            if self.feed.hotContractObj.isNeedMovePositionNDays(aSymbol, cBarSDateTime):
                nextHotSymbol = self.feed.hotContractObj.getHotContractNextTDays(aSymbol, cBarSDateTime)
                for aPos in symbolHolding:
                    vol_ = aPos['volume']
                    side_ = aPos['side']
                    if side_ == PositionSide_Long:
                        clearLongOrderRes = order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Sell, order_type=OrderType_Market,
                          position_effect=PositionEffect_Close,
                          price=0)
                        openLongOrderRes = order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Buy, order_type=OrderType_Market,
                          position_effect=PositionEffect_Open,
                          price=0)
                    if side_ == PositionSide_Short:
                        clearShortOrderRes = order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Buy, order_type=OrderType_Market,
                          position_effect=PositionEffect_Close,
                          price=0)
                        openShortOrderRes = order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Sell, order_type=OrderType_Market,
                          position_effect=PositionEffect_Open,
                          price=0)

        return (
         openLongOrderRes, openShortOrderRes, clearLongOrderRes, clearShortOrderRes)


def move_mainsymbol_position1(aSymbol, context, moveOrderLog=None):
    clearShortOrderRes = None
    openLongOrderRes = None
    clearLongOrderRes = None
    openShortOrderRes = None
    symbolHolding = context.account().positions(symbol=aSymbol)
    if symbolHolding:
        mainContract = commonHelpBylw.getMainContinContract(aSymbol)
        cdt = datetime.datetime.now()
        sDT = cdt - datetime.timedelta(days=1000)
        currDTstr = cdt.strftime('%Y-%m-%d %H:%M:%S')
        sDTstr = sDT.strftime('%Y-%m-%d %H:%M:%S')
        mainContractData = gm3HelpBylw.getMainContractData_Fade([mainContract], sDTstr, currDTstr)
        mainSymbolDf = mainContractData.stack().reset_index()
        mainSymbolDf.rename(index=str, columns={0: 'symbol'}, inplace=True)
        lastDf = mainSymbolDf.loc[(mainSymbolDf['symbol'] == aSymbol)].tail(1)
        lastDt = lastDf['datetime'].iloc[0]
        nextSymbolDf = mainSymbolDf.loc[(mainSymbolDf['datetime'] > lastDt)].head(1)
        next_symbol = nextSymbolDf['symbol'].iloc[0]
        for aPos in symbolHolding:
            vol_ = aPos['volume']
            side_ = aPos['side']
            if side_ == PositionSide_Long:
                if moveOrderLog is not None:
                    moveOrderLog.info('%s,%s,%s', aSymbol, vol_, '卖平')
                    moveOrderLog.info('%s,%s,%s', next_symbol, vol_, '买开')
                else:
                    context.clearOrders_whenOpen[aSymbol] = (
                     aSymbol, vol_, '卖平')
                    context.openOrders_whenOpen[next_symbol] = (next_symbol, vol_, '买开')
            if side_ == PositionSide_Short:
                if moveOrderLog is not None:
                    moveOrderLog.info('%s,%s,%s', aSymbol, vol_, '买平')
                    moveOrderLog.info('%s,%s,%s', next_symbol, vol_, '卖开')
                else:
                    context.clearOrders_whenOpen[aSymbol] = (
                     aSymbol, vol_, '买平')
                    context.openOrders_whenOpen[next_symbol] = (next_symbol, vol_, '卖开')


def move_mainsymbol_position(positions, latestTradeDate, context, moveOrderLog=None):
    if len(positions) <= 0:
        return
    underlyingAssets = []
    for aposition in positions:
        aSymbol = aposition.symbol
        mainContract = commonHelpBylw.getMainContinContract(aSymbol)
        underlyingAssets.append(mainContract)

    mainContractData = gm3HelpBylw.getMainContractData_Fade(underlyingAssets, latestTradeDate, latestTradeDate)
    for aposition in positions:
        aSymbol = aposition.symbol
        mainContract = commonHelpBylw.getMainContinContract(aSymbol)
        currSymbol = mainContractData[mainContract].iloc[0]
        if aSymbol != currSymbol:
            vol_ = aposition['volume']
            side_ = aposition['side']
            if side_ == PositionSide_Long:
                if moveOrderLog is not None:
                    moveOrderLog.info('%s,%s,%s', aSymbol, vol_, '卖平')
                    moveOrderLog.info('%s,%s,%s', currSymbol, vol_, '买开')
                else:
                    context.clearOrders_whenOpen[aSymbol] = (
                     aSymbol, vol_, '卖平')
                    context.openOrders_whenOpen[currSymbol] = (currSymbol, vol_, '买开')
        if side_ == PositionSide_Short:
            if moveOrderLog is not None:
                moveOrderLog.info('%s,%s,%s', aSymbol, vol_, '买平')
                moveOrderLog.info('%s,%s,%s', currSymbol, vol_, '卖开')
            else:
                context.clearOrders_whenOpen[aSymbol] = (
                 aSymbol, vol_, '买平')
                context.openOrders_whenOpen[currSymbol] = (currSymbol, vol_, '卖开')


def fisrt_two_Contracts_max_volume(dateTimeStr, aNewTradeCalendar, underlySym):
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)
    contractsdf = gm3HelpBylw.getContractsByUnderlyingSymbols(underlySym, nextTradeDate, nextTradeDate)
    symbolist = list(contractsdf['symbol'].values)
    sDt = lastDate + ' 00:00:00'
    edt = lastDate + ' 23:59:59'
    volDf = gm3HelpBylw.getHQData_Fade(symbolist, sDt, edt, fre='1d', fields_='symbol,eob,volume')
    volDf['underLyingSym'] = volDf['symbol'].apply(commonHelpBylw.getMainContinContract)
    volDf = volDf.groupby('underLyingSym').apply(lambda x: x.sort_values('volume', ascending=False))
    volDf = volDf.reset_index(drop=True)
    volDf = volDf.groupby('underLyingSym').head(2)
    contract1List = list(volDf['symbol'].values)
    leftContractsList = list(set(symbolist).difference(set(contract1List)))
    return (
     contract1List, leftContractsList)


def last_month_of_Contracts_delisted_date(dateTimeStr, aNewTradeCalendar, underlySym):
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)
    contractsdf = gm3HelpBylw.getContractsByUnderlyingSymbols(underlySym, nextTradeDate, nextTradeDate)
    from pandas.tseries.offsets import MonthBegin
    import pandas as pd
    contractsdf['lastMonthDate'] = pd.to_datetime(contractsdf['delisted_date']) + MonthBegin(-2)
    contractsdf['lastMonthDate'] = contractsdf['lastMonthDate'].dt.strftime('%Y-%m-%d')
    newContracDf = contractsdf.loc[(nextTradeDate < contractsdf['lastMonthDate'])]
    newContracDf['underLyingSym'] = newContracDf['symbol'].apply(commonHelpBylw.getMainContinContract)
    newContracDf = newContracDf.groupby('underLyingSym').apply(lambda x: x.sort_values('delisted_date'))
    newContracDf.index = newContracDf.index.droplevel(0)
    newContracDf = newContracDf.groupby('underLyingSym').head(2)
    contract1List = list(newContracDf['symbol'].values)
    keepContracDf = contractsdf.loc[(nextTradeDate >= contractsdf['lastMonthDate'])]
    leftContractsList = list(keepContracDf['symbol'].values)
    return (contract1List, leftContractsList)


def special_date_of_Contracts_delisted_date(dateTimeStr, aNewTradeCalendar, underLyingSymList):
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)
    import pandas as pd
    pDf = pd.read_excel('策略合约.xlsx', header=0)
    pDf['日期'] = pDf['日期'].dt.strftime('%Y-%m-%d')
    aContractRow = pDf.loc[(pDf['日期'] <= nextTradeDate)].iloc[(-1)]
    aContractRow = aContractRow.reset_index(drop=True)
    aContractRow = aContractRow.dropna()
    adjustContract = aContractRow.iloc[1:]
    for aunderLysym in underLyingSymList:
        if aunderLysym not in adjustContract.values:
            ex = Exception()
            raise ex

    boolflag = adjustContract.apply(gm3HelpBylw.isUnderlyingSymbl)
    adjustContract = adjustContract[(~boolflag)]
    adjustContract = adjustContract.apply(commonHelpBylw.adjustSymbol)
    contract1List = []
    for asymbol in list(adjustContract.values):
        underLysym = commonHelpBylw.getMainContinContract(asymbol)
        if underLysym in underLyingSymList:
            contract1List.append(asymbol)
        i = 1

    return contract1List


def special_date_of_Contracts_delisted_date_copy(dateTimeStr, aNewTradeCalendar, underlySym):
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)
    contractsdf = gm3HelpBylw.getContractsByUnderlyingSymbols(underlySym, nextTradeDate, nextTradeDate)
    from pandas.tseries.offsets import MonthBegin
    import pandas as pd
    dateIndex = pd.date_range('2019-01-01', '2020-12-31')
    datedf = dateIndex.to_frame(index=False, name='date')
    datedf['date'] = datedf['date'].dt.strftime('%Y-%m-%d')
    adjustDate = datedf.loc[datedf['date'].str[5:].isin(['04-15', '08-15', '12-15'])]
    comparedatedf = adjustDate.loc[(adjustDate['date'] <= nextTradeDate)]
    comparedate = comparedatedf['date'].iloc[(-1)]
    newContracDf = contractsdf.copy()
    newContracDf['underLyingSym'] = newContracDf['symbol'].apply(commonHelpBylw.getMainContinContract)
    newContracDf = newContracDf.groupby('underLyingSym').apply(lambda x: x.sort_values('delisted_date'))
    newContracDf.index = newContracDf.index.droplevel(0)
    newContracDf = newContracDf.loc[((newContracDf['listed_date'] <= comparedate) & (newContracDf['delisted_date'] >= comparedate))]
    newContracDf = newContracDf.groupby('underLyingSym').tail(2)
    contract1List = list(newContracDf['symbol'].values)
    keepContracDf = contractsdf.loc[(nextTradeDate >= contractsdf['lastMonthDate'])]
    leftContractsList = list(keepContracDf['symbol'].values)
    return (contract1List, leftContractsList)