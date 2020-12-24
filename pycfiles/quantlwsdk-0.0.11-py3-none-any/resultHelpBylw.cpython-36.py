# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\resultHelpBylw.py
# Compiled at: 2020-04-04 05:11:32
# Size of source mod 2**32: 21393 bytes
"""
20190819   14：30

@author: lw 李文
"""
from __future__ import print_function, absolute_import, unicode_literals
import numpy as np, pandas as pd
from datetime import timezone
from datetime import timedelta
from collections import deque
import sys
from pyalgotrade import gm3HelpBylw
from pyalgotrade import commonHelpBylw
import copy, time
try:
    import talib
except:
    print('请安装TA-Lib库')

from gm.api import *
from highcharts import plotHelpbylw
from pyalgotrade.utils import parseToGmFre, freMapFromGM

def writeBackTestResult(strategyParams, strategyBackTestIndicator, btestID, resultFile, enconding='gbk'):
    arow = []
    backTestID = btestID
    arow.append(strategyParams)
    arow.append(strategyBackTestIndicator.pnl_ratio)
    arow.append(strategyBackTestIndicator.pnl_ratio_annual)
    arow.append(strategyBackTestIndicator.max_drawdown)
    arow.append(strategyBackTestIndicator.calmar_ratio)
    arow.append(strategyBackTestIndicator.sharp_ratio)
    arow.append(strategyBackTestIndicator.open_count)
    arow.append(strategyBackTestIndicator.close_count)
    arow.append(strategyBackTestIndicator.win_ratio)
    arow.append(backTestID)
    with open(resultFile, 'a', newline='', encoding=enconding) as (csvFile):
        import csv
        writer = csv.writer(csvFile)
        writer.writerow(arow)


def plotBackTestResult(underLysymbol, bTestParams, logDataPathDir, figPathDir, plotSDateTime, plotEDateTime, firstYVarsname=[], secondYVarsname=[]):
    for aUnderLyAsset in underLysymbol:
        try:
            with open((logDataPathDir + aUnderLyAsset + '-orderRecord.txt'), encoding='gbk') as (f):
                dfOrderSingal = pd.read_csv(f, header=None, sep=',')
                dfOrderSingal.columns = [
                 'createdAt', 'symbol', 'signalname']
                dfOrderSingal = dfOrderSingal.loc[((dfOrderSingal['createdAt'] >= plotSDateTime) & (dfOrderSingal['createdAt'] <= plotEDateTime))]
                dfOrderSingal['date'] = pd.to_datetime((dfOrderSingal['createdAt']), format='%Y-%m-%d %H:%M:%S')
                dfOrderSingal['date'] = dfOrderSingal['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))
            if dfOrderSingal.empty:
                pass
            else:
                symbol_ = dfOrderSingal['symbol'].iloc[(-1)]
        except Exception as e:
            print(e)

        mainSymbol = aUnderLyAsset
        sfrestr = bTestParams[aUnderLyAsset]['fre']
        gmFreStr = parseToGmFre(sfrestr)
        H = plotHelpbylw.plotMainContractCandle(mainSymbol, plotSDateTime, plotEDateTime, fre=gmFreStr)
        plotHelpbylw.plotSingal(H, dfOrderSingal, mainSymbol)
        if len(secondYVarsname) >= 1:
            yAxis = [
             {'height':'70%', 
              'resize':{'enabled': True}},
             {'top':'70%', 
              'height':'30%'}]
            H.set_options('yAxis', yAxis)

        def addASeries(varsname, yaxisindex):
            for aname in varsname:
                with open((logDataPathDir + '%s-%s.txt' % (aUnderLyAsset, aname)), encoding='gbk') as (f):
                    aVar = pd.read_csv(f, header=None, sep=',')
                    aVar.columns = ['createdAt', aname]
                    aVar = aVar.loc[((aVar['createdAt'] >= plotSDateTime) & (aVar['createdAt'] <= plotEDateTime))]
                    aVar['date'] = pd.to_datetime((aVar['createdAt']), format='%Y-%m-%d %H:%M:%S')
                    aVar['date'] = aVar['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))
                if aname == 'macd':
                    plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex, seriesType='column')
                else:
                    plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex)

        addASeries(firstYVarsname, 0)
        addASeries(secondYVarsname, 1)
        filename = figPathDir + mainSymbol
        H.save_file(filename)

    i = 1


def plotResultAndStopLossProfitMulContract(logDataPathDir, plotSDateTime, plotEDateTime, bTestParams, firstYVarsname=[], secondYVarsname=[]):
    import os, re

    def getOrder(filePath):
        fileNameList = os.listdir(filePath)
        absPath = os.path.abspath(filePath)
        dfOrderSingal = pd.DataFrame(columns=['createdAt', 'symbol', 'signalname'])
        for afName in fileNameList:
            fDirAndName = os.path.join(absPath, afName)
            try:
                with open(fDirAndName, encoding='gbk') as (f):
                    tmpd = pd.read_csv(f, header=None, sep=',')
                    tmpd.columns = ['createdAt', 'symbol', 'signalname']
                    dfOrderSingal = dfOrderSingal.append(tmpd, ignore_index=True)
            except Exception as e:
                print(e)

        return dfOrderSingal

    dfOrderSingal = getOrder(logDataPathDir + 'orderRecord')
    stopFilePath = logDataPathDir.replace('log', 'stopLossProfitLog')
    stopOrder = getOrder(stopFilePath + '' + 'orderRecord')
    dfOrderSingal = dfOrderSingal.append(stopOrder)
    dfOrderSingal = dfOrderSingal.loc[((dfOrderSingal['createdAt'] >= plotSDateTime) & (dfOrderSingal['createdAt'] <= plotEDateTime))]
    dfOrderSingal['date'] = pd.to_datetime((dfOrderSingal['createdAt']), format='%Y-%m-%d %H:%M:%S')
    dfOrderSingal['date'] = dfOrderSingal['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))

    def addASeries(varsname, yaxisindex):
        interResultAbsPath = os.path.abspath(logDataPathDir + 'interResult')
        for aname in varsname:
            filenameAndPath = os.path.join(interResultAbsPath, asymbol + '-' + aname + '.txt')
            with open(filenameAndPath, encoding='gbk') as (f):
                aVar = pd.read_csv(f, header=None, sep=',')
                aVar.columns = ['createdAt', aname]
                aVar = aVar.loc[((aVar['createdAt'] >= plotSDateTime) & (aVar['createdAt'] <= plotEDateTime))]
                aVar['date'] = pd.to_datetime((aVar['createdAt']), format='%Y-%m-%d %H:%M:%S')
                aVar['date'] = aVar['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))
            if aname == 'macd':
                plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex, seriesType='column')
            else:
                plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex)

    symlist = list(dfOrderSingal['symbol'].drop_duplicates().values)
    for asymbol in symlist:
        aUnderLyAsset = commonHelpBylw.getMainContinContract(asymbol)
        if asymbol == 'DCE.j2001':
            i = 1
        if aUnderLyAsset not in bTestParams.keys():
            pass
        else:
            sfrestr = bTestParams[aUnderLyAsset]['fre']
            gmFreStr = parseToGmFre(sfrestr)
            H = plotHelpbylw.plotAContractCandle(asymbol, plotSDateTime, plotEDateTime, fre=gmFreStr)
            currDf = dfOrderSingal.loc[(dfOrderSingal['symbol'] == asymbol)]
            plotHelpbylw.plotSingal(H, currDf, asymbol)
            addASeries(firstYVarsname, 0)
            if len(secondYVarsname) >= 1:
                yAxis = [
                 {'height':'70%', 
                  'resize':{'enabled': True}},
                 {'top':'70%', 
                  'height':'30%'}]
                H.set_options('yAxis', yAxis)
                addASeries(secondYVarsname, 1)
            filename = logDataPathDir + asymbol
            H.save_file(filename)


def plotStockResultMulContract(logDataPathDir, plotSDateTime, plotEDateTime, bTestParams, firstYVarsname=[], secondYVarsname=[]):
    import os, re

    def getOrder(filePath):
        fileNameList = os.listdir(filePath)
        absPath = os.path.abspath(filePath)
        dfOrderSingal = pd.DataFrame(columns=['createdAt', 'symbol', 'signalname'])
        for afName in fileNameList:
            fDirAndName = os.path.join(absPath, afName)
            try:
                with open(fDirAndName, encoding='gbk') as (f):
                    tmpd = pd.read_csv(f, header=None, sep=',')
                    tmpd.columns = ['createdAt', 'symbol', 'signalname']
                    dfOrderSingal = dfOrderSingal.append(tmpd, ignore_index=True)
            except Exception as e:
                print(e)

        return dfOrderSingal

    dfOrderSingal = getOrder(logDataPathDir + 'orderRecord')
    dfOrderSingal = dfOrderSingal.loc[((dfOrderSingal['createdAt'] >= plotSDateTime) & (dfOrderSingal['createdAt'] <= plotEDateTime))]
    dfOrderSingal['date'] = pd.to_datetime((dfOrderSingal['createdAt']), format='%Y-%m-%d %H:%M:%S')
    dfOrderSingal['date'] = dfOrderSingal['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))

    def addASeries(varsname, yaxisindex):
        interResultAbsPath = os.path.abspath(logDataPathDir + 'interResult')
        for aname in varsname:
            filenameAndPath = os.path.join(interResultAbsPath, asymbol + '-' + aname + '.txt')
            with open(filenameAndPath, encoding='gbk') as (f):
                aVar = pd.read_csv(f, header=None, sep=',')
                aVar.columns = ['createdAt', aname]
                aVar = aVar.loc[((aVar['createdAt'] >= plotSDateTime) & (aVar['createdAt'] <= plotEDateTime))]
                aVar['date'] = pd.to_datetime((aVar['createdAt']), format='%Y-%m-%d %H:%M:%S')
                aVar['date'] = aVar['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))
            if aname == 'macd':
                plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex, seriesType='column')
            else:
                plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex)

    symlist = list(dfOrderSingal['symbol'].drop_duplicates().values)
    for asymbol in symlist:
        aUnderLyAsset = asymbol
        if asymbol == 'DCE.j2001':
            i = 1
        sfrestr = bTestParams[aUnderLyAsset]['fre']
        gmFreStr = parseToGmFre(sfrestr)
        H = plotHelpbylw.plotAContractCandle(asymbol, plotSDateTime, plotEDateTime, fre=gmFreStr)
        currDf = dfOrderSingal.loc[(dfOrderSingal['symbol'] == asymbol)]
        plotHelpbylw.plotSingal(H, currDf, asymbol)
        addASeries(firstYVarsname, 0)
        if len(secondYVarsname) >= 1:
            yAxis = [
             {'height':'70%', 
              'resize':{'enabled': True}},
             {'top':'70%', 
              'height':'30%'}]
            H.set_options('yAxis', yAxis)
            addASeries(secondYVarsname, 1)
        filename = logDataPathDir + asymbol
        H.save_file(filename)


def plotStockResultSingleContract(logDataPathDir, plotSDateTime, plotEDateTime, paramsDict, firstYVarsname=[], secondYVarsname=[]):
    import os

    def getOrder(filePath):
        fileNameList = os.listdir(filePath)
        absPath = os.path.abspath(filePath)
        dfOrderSingal = pd.DataFrame(columns=['createdAt', 'symbol', 'signalname'])
        for afName in fileNameList:
            fDirAndName = os.path.join(absPath, afName)
            try:
                with open(fDirAndName, encoding='gbk') as (f):
                    tmpd = pd.read_csv(f, header=None, sep=',')
                    tmpd.columns = ['createdAt', 'symbol', 'signalname']
                    dfOrderSingal = dfOrderSingal.append(tmpd, ignore_index=True)
            except Exception as e:
                print(e)

        return dfOrderSingal

    dfOrderSingal = getOrder(logDataPathDir + 'orderRecord')
    dfOrderSingal = dfOrderSingal.loc[((dfOrderSingal['createdAt'] >= plotSDateTime) & (dfOrderSingal['createdAt'] <= plotEDateTime))]
    dfOrderSingal['date'] = pd.to_datetime((dfOrderSingal['createdAt']), format='%Y-%m-%d %H:%M:%S')
    dfOrderSingal['date'] = dfOrderSingal['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))

    def addASeries(varsname, yaxisindex):
        interResultAbsPath = os.path.abspath(logDataPathDir + 'interResult')
        for aname in varsname:
            filenameAndPath = os.path.join(interResultAbsPath, asymbol + '-' + aname + '.txt')
            with open(filenameAndPath, encoding='gbk') as (f):
                aVar = pd.read_csv(f, header=None, sep=',')
                aVar.columns = ['createdAt', aname]
                aVar = aVar.loc[((aVar['createdAt'] >= plotSDateTime) & (aVar['createdAt'] <= plotEDateTime))]
                aVar['date'] = pd.to_datetime((aVar['createdAt']), format='%Y-%m-%d %H:%M:%S')
                aVar['date'] = aVar['date'].dt.tz_localize(tz=(timezone(timedelta(hours=8))))
            if aname == 'macd':
                plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex, seriesType='column')
            else:
                plotHelpbylw.addASeries(H, (aVar[['date', aname]]), aname, yaxisIndex=yaxisindex)

    symlist = list(dfOrderSingal['symbol'].drop_duplicates().values)
    for asymbol in symlist:
        aUnderLyAsset = asymbol
        if asymbol == 'DCE.j2001':
            i = 1
        sfrestr = paramsDict['fre']
        gmFreStr = parseToGmFre(sfrestr)
        H = plotHelpbylw.plotAContractCandle(asymbol, plotSDateTime, plotEDateTime, fre=gmFreStr)
        currDf = dfOrderSingal.loc[(dfOrderSingal['symbol'] == asymbol)]
        plotHelpbylw.plotSingal(H, currDf, asymbol)
        addASeries(firstYVarsname, 0)
        if len(secondYVarsname) >= 1:
            yAxis = [
             {'height':'70%', 
              'resize':{'enabled': True}},
             {'top':'70%', 
              'height':'30%'}]
            H.set_options('yAxis', yAxis)
            addASeries(secondYVarsname, 1)
        filename = logDataPathDir + asymbol
        H.save_file(filename)