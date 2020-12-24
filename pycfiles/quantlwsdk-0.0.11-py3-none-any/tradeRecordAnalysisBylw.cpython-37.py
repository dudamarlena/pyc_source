# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\tradeRecordAnalysisBylw.py
# Compiled at: 2020-04-04 05:11:32
# Size of source mod 2**32: 54056 bytes
"""
Created on Fri Oct 12 21:34:13 2018

@author: SH
"""
from __future__ import print_function, absolute_import, unicode_literals
import numpy as np, pandas as pd
from pyalgotrade import gm3HelpBylw
from pyalgotrade import commonHelpBylw
try:
    import talib
except:
    print('请安装TA-Lib库')

from gm.api import *
import datetime

class tradeRecordObj:

    def __addMul(self):
        self.jiaogeDf['mul'] = 1
        if self.mulDf.empty:
            return
        for i in range(self.jiaogeDf.shape[0]):
            sym = self.jiaogeDf['symbol'].iloc[i]
            date = self.jiaogeDf['tradeDate'].iloc[i]
            self.jiaogeDf['mul'].iloc[i] = self.mulDf.loc[(date, sym)]

    def __init__(self, aDf, aCusCalendar, aMul=pd.DataFrame(), aMulDict={}):
        aDf = aDf.sort_values(by=['tradeDateTime'], kind='mergesort')
        self.jiaogeDf = aDf
        self.mulDict = aMulDict
        self.clearName = [
         '平仓', '平今仓', '平昨仓', '平今', '平昨']
        self.aCusCalendar = aCusCalendar
        self._tradeRecordObj__clearedTradeRecordDf = self._tradeRecordObj__productTradeMatchDf()
        self.clearedDFwithProfit = self.getAOpenClearPairProfit()
        print('*****')
        i = 1

    def __productTradeMatchDf(self):
        tradeMatchDf = self.jiaogeDf.groupby('symbol').apply(self._tradeRecordObj__tradeMatch)
        tradeMatchDf = tradeMatchDf.sort_values(by=['cleartradeDateTime'])
        tradeMatchDf.index = tradeMatchDf.index.droplevel(1)
        tradeMatchDf = tradeMatchDf.reset_index()
        return tradeMatchDf

    def __tradeMatch(self, aGroup):
        openLongDf = aGroup.loc[((aGroup['direction'] == '买') & (aGroup['PositionEffect'] == '开仓'))]
        clearLongDf = aGroup.loc[((aGroup['direction'] == '卖') & aGroup['PositionEffect'].isin(self.clearName))]
        openShortDf = aGroup.loc[((aGroup['direction'] == '卖') & (aGroup['PositionEffect'] == '开仓'))]
        clearShortDf = aGroup.loc[((aGroup['direction'] == '买') & aGroup['PositionEffect'].isin(self.clearName))]
        resDF = pd.DataFrame()
        resIn = 0

        def merge2DF(openLongDf, clearLongDf):
            if not openLongDf.empty:
                if not clearLongDf.empty:
                    i = 1
            else:
                resDF = pd.DataFrame()
                resIn = 0
                openin = 0
                clearin = 0
                while openin < openLongDf.shape[0] and clearin < clearLongDf.shape[0]:
                    longOpenDT = openLongDf['tradeDateTime'].iloc[openin]
                    longClearDT = clearLongDf['tradeDateTime'].iloc[clearin]
                    if longOpenDT <= longClearDT:
                        resDF.loc[(resIn, 'opentradeDateTime')] = openLongDf['tradeDateTime'].iloc[openin]
                        resDF.loc[(resIn, 'cleartradeDateTime')] = clearLongDf['tradeDateTime'].iloc[clearin]
                        resDF.loc[(resIn, 'openTradePrice')] = openLongDf['tradePrice'].iloc[openin]
                        resDF.loc[(resIn, 'clearTradePrice')] = clearLongDf['tradePrice'].iloc[clearin]
                        if clearLongDf['volume'].iloc[clearin] < openLongDf['volume'].iloc[openin]:
                            resDF.loc[(resIn, 'clearCom')] = clearLongDf['commission'].iloc[clearin]
                            resDF.loc[(resIn, 'openCom')] = openLongDf['commission'].iloc[openin] / openLongDf['volume'].iloc[openin] * clearLongDf['volume'].iloc[clearin]
                            openLongDf['commission'].iloc[openin] = openLongDf['commission'].iloc[openin] - resDF.loc[(
                             resIn, 'openCom')]
                            resDF.loc[(resIn, 'vol')] = clearLongDf['volume'].iloc[clearin]
                            openLongDf['volume'].iloc[openin] = openLongDf['volume'].iloc[openin] - clearLongDf['volume'].iloc[clearin]
                            clearin = clearin + 1
                            resIn = resIn + 1
                            continue
                    else:
                        if clearLongDf['volume'].iloc[clearin] == openLongDf['volume'].iloc[openin]:
                            resDF.loc[(resIn, 'vol')] = openLongDf['volume'].iloc[openin]
                            resDF.loc[(resIn, 'clearCom')] = clearLongDf['commission'].iloc[clearin]
                            resDF.loc[(resIn, 'openCom')] = openLongDf['commission'].iloc[openin]
                            openin = openin + 1
                            clearin = clearin + 1
                            resIn = resIn + 1
                            continue
                        if clearLongDf['volume'].iloc[clearin] > openLongDf['volume'].iloc[openin]:
                            resDF.loc[(resIn, 'openCom')] = openLongDf['commission'].iloc[openin]
                            resDF.loc[(resIn, 'clearCom')] = clearLongDf['commission'].iloc[clearin] / clearLongDf['volume'].iloc[clearin] * openLongDf['volume'].iloc[openin]
                            clearLongDf['commission'].iloc[clearin] = clearLongDf['commission'].iloc[clearin] - resDF.loc[(
                             resIn, 'clearCom')]
                            resDF.loc[(resIn, 'vol')] = openLongDf['volume'].iloc[openin]
                            clearLongDf['volume'].iloc[clearin] = -openLongDf['volume'].iloc[openin] + clearLongDf['volume'].iloc[clearin]
                            openin = openin + 1
                            resIn = resIn + 1
                            continue
                        else:
                            resDF.loc[(resIn, 'opentradeDateTime')] = np.nan
                            resDF.loc[(resIn, 'cleartradeDateTime')] = clearLongDf['tradeDateTime'].iloc[clearin]
                            resDF.loc[(resIn, 'openTradePrice')] = np.nan
                            resDF.loc[(resIn, 'clearTradePrice')] = clearLongDf['tradePrice'].iloc[clearin]
                            resDF.loc[(resIn, 'openCom')] = np.nan
                            resDF.loc[(resIn, 'clearCom')] = clearLongDf['commission'].iloc[clearin]
                            resDF.loc[(resIn, 'vol')] = clearLongDf['volume'].iloc[clearin]
                            clearin = clearin + 1
                            resIn = resIn + 1
                        continue

                if openin == openLongDf.shape[0]:
                    if clearin < clearLongDf.shape[0]:
                        while clearin < clearLongDf.shape[0]:
                            resDF.loc[(resIn, 'opentradeDateTime')] = np.nan
                            resDF.loc[(resIn, 'cleartradeDateTime')] = clearLongDf['tradeDateTime'].iloc[clearin]
                            resDF.loc[(resIn, 'openTradePrice')] = np.nan
                            resDF.loc[(resIn, 'clearTradePrice')] = clearLongDf['tradePrice'].iloc[clearin]
                            resDF.loc[(resIn, 'openCom')] = np.nan
                            resDF.loc[(resIn, 'clearCom')] = clearLongDf['commission'].iloc[clearin]
                            resDF.loc[(resIn, 'vol')] = clearLongDf['volume'].iloc[clearin]
                            clearin = clearin + 1
                            resIn = resIn + 1
                            continue

                if openin < openLongDf.shape[0] and clearin == clearLongDf.shape[0]:
                    while openin < openLongDf.shape[0]:
                        resDF.loc[(resIn, 'cleartradeDateTime')] = np.nan
                        resDF.loc[(resIn, 'opentradeDateTime')] = openLongDf['tradeDateTime'].iloc[openin]
                        resDF.loc[(resIn, 'clearTradePrice')] = np.nan
                        resDF.loc[(resIn, 'openTradePrice')] = openLongDf['tradePrice'].iloc[openin]
                        resDF.loc[(resIn, 'clearCom')] = np.nan
                        resDF.loc[(resIn, 'openCom')] = openLongDf['commission'].iloc[openin]
                        resDF.loc[(resIn, 'vol')] = openLongDf['volume'].iloc[openin]
                        openin = openin + 1
                        resIn = resIn + 1
                        continue

            return resDF

        longRes = merge2DF(openLongDf, clearLongDf)
        longRes['positionSide'] = 'long'
        shortRes = merge2DF(openShortDf, clearShortDf)
        shortRes['positionSide'] = 'short'
        resDF = longRes.append(shortRes)
        return resDF

    def __openClearMatchNoDTime(self, aGroup):
        openLongDf = aGroup.loc[((aGroup['direction'] == '买') & (aGroup['PositionEffect'] == '开仓'))]
        clearLongDf = aGroup.loc[((aGroup['direction'] == '卖') & aGroup['PositionEffect'].isin(self.clearName))]
        openShortDf = aGroup.loc[((aGroup['direction'] == '卖') & (aGroup['PositionEffect'] == '开仓'))]
        clearShortDf = aGroup.loc[((aGroup['direction'] == '买') & aGroup['PositionEffect'].isin(self.clearName))]
        resDF = pd.DataFrame()
        resIn = 0

        def merge2DF(openLongDf, clearLongDf):
            if not openLongDf.empty:
                if not clearLongDf.empty:
                    openLongDf = openLongDf.sort_values(by=['tradeDate', 'tradeTime'])
                    clearLongDf = clearLongDf.sort_values(by=['tradeDate', 'tradeTime'])
            resDF = pd.DataFrame()
            resIn = 0
            openin = 0
            clearin = 0
            while openin < openLongDf.shape[0] and clearin < clearLongDf.shape[0]:
                resDF.loc[(resIn, 'opentradeDate')] = openLongDf['tradeDate'].iloc[openin]
                resDF.loc[(resIn, 'opentradeTime')] = openLongDf['tradeTime'].iloc[openin]
                resDF.loc[(resIn, 'cleartradeDate')] = clearLongDf['tradeDate'].iloc[clearin]
                resDF.loc[(resIn, 'cleartradeTime')] = clearLongDf['tradeTime'].iloc[clearin]
                resDF.loc[(resIn, 'openTradePrice')] = openLongDf['tradePrice'].iloc[openin]
                resDF.loc[(resIn, 'clearTradePrice')] = clearLongDf['tradePrice'].iloc[clearin]
                resDF.loc[(resIn, 'openMul')] = openLongDf['mul'].iloc[openin]
                resDF.loc[(resIn, 'clearMul')] = clearLongDf['mul'].iloc[clearin]
                resDF.loc[(resIn, 'openCom')] = openLongDf['commission'].iloc[openin]
                resDF.loc[(resIn, 'clearCom')] = clearLongDf['commission'].iloc[clearin]
                if clearLongDf['volume'].iloc[clearin] < openLongDf['volume'].iloc[openin]:
                    resDF.loc[(resIn, 'vol')] = clearLongDf['volume'].iloc[clearin]
                    openLongDf['volume'].iloc[openin] = openLongDf['volume'].iloc[openin] - clearLongDf['volume'].iloc[clearin]
                    clearin = clearin + 1
                    resIn = resIn + 1
                    continue
                if clearLongDf['volume'].iloc[clearin] == openLongDf['volume'].iloc[openin]:
                    resDF.loc[(resIn, 'vol')] = openLongDf['volume'].iloc[openin]
                    openin = openin + 1
                    clearin = clearin + 1
                    resIn = resIn + 1
                    continue
                if clearLongDf['volume'].iloc[clearin] > openLongDf['volume'].iloc[openin]:
                    resDF.loc[(resIn, 'vol')] = openLongDf['volume'].iloc[openin]
                    clearLongDf['volume'].iloc[clearin] = -openLongDf['volume'].iloc[openin] + clearLongDf['volume'].iloc[clearin]
                    openin = openin + 1
                    resIn = resIn + 1
                    continue

            return resDF

        longRes = merge2DF(openLongDf, clearLongDf)
        longRes['positionSide'] = 'long'
        shortRes = merge2DF(openShortDf, clearShortDf)
        shortRes['positionSide'] = 'short'
        resDF = longRes.append(shortRes)
        return resDF

    def getTradeStatistics(self):
        """
        仿照 文华财经的输出报告。输出交易统计。具体格式见笔记

    直接忽略了没有平仓的东东。即只算了 开平仓对的收益。如果有未平仓的情况，忽略了。具体间笔记“统计交易次数”
    
        """

        def tradeCount(aGroup):
            if aGroup['symbol'].iloc[0] == 'CFFEX.IF1812':
                ii = 1
            dropDul = aGroup.drop_duplicates(subset=['opentradeDateTime', 'cleartradeDateTime'], keep='first',
              inplace=False)
            count = dropDul.shape[0]
            return count

        def tradeCountNoTime(aGroup):
            dropDul = aGroup.drop_duplicates(subset=['opentradeDate', 'cleartradeDate'], keep='first',
              inplace=False)
            count = dropDul.shape[0]
            return count

        def tradeCountOrginal(aGroup):
            count = aGroup.shape[0]
            return count

        countDf = self._tradeRecordObj__clearedTradeRecordDf.groupby(by=['symbol', 'positionSide']).apply(tradeCount)
        profitOfevryContDf = self.clearedDFwithProfit.groupby(by=['symbol', 'positionSide'])[[
         'profit', 'vol']].sum()
        profitOfevryContDf['tradeCount'] = countDf
        profitOfevryContDf = profitOfevryContDf.reset_index()
        return profitOfevryContDf

    def getAOpenClearPairProfit(self):

        def addAProfit(aSeries):
            if aSeries['positionSide'] == 'long':
                return (-aSeries['openTradePrice'] + aSeries['clearTradePrice']) * aSeries['vol'] * self.mulDict[aSeries['symbol']] - aSeries['openCom'] - aSeries['clearCom']
            return (aSeries['openTradePrice'] - aSeries['clearTradePrice']) * aSeries['vol'] * self.mulDict[aSeries['symbol']] - aSeries['openCom'] - aSeries['clearCom']

        clearedDFwithProfit = self._tradeRecordObj__clearedTradeRecordDf.copy()
        clearedDFwithProfit['profit'] = clearedDFwithProfit.apply(addAProfit, axis=1)
        return clearedDFwithProfit

    def intradayProfit(self):
        dataDf = self.jiaogeDf
        reDf = dataDf.groupby(by=['tradeDate', 'symbol']).apply(self._tradeRecordObj__openClearMatchNoDTime)
        reDf.index = reDf.index.droplevel(2)

        def afun(adf):
            if adf['positionSide'] == 'long':
                profit = -adf['openTradePrice'] * adf['vol'] * adf['openMul'] + adf['clearTradePrice'] * adf['vol'] * adf['clearMul'] - adf['openCom'] - adf['clearCom']
            if adf['positionSide'] == 'short':
                profit = adf['openTradePrice'] * adf['vol'] * adf['openMul'] - adf['clearTradePrice'] * adf['vol'] * adf['clearMul'] - adf['openCom'] - adf['clearCom']
            return profit

        reDf['profit'] = reDf.apply(afun, axis=1)
        return reDf

    def intradayAmount(self):
        dataDf = self.jiaogeDf
        reDf = dataDf.groupby(by=['tradeDate', 'symbol']).apply(self._tradeRecordObj__openClearMatchNoDTime)
        reDf['amount'] = reDf['clearMul'] * reDf['clearTradePrice'] * reDf['vol'] + reDf['openMul'] * reDf['openTradePrice'] * reDf['vol']
        reDf.index = reDf.index.droplevel(2)
        i = 1
        return reDf['amount'].sum()

    def tradeProfitVSClose(self, closeData):
        dataDf = self.jiaogeDf

        def afun(aSeries):
            symbol = aSeries['symbol']
            close = closeData.loc[(aSeries['tradeDate'], symbol)]
            if aSeries['direction'] == '买':
                profit = (close - aSeries['tradePrice']) * 1 * self.mulDict[symbol] * aSeries['volume'] - aSeries['commission']
            if aSeries['direction'] == '卖':
                profit = (close - aSeries['tradePrice']) * -1 * self.mulDict[symbol] * aSeries['volume'] - aSeries['commission']
            return profit

        dataDf['tradeProfit'] = dataDf.apply(afun, axis=1)
        tradeProDF = dataDf.groupby(by=['tradeDate', 'symbol'])['tradeProfit'].agg(sum)
        tradeProDF = tradeProDF.reset_index()
        return tradeProDF

    def tradeProfitNoIntra(self, tradeDF, intraDf):
        adjustIntraDF = intraDf.reset_index()
        adjustIntraDF = adjustIntraDF[['tradeDate', 'symbol', 'positionSide', 'profit']]
        adjustIntraDF = adjustIntraDF.groupby(by=['tradeDate', 'symbol', 'positionSide'])['profit'].agg(sum)
        adjustIntraDF = adjustIntraDF.reset_index()
        adjustIntraDF['profit'].sum()
        mergeResu = pd.merge(adjustIntraDF, tradeDF, left_on=['tradeDate', 'symbol', 'positionSide'], right_on=[
         'tradeDate', 'symbol', 'positionSi'],
          how='outer')
        mergeResu = mergeResu.fillna(0)
        mergeResu['dailyPro'] = mergeResu['tradeProfit'] - mergeResu['profit']
        return mergeResu

    def getTradeMatchDf(self):
        return self._tradeRecordObj__clearedTradeRecordDf

    def positionEveryDaySave(self, dateSerial):
        positionDF = pd.DataFrame()
        tradeMatchDf = self.jiaogeDf.groupby('symbol').apply(self._tradeRecordObj__tradeMatch)
        tradeMatchDf = tradeMatchDf.sort_values(by=['opentradeDate'])
        tradeMatchDf.index = tradeMatchDf.index.droplevel(1)
        tradeMatchDf = tradeMatchDf.reset_index()
        tradeMatchDf = tradeMatchDf[(tradeMatchDf['opentradeDate'] != tradeMatchDf['cleartradeDate'])]
        for aDate in dateSerial.__iter__():
            aSelectDf = tradeMatchDf.loc[((tradeMatchDf['opentradeDate'] <= aDate) & (tradeMatchDf['cleartradeDate'] > aDate))]
            aSelectDf = aSelectDf[['symbol', 'positionSide', 'opentradeDate', 'cleartradeDate', 'openTradePrice', 'vol']]
            aSelectDf['tradeDate'] = aDate
            positionDF = positionDF.append(aSelectDf)

        positionDF = positionDF.drop(['cleartradeDate'], axis=1)
        positionDF = positionDF.groupby(by=['symbol', 'positionSide', 'tradeDate', 'openTradePrice'])['vol'].agg(sum)
        positionDF = positionDF.reset_index()
        return positionDF

    def purePositionEveryDay(self, finalPostionDF):
        aSDate = self.jiaogeDf['tradeDate'].iloc[0]
        aEDate = self.jiaogeDf['tradeDate'].iloc[(-1)]
        aPreDate = self.aCusCalendar.tradingDaysOffset(aSDate, -1)
        if finalPostionDF.empty:
            dateSeriesEndDate = aEDate
        else:
            dateSeriesEndDate = self.aCusCalendar.tradingDaysOffset(finalPostionDF['tradeDate'].iloc[0], -1)
        dateSerial = self.aCusCalendar.getADateTimeSeries(aPreDate, dateSeriesEndDate)
        dateSerial = dateSerial.sort_values(ascending=False)
        positionEveryDayDf = finalPostionDF.copy()
        dateSerialLen = len(dateSerial)
        positionColumnsName = list(finalPostionDF.columns.values)
        for poNum in range(dateSerialLen):
            aDate = dateSerial.iloc[poNum]
            aTime = '00:00:00'
            if aDate in positionEveryDayDf['tradeDate'].values:
                continue
            else:
                if poNum >= 1:
                    nextDate = dateSerial.iloc[(poNum - 1)]
                else:
                    nextDate = self.aCusCalendar.tradingDaysOffset(aDate, 1)
                nextDayPostionDf = positionEveryDayDf.loc[(positionEveryDayDf['tradeDate'] == nextDate)]
                nextDayTradeDf = self.jiaogeDf.loc[(self.jiaogeDf['tradeDate'] == nextDate)]
                nextDayPostionDf['tradeDate'] = aDate
                if nextDayTradeDf.empty:
                    positionEveryDayDf = positionEveryDayDf.append(nextDayPostionDf)
                else:
                    reversnextDayTradeDf = nextDayTradeDf[::-1]
                    for row_number, row in reversnextDayTradeDf.iterrows():
                        sym = row['symbol']
                        dire = row['direction']
                        positionEffect = row['PositionEffect']
                        vol = row['volume']
                        tradePirce = row['tradePrice']
                        if dire == '买' and positionEffect == '开仓' or dire == '卖':
                            if positionEffect in self.clearName:
                                longBoolindex = (nextDayPostionDf['symbol'] == sym) & (nextDayPostionDf['positionSide'] == 'long')
                        if dire == '买':
                            if positionEffect == '开仓':
                                aSeriesPos = nextDayPostionDf.loc[longBoolindex]
                                if aSeriesPos.empty:
                                    aTuple = (
                                     sym, 'long', -vol, tradePirce, aDate)
                                    aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                    nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                                else:
                                    nextDayPostionDf.loc[(longBoolindex, 'vol')] = nextDayPostionDf.loc[(longBoolindex, 'vol')] - vol
                        if dire == '卖':
                            if positionEffect in self.clearName:
                                aLongPosition = nextDayPostionDf.loc[longBoolindex]
                                if aLongPosition.empty:
                                    aTuple = (
                                     sym, 'long', vol, tradePirce, aDate)
                                    aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                    nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                                else:
                                    nextDayPostionDf.loc[(longBoolindex, 'vol')] = nextDayPostionDf.loc[(longBoolindex, 'vol')] + vol
                        if dire == '卖' and positionEffect == '开仓' or dire == '买':
                            if positionEffect in self.clearName:
                                shortBoolindex = (nextDayPostionDf['symbol'] == sym) & (nextDayPostionDf['positionSide'] == 'short')
                        if dire == '卖':
                            if positionEffect == '开仓':
                                aSeriesPos = nextDayPostionDf.loc[shortBoolindex]
                                if aSeriesPos.empty:
                                    aTuple = (
                                     sym, 'short', -vol, tradePirce, aDate)
                                    aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                    nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                                else:
                                    nextDayPostionDf.loc[(shortBoolindex, 'vol')] = nextDayPostionDf.loc[(shortBoolindex, 'vol')] - vol
                        if dire == '买' and positionEffect in self.clearName:
                            aSeriesPos = nextDayPostionDf.loc[shortBoolindex]
                            if aSeriesPos.empty:
                                aTuple = (
                                 sym, 'short', vol, tradePirce, aDate)
                                aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                            else:
                                nextDayPostionDf.loc[(shortBoolindex, 'vol')] = nextDayPostionDf.loc[(shortBoolindex, 'vol')] + vol

                    nextDayPostionDf = nextDayPostionDf.loc[(nextDayPostionDf['vol'] != 0)]
                    positionEveryDayDf = positionEveryDayDf.append(nextDayPostionDf)

        return positionEveryDayDf

    def purePositionEveryDay_vecotr(self, finalPostionDF):
        aSDate = self.jiaogeDf['tradeDate'].iloc[0]
        aEDate = self.jiaogeDf['tradeDate'].iloc[(-1)]
        aPreDate = self.aCusCalendar.tradingDaysOffset(aSDate, -1)
        if finalPostionDF.empty:
            dateSeriesEndDate = aEDate
        else:
            dateSeriesEndDate = aCusCalendar.tradingDaysOffset(finalPostionDF['tradeDate'].iloc[0], -1)
        dateSerial = self.aCusCalendar.getADateTimeSeries(aPreDate, dateSeriesEndDate)
        dateDf = dateSerial.to_frame()
        positionEveryDayDf = finalPostionDF.copy()
        dateSerialLen = len(dateSerial)
        positionColumnsName = list(finalPostionDF.columns.values)
        for poNum in range(dateSerialLen):
            aDate = dateSerial.iloc[poNum]
            aTime = '00:00:00'
            if aDate in positionEveryDayDf['tradeDate'].values:
                continue
            else:
                if poNum >= 1:
                    nextDate = dateSerial.iloc[(poNum - 1)]
                else:
                    nextDate = self.aCusCalendar.tradingDaysOffset(aDate, 1)
                nextDayPostionDf = positionEveryDayDf.loc[(positionEveryDayDf['tradeDate'] == nextDate)]
                nextDayTradeDf = self.jiaogeDf.loc[(self.jiaogeDf['tradeDate'] == nextDate)]
                nextDayPostionDf['tradeDate'] = aDate
                if nextDayTradeDf.empty:
                    positionEveryDayDf = positionEveryDayDf.append(nextDayPostionDf)
                else:
                    reversnextDayTradeDf = nextDayTradeDf[::-1]
                    for row_number, row in reversnextDayTradeDf.iterrows():
                        sym = row['symbol']
                        dire = row['direction']
                        positionEffect = row['PositionEffect']
                        vol = row['volume']
                        tradePirce = row['tradePrice']
                        if dire == '买' and positionEffect == '开仓' or dire == '卖':
                            if positionEffect in self.clearName:
                                longBoolindex = (nextDayPostionDf['symbol'] == sym) & (nextDayPostionDf['positionSide'] == 'long')
                        if dire == '买':
                            if positionEffect == '开仓':
                                aSeriesPos = nextDayPostionDf.loc[longBoolindex]
                                if aSeriesPos.empty:
                                    aTuple = (
                                     sym, 'long', -vol, tradePirce, aDate)
                                    aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                    nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                                else:
                                    nextDayPostionDf.loc[(longBoolindex, 'vol')] = nextDayPostionDf.loc[(
                                     longBoolindex, 'vol')] - vol
                        if dire == '卖':
                            if positionEffect in self.clearName:
                                aLongPosition = nextDayPostionDf.loc[longBoolindex]
                                if aLongPosition.empty:
                                    aTuple = (
                                     sym, 'long', vol, tradePirce, aDate)
                                    aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                    nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                                else:
                                    nextDayPostionDf.loc[(longBoolindex, 'vol')] = nextDayPostionDf.loc[(
                                     longBoolindex, 'vol')] + vol
                        if dire == '卖' and positionEffect == '开仓' or dire == '买':
                            if positionEffect in self.clearName:
                                shortBoolindex = (nextDayPostionDf['symbol'] == sym) & (nextDayPostionDf['positionSide'] == 'short')
                        if dire == '卖':
                            if positionEffect == '开仓':
                                aSeriesPos = nextDayPostionDf.loc[shortBoolindex]
                                if aSeriesPos.empty:
                                    aTuple = (
                                     sym, 'short', -vol, tradePirce, aDate)
                                    aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                    nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                                else:
                                    nextDayPostionDf.loc[(shortBoolindex, 'vol')] = nextDayPostionDf.loc[(
                                     shortBoolindex, 'vol')] - vol
                        if dire == '买' and positionEffect in self.clearName:
                            aSeriesPos = nextDayPostionDf.loc[shortBoolindex]
                            if aSeriesPos.empty:
                                aTuple = (
                                 sym, 'short', vol, tradePirce, aDate)
                                aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                            else:
                                nextDayPostionDf.loc[(shortBoolindex, 'vol')] = nextDayPostionDf.loc[(
                                 shortBoolindex, 'vol')] + vol

                    nextDayPostionDf = nextDayPostionDf.loc[(nextDayPostionDf['vol'] != 0)]
                    positionEveryDayDf = positionEveryDayDf.append(nextDayPostionDf)

        return positionEveryDayDf

    def positionProfit(self, positionEveryDayDf, closeData):
        maxDate = positionEveryDayDf['tradeDate'].max()

        def afun(aRow):
            sym = aRow['symbol']
            date = aRow['tradeDate']
            close = closeData.loc[(date, sym)]
            symData = closeData[sym].dropna()
            preClose = symData.loc[(symData.index < date)].iloc[(-1)]
            if np.isnan(close) or np.isnan(preClose):
                print('close is nan')
            aRow['close'] = close
            aRow['preClose'] = preClose
            aRow['mul'] = self.mulDict[sym]
            if aRow['positionSide'] == 'long':
                aRow['profit'] = (aRow['close'] - aRow['preClose']) * aRow['mul'] * aRow['vol'] * 1
            if aRow['positionSide'] == 'short':
                aRow['profit'] = (aRow['close'] - aRow['preClose']) * aRow['mul'] * aRow['vol'] * -1
            return aRow

        yesDayPositionDf = positionEveryDayDf.copy()
        yesDayPositionDf['tradeDate'] = yesDayPositionDf['tradeDate'].apply((self.aCusCalendar.tradingDaysOffset), args=(1, ))
        cmpDate = closeData.index[(-1)]
        yesDayPositionDf = yesDayPositionDf.loc[(yesDayPositionDf['tradeDate'] <= cmpDate)]
        adjustPoProfitDF = yesDayPositionDf.apply(afun, axis=1)
        return adjustPoProfitDF

    def profitEveryTDay(self, finalPostionDF, symbolflag='underlyingSymbol'):
        currNeedContract = self.jiaogeDf['symbol'].drop_duplicates().values
        tradeSDate = self.jiaogeDf['tradeDate'].iloc[0]
        tradeDate = self.jiaogeDf['tradeDate'].iloc[(-1)]
        hSDate = self.aCusCalendar.tradingDaysOffset(tradeSDate, -1)
        hqdata = gm3HelpBylw.getHQData_Fade(currNeedContract, hSDate, tradeDate, fre='1d', fields_='symbol,eob,close')
        hqdata['eob'] = hqdata['eob'].dt.strftime('%Y-%m-%d %H:%M:%S')
        hqdata['eob'] = hqdata['eob'].str[0:10]
        closeData = hqdata.pivot(index='eob', columns='symbol', values='close')
        positionDf = self.purePositionEveryDay(finalPostionDF)
        if not positionDf.empty:
            positionProfitDf = self.positionProfit(positionDf, closeData)
        else:
            positionProfitDf = pd.DataFrame(columns=['symbol', 'positionSide', 'vol', 'cost', 'tradeDate', 'profit'])
        if symbolflag == 'underlyingSymbol':
            positionProfitDf['underLyingSym'] = positionProfitDf['symbol'].apply(commonHelpBylw.getMainContinContract)
            positionProfitDf = positionProfitDf.groupby(by=['underLyingSym', 'tradeDate'])['profit'].apply(sum)
            positionProfitDf = positionProfitDf.reset_index()
            positionProfitDf = positionProfitDf.rename(columns={'underLyingSym': 'symbol'})
        tradeProfit = self.tradeProfitVSClose(closeData)
        if symbolflag == 'underlyingSymbol':
            tradeProfit['underLyingSym'] = tradeProfit['symbol'].apply(commonHelpBylw.getMainContinContract)
            tradeProfit = tradeProfit.groupby(by=['underLyingSym', 'tradeDate'])['tradeProfit'].apply(sum)
            tradeProfit = tradeProfit.reset_index()
            tradeProfit = tradeProfit.rename(columns={'underLyingSym': 'symbol'})
        profitEveryTDayDf = tradeProfit.copy()
        profitEveryTDayDf = profitEveryTDayDf.rename(columns={'tradeProfit': 'profit'})
        profitEveryTDayDf = profitEveryTDayDf.pivot(index='tradeDate', columns='symbol', values='profit')
        aDateDf = self.aCusCalendar.getADateTimeSeries(hSDate, tradeDate).to_frame()
        adf = pd.merge(profitEveryTDayDf, aDateDf, how='right', left_index=True, right_on='tradingDays')
        adf = adf.fillna(0)
        adf = adf.reset_index(drop=True)
        for ainx, arow in positionProfitDf.iterrows():
            sym = arow['symbol']
            dt = arow['tradeDate']
            profit = arow['profit']
            adf.loc[(adf['tradingDays'] == dt, sym)] = adf.loc[(adf['tradingDays'] == dt, sym)] + profit

        return adf

    def netAssetValueTDay(self, finalPostionDF, iniCash):
        profitEveryDayDf = self.profitEveryTDay(finalPostionDF)
        colNameList = list(profitEveryDayDf.columns)
        colNameList.remove('tradingDays')
        netprofitEDay = profitEveryDayDf.copy()
        netprofitEDay['allprofit'] = 0
        for aCname in colNameList:
            netprofitEDay['allprofit'] = netprofitEDay['allprofit'] + netprofitEDay[aCname]

        netprofitEDay['NetAssetValue'] = netprofitEDay['allprofit']
        netprofitEDay['NetAssetValue'].iloc[0] = iniCash
        netprofitEDay['NetAssetValue'] = netprofitEDay['NetAssetValue'].cumsum()
        return netprofitEDay

    def yepanAmount(self, yepanDF):
        adjustJiaogedanDF = self.jiaogeDf.copy()
        adjustJiaogedanDF['mainContra'] = adjustJiaogedanDF['symbol'].apply(commonHelpBylw.getMainContract)
        yepanMerge = pd.merge(yepanDF, adjustJiaogedanDF, left_on='symbol', right_on='mainContra', how='right')
        yepanMerge['amount'] = yepanMerge['tradePrice'] * yepanMerge['volume'] * yepanMerge['mul']
        return yepanMerge

    def mergeTrades(self, seconds=1800):
        adjustJiaogedanDF = self.jiaogeDf.copy()
        adjustJiaogedanDF['tradeDateTime'] = pd.to_datetime((adjustJiaogedanDF['tradeDateTime']), format='%Y-%m-%d %H:%M:%S')

        def mergefun(adf):
            finanlDf = pd.DataFrame()
            nextDf = adf.copy()
            while not nextDf.empty:
                eDt = nextDf['tradeDateTime'].iloc[0] + datetime.timedelta(seconds=seconds)
                currDf = nextDf.loc[(adf['tradeDateTime'] <= eDt)]
                nextDf = nextDf.loc[(adf['tradeDateTime'] > eDt)]
                tempMergeDf = currDf.head(1)
                tempMergeDf['volume'] = currDf['volume'].sum()
                tempMergeDf['commission'] = currDf['commission'].sum()
                finanlDf = finanlDf.append(tempMergeDf)

            return finanlDf

        ss = adjustJiaogedanDF.groupby(['symbol', 'direction', 'PositionEffect']).apply(mergefun)
        ss = ss.reset_index(drop=True)
        return ss