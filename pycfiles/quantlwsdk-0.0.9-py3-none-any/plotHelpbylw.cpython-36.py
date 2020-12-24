# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\highcharts\plotHelpbylw.py
# Compiled at: 2020-04-04 05:11:32
# Size of source mod 2**32: 15907 bytes
from .version import version_info, __version__
from .highcharts.highcharts import Highchart
from .highmaps.highmaps import Highmap
from .highstock.highstock import Highstock
from . import ipynb
import sys
sys.path.append('..\\..')
from pyalgotrade.broker import gmEnum
from pyalgotrade import gm3HelpBylw
import json

def dftounixTimestamp(arow):
    adt = arow.to_pydatetime()
    ats = int(adt.timestamp() * 1000)
    return ats


def plotLine(dataDf, symbol_):
    dataDf.columns = [
     'date', 'close']
    sttt = "'abc'cced"
    atooltipValue = {'pointFormat': '\'<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>\',changeDecimals: 2,valueDecimals: 2'}
    H = createAHStock(symbol_)
    H.set_options('plotOptions', {'series': {'compare': 'percent'}})
    addASeries(H, dataDf, symbol_, tooltip=atooltipValue, marker={'enabled':True,  'radius':5})
    return H


def plotSingleLine(dataDf, symbol_):
    dataDf.columns = [
     'date', 'close']
    H = createAHStock(symbol_)
    addASeries(H, dataDf, symbol_, marker={'enabled':True,  'radius':5})
    return H


def plotPoint(dataDf, symbol_):
    dataDf.columns = ['date', 'pValue']
    i = 1


def createAHStock(symbol_):
    options = {'global':{'timezoneOffset': -480}, 
     'rangeSelector':{'selected': 1}, 
     'plotOptions':{'series': {'turboThreshold':100000, 
                 'states':{'inactive': {'opacity': 1}}, 
                 'dataGrouping':{'enabled': False}}}, 
     'title':{'text': symbol_}, 
     'tooltip':{'crosshairs':[
       True, True], 
      'xDateFormat':'%Y-%m-%d %H:%M:%S', 
      'shared':True}}
    from win32api import GetSystemMetrics
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    divStyle = 'min-width:100%%;min-height:%dpx' % int(height * 0.8)
    H = Highstock(divstyle=divStyle)
    H.set_dict_options(options)
    return H


def plotCandle(H, dataDf, symbol_):
    dataDf.columns = [
     'date', 'open', 'high', 'low', 'close']
    adjustPE = dataDf.reset_index()

    def afun(arow):
        adt = arow.to_pydatetime()
        ats = int(adt.timestamp() * 1000)
        return ats

    adjustPE['eobTstamp'] = adjustPE['date'].apply(afun)
    adjustPE = adjustPE[['eobTstamp', 'open', 'high', 'low', 'close']]
    peData = adjustPE.values.tolist()
    for alist in peData:
        alist[0] = int(alist[0])

    H.add_data_set(peData, 'candlestick', symbol_, tooltip={'valueDecimals': 2},
      allowPointSelect=True,
      color='green',
      upColor='red')
    xAxis = {}
    options = {}
    if adjustPE.shape[0] > 400:
        xAxis['min'] = int(adjustPE['eobTstamp'].iloc[0])
        xAxis['max'] = int(adjustPE['eobTstamp'].iloc[400])
        options['xAxis'] = xAxis
    H.set_dict_options(options)


def setAxisMinMax(H, adjustPE):
    xAxis = {}
    options = {}
    if adjustPE.shape[0] > 400:
        xAxis['min'] = int(adjustPE['eobTstamp'].iloc[0])
        xAxis['max'] = int(adjustPE['eobTstamp'].iloc[400])
        options['xAxis'] = xAxis
    H.set_dict_options(options)


def addMA(H, mainDataId, period=14, index=0):
    parDict = {'period':period, 
     'index':index}
    anameStr = 'sma(%d)' % period
    H.add_data_set([], 'sma', name=anameStr, linkedTo=mainDataId, params=parDict)


def addAIndictor(H, mainDataId, indicatorType, period=14, index=0, yaxisIndex=0, **kwargs):
    parDict = {'period':period, 
     'index':index}
    anameStr = '%s(%d)' % (indicatorType, period)
    (H.add_data_set)([], indicatorType, name=anameStr, linkedTo=mainDataId, params=parDict, yAxis=yaxisIndex, **kwargs)


def addMacd(H, mainDataId, speriod=12, longperiod=26, signalperiod=9, yaxisIndex=1, index=3):
    parDict = {'shortPeriod':speriod, 
     'longPeriod':longperiod,  'signalPeriod':signalperiod,  'period':longperiod,  'index':index}
    atooltipValue = {'pointFormatter': 'function() {\n            var seriesOptions = this.series.options,\n            str = \'<b>MACD (26, 12, 9)</b><br>\';\n            function getLine(color, name, value){\n                return \'<span style="color:\' + color + \'">\\u25CF</span> \' + name + \': <b>\' + value + \'</b><br/>\';\n    }\n    str += getLine(seriesOptions.macdLine.styles.lineColor, \'diff\', this.MACD.toFixed(2));\n    str += getLine(seriesOptions.signalLine.styles.lineColor, \'dea\', this.signal.toFixed(2));\n    str += getLine(seriesOptions.color, \'macd\', this.y.toFixed(2));\n    return str;\n}'}
    tststr = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    macdLineValue = {'styles': {'lineColor':'blue',  'lineWidth':1}}
    signalLineValue = {'styles': {'lineColor':'red',  'lineWidth':1}}
    color = 'lightblue'
    H.add_data_set([], 'macd', name='macdIndicator', linkedTo=mainDataId, params=parDict, macdLine=macdLineValue, signalLine=signalLineValue,
      color=color,
      yAxis=yaxisIndex,
      tooltip=atooltipValue)


def plotSingal(H, signalDf, symbol):
    signalDf['TStamp'] = signalDf['date'].apply(dftounixTimestamp)
    aList = []
    for index_, row in signalDf.iterrows():
        adict = {}
        title = row['signalname']
        adict['title'] = title
        adict['text'] = title
        x = row['TStamp']
        adict['x'] = x
        aList.append(adict)

    H.add_data_set(aList, 'flags', ('flag-' + symbol), onSeries=symbol, allowOverlapX=True, stackDistance=20)


def plotBuySell(H, buysellData, symbol):
    i = 1
    buysellData['TStamp'] = buysellData['date'].apply(dftounixTimestamp)
    aList = []
    for index_, row in buysellData.iterrows():
        adict = {}
        if row['positionEffect'] == gmEnum.PositionEffect_Open:
            if row['positionSide'] == gmEnum.PositionSide_Long:
                title = 'openlong'
        if row['positionEffect'] == gmEnum.PositionEffect_Open:
            if row['positionSide'] == gmEnum.PositionSide_Short:
                title = 'openshort'
        if row['positionEffect'] == gmEnum.PositionEffect_Close:
            if row['positionSide'] == gmEnum.PositionSide_Long:
                title = 'clearlong'
        if row['positionEffect'] == gmEnum.PositionEffect_Close:
            if row['positionSide'] == gmEnum.PositionSide_Short:
                title = 'clearshort'
        adict['title'] = title
        text = 'price:%f,volumne:%d' % (row['price'], row['volume'])
        adict['text'] = text
        x = row['TStamp']
        adict['x'] = x
        aList.append(adict)

    H.add_data_set(aList, 'flags', symbol, onSeries=symbol, allowOverlapX=True)
    i = 1


def addASeries(H, aSeriesData, sName, yaxisIndex=0, seriesType='line', setMax=False, **kwargs):
    aSeriesData.columns = [
     'date', sName]
    adjustPE = aSeriesData.copy()
    adjustPE['eobTstamp'] = adjustPE['date'].apply(dftounixTimestamp)
    adjustPE = adjustPE[['eobTstamp', sName]]
    peData = adjustPE.values.tolist()
    for alist in peData:
        alist[0] = int(alist[0])

    if setMax:
        xAxis = {}
        options = {}
        if adjustPE.shape[0] > 400:
            xAxis['min'] = int(adjustPE['eobTstamp'].iloc[0])
            xAxis['max'] = int(adjustPE['eobTstamp'].iloc[400])
            options['xAxis'] = xAxis
        H.set_dict_options(options)
    (H.add_data_set)(peData, seriesType, sName, allowPointSelect=True, 
     yAxis=yaxisIndex, **kwargs)
    i = 1


def plotMainContractCandle(underlyingAsset, sDateTime, eDateTime, fre='60s'):
    H = createAHStock(underlyingAsset)
    hqDF = gm3HelpBylw.getHQDataOfMainContract_Fade([underlyingAsset], sDateTime, eDateTime, fre)
    aPlotData = hqDF[['eob', 'open', 'high', 'low', 'close']]
    plotCandle(H, aPlotData, underlyingAsset)
    hqDF['symbolShift1'] = hqDF['symbol'].shift(1)
    newDf = hqDF.loc[(hqDF['symbolShift1'] != hqDF['symbol'])]
    newDf = newDf.dropna()
    newDf['TStamp'] = newDf['eob'].apply(dftounixTimestamp)
    for index_, row in newDf.iterrows():
        title = row['symbol']
        x = row['TStamp']
        plotLinedict = {'value':x,  'width':2, 
         'color':'red', 
         'id':underlyingAsset, 
         'label':{'text':title, 
          'align':'left',  'x':10}}
        astr = json.dumps(plotLinedict)
        jsStript = 'chart.xAxis[0].addPlotLine(%s)' % astr
        H.add_JSscript(jsStript, 'end')

    return H


def plotAContractCandle(underlyingAsset, sDateTime, eDateTime, fre='60s', adjust=1):
    H = createAHStock(underlyingAsset)
    hqDF = gm3HelpBylw.getHQData_Fade([underlyingAsset], sDateTime, eDateTime, fre, adjust=adjust)
    aPlotData = hqDF[['eob', 'open', 'high', 'low', 'close']]
    plotCandle(H, aPlotData, underlyingAsset)
    return H


def plotTradeSigByOrderRecord(H, orderRecord):
    orderRecord.columns = [
     'date', '委托方向', '成交数量', '成交均价']
    aSeriesData = orderRecord[['date', '成交均价']]
    str11 = 'function() {\n                        return this.y.toFixed(3);\n                    }'
    addASeries(H, aSeriesData, 'tradePrice', yaxisIndex=0, seriesType='line', setMax=False, lineWidth=0, marker={'enabled':True, 
     'radius':5},
      dataLabels={'enabled':True,  'formatter':str11})
    orderRecord['signalname'] = orderRecord['委托方向'] + ':' + orderRecord['成交数量'].astype(str)
    sigDF = orderRecord[['date', 'signalname']]
    plotSingal(H, sigDF, 'tradePrice')
    return H