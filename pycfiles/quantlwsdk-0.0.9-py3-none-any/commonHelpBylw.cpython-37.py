# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\commonHelpBylw.py
# Compiled at: 2020-04-04 05:11:32
# Size of source mod 2**32: 33271 bytes
"""
Created on Wed Apr  4 16:12:37 2018

@author: SH
"""
import pandas as pd, sys
sys.path.append('E://sihuanlw4SVN//framework')
import logging, re, numpy as np
from pyalgotrade import calendayBylw
FUTURES_CN_Day_STARTTIME_N001 = '21:00:00'
FUTURES_CN_Day_STARTTIME_N002 = '09:00:00'
FUTURES_CN_Day_ENDTIME = '15:00:00'
FUTURES_CN_SYMNAME_MAP_SYMID = {'沪深主连':'CFFEX.IF', 
 '上证主连':'CFFEX.IH', 
 '中证主连':'CFFEX.IC', 
 '债五主连':'CFFEX.TF', 
 '债十主连':'CFFEX.T', 
 '债二主连':'CFFEX.TS', 
 '沪铜主连':'SHFE.CU', 
 '沪金主连':'SHFE.AU', 
 '沪银主连':'SHFE.AG', 
 '沪锌主连':'SHFE.ZN', 
 '沪铝主连':'SHFE.AL', 
 '橡胶主连':'SHFE.RU', 
 '螺纹主连':'SHFE.RB', 
 '燃油主连':'SHFE.FU', 
 '热卷主连':'SHFE.HC', 
 '沥青主连':'SHFE.BU', 
 '沪铅主连':'SHFE.PB', 
 '沪镍主连':'SHFE.NI', 
 '沪锡主连':'SHFE.SN', 
 '线材主连':'SHFE.WR', 
 '原油主连':'INE.SC', 
 '豆一主连':'DCE.A', 
 '豆二主连':'DCE.B', 
 '玉米主连':'DCE.C', 
 '淀粉主连':'DCE.CS', 
 '纤板主连':'DCE.FB', 
 '铁矿主连':'DCE.I', 
 '焦炭主连':'DCE.J', 
 '鸡蛋主连':'DCE.JD', 
 '焦煤主连':'DCE.JM', 
 '塑料主连':'DCE.L', 
 '豆粕主连':'DCE.M', 
 '棕榈主连':'DCE.P', 
 'PP主连':'DCE.PP', 
 'PVC主连':'DCE.V', 
 '豆油主连':'DCE.Y', 
 '棉花主连':'CZCE.CF', 
 '棉纱主连':'CZCE.CY', 
 '白糖主连':'CZCE.SR', 
 'PTA主连':'CZCE.TA', 
 '菜油主连':'CZCE.OI', 
 '甲醇主连':'CZCE.MA', 
 '玻璃主连':'CZCE.FG', 
 '菜粕主连':'CZCE.RM', 
 '郑煤主连':'CZCE.ZC', 
 '粳稻主连':'CZCE.JR', 
 '晚稻主连':'CZCE.LR', 
 '硅铁主连':'CZCE.SF', 
 '锰硅主连':'CZCE.SM', 
 '苹果主连':'CZCE.AP', 
 '铁矿':'DCE.I', 
 '苹果':'CZCE.AP', 
 '甲醇':'CZCE.MA', 
 '螺纹':'SHFE.RB', 
 '镍':'SHFE.NI', 
 '白糖':'CZCE.SR', 
 'PTA':'CZCE.TA', 
 '棉花':'CZCE.CF', 
 '橡胶':'SHFE.RU', 
 '豆油':'DCE.Y', 
 '燃料油':'SHFE.FU', 
 '原油':'INE.SC', 
 'PP':'DCE.PP', 
 'EG':'DCE.EG', 
 '焦炭':'DCE.J', 
 '白银':'SHFE.AG', 
 '纸浆':'SHFE.SP', 
 '沥青':'SHFE.BU', 
 '鸡蛋':'DCE.JD', 
 '豆粕':'DCE.M', 
 '玉米':'DCE.C', 
 '动力煤':'CZCE.ZC', 
 '锰硅':'CZCE.SM'}
STOCKS_CN_SYMNAME_MAP_SYMID = {'300ETF':'SHSE.510300', 
 '500ETF':'SHSE.510500', 
 '标普500':'SHSE.513500', 
 '纳指ETF':'SHSE.513100', 
 '创业板50':'SZSE.159949'}

def splitASymbol(aSymbol):
    atemp = aSymbol.split('.')
    exchange = atemp[0]
    secID = atemp[1]
    secSymbol = ''
    secYear = ''
    secMonth = ''
    secDict = {}
    if exchange == 'CZCE' or exchange == 'SHFE':
        secSymbol = secID[0:2]
        secMonth = secID[-2:]
    if exchange == 'DCE':
        if secID[0:2] in ('jm', 'jd', 'cs', 'pp'):
            secSymbol = secID[0:2]
            secMonth = secID[-2:]
        else:
            if secID[0:1] in ('a', 'c', 'i', 'j', 'l', 'm', 'p', 'v', 'y'):
                secSymbol = secID[0:1]
                secMonth = secID[-2:]
    elif exchange == 'CFFEX':
        if secID[0:2] in ('IC', 'IH', 'IF', 'TF'):
            secSymbol = secID[0:2]
            secMonth = secID[-2:]
    else:
        if secID[0:1] in ('T', ):
            secSymbol = secID[0:1]
            secMonth = secID[-2:]
        secYear = secID.replace(secSymbol, '').replace(secMonth, '')
        secDict['secSymbol'] = exchange + '.' + secSymbol
        secDict['secYear'] = secYear
        secDict['secMonth'] = secMonth
        import datetime
        strtime = datetime.datetime.now().strftime('%Y-%m-%d')
        if exchange == 'CZCE':
            strNext1Year = str(int(strtime[0:4]) + 1)
            strNext2Year = str(int(strtime[0:4]) + 2)
            if strtime[3] == secYear:
                secDict['secRealYear'] = strtime[2] + secYear
            if strNext1Year[3] == secYear:
                secDict['secRealYear'] = strNext1Year[2] + secYear
            if strNext2Year[3] == secYear:
                secDict['secRealYear'] = strNext2Year[2] + secYear
        else:
            secDict['secRealYear'] = secYear
    return secDict


def juejinSymbol(x):
    if x[0] in ('5', '6'):
        return 'SHSE.' + x
    return 'SZSE.' + x


def adjustSymbol(aSym):
    if '.' in aSym:
        splitSym = aSym.split('.')
        if 'DCE' in aSym or 'SHFE' in aSym:
            adjustSym = splitSym[0] + '.' + splitSym[1].lower()
            return adjustSym
        if 'CZCE' in aSym or 'CFFEX' in aSym:
            adjustSym = splitSym[0] + '.' + splitSym[1].upper()
            return adjustSym
        if 'SHF' in aSym:
            adjustSym = splitSym[0] + 'E.' + splitSym[1].lower()
            return adjustSym
        if 'CZC' in aSym:
            adjustSym = splitSym[0] + 'E.' + splitSym[1].upper()
            return adjustSym


def reverseExchangeAndSecID(aSymbol):
    splitSym = aSymbol.split('.')
    return splitSym[1] + '.' + splitSym[0]


def adjustExchangeName(oldName):
    if oldName == '郑商所':
        return 'CZCE'
    if oldName == '大商所':
        return 'DCE'
    if oldName == '上期所':
        return 'SHFE'
    if oldName == '中金所':
        return 'CFFEX'
    if oldName == '能源中心':
        return 'INE'
    assert 2 == 1, 'strage exchangeName'


def symNameToSymID(symName):
    adict = {}
    adict.update(FUTURES_CN_SYMNAME_MAP_SYMID)
    adict.update(STOCKS_CN_SYMNAME_MAP_SYMID)
    return adict[symName]


def addExchange(aSymbol):
    instruments4CZCE = [
     'TA', 'SR', 'CF', 'OI', 'MA',
     'FG', 'RM', 'ZC', 'SF', 'SM', 'AP',
     'ER', 'RO', 'WS', 'ME', 'WH',
     'TC', 'WT', 'PM', 'RI', 'LR',
     'JR', 'CY', 'RS', 'GN']
    instruments4DCE = [
     'A', 'B', 'C', 'CS', 'I', 'J',
     'JD', 'JM', 'L', 'M', 'P',
     'PP', 'V', 'Y', 'FB', 'S',
     'EG']
    instruments4SHFE = [
     'AL', 'BU', 'CU', 'SN', 'ZN',
     'HC', 'NI', 'PB', 'RB', 'RU',
     'AG', 'AU', 'FU', 'WR']
    instruments4INE = [
     'SC']
    instruments4CFFEX = [
     'IC', 'IH', 'IF', 'T', 'TF']
    adjustSym = aSymbol.upper()
    fianSymbol = ''
    if adjustSym[0:2] in instruments4CZCE:
        if len(adjustSym[2:]) == 4:
            fianSymbol = 'CZCE.' + aSymbol[0:2].upper() + adjustSym[3:]
        else:
            fianSymbol = 'CZCE.' + aSymbol.upper()
    else:
        if adjustSym[0:2] in instruments4SHFE:
            fianSymbol = 'SHFE.' + aSymbol.lower()
        else:
            if adjustSym[0:2] in instruments4INE:
                fianSymbol = 'INE.' + aSymbol.lower()
            else:
                if adjustSym[0:2] in instruments4CFFEX:
                    fianSymbol = 'CFFEX.' + aSymbol.upper()
                else:
                    if adjustSym[0:1] in instruments4CFFEX:
                        fianSymbol = 'CFFEX.' + aSymbol.upper()
                    else:
                        if adjustSym[0:2] in instruments4DCE:
                            fianSymbol = 'DCE.' + aSymbol.lower()
                        else:
                            if adjustSym[0:1] in instruments4DCE:
                                fianSymbol = 'DCE.' + aSymbol.lower()
                            return fianSymbol


def removeExchange(aSymbol):
    adjSymbol = aSymbol.split('.')
    return adjSymbol[1]


def getOptionContractsBylw(sDateTime, eDateTime):
    engine = create_engine('mysql+pymysql://admin:admin@192.168.10.81:3306/option?charset=utf8', encoding='utf-8')
    optionSymbolsINfo = pd.read_sql('SELECT * FROM optionContractBasicInfo', engine)
    if sDateTime:
        if eDateTime:
            optionSymbolsINfo = optionSymbolsINfo[(~((optionSymbolsINfo['listed_date'] > eDateTime) | (optionSymbolsINfo['expire_date'] < sDateTime)))]
    return list(optionSymbolsINfo['wind_code'].values)


def contracts4wangzong():
    instruments4CZCE = [
     'CZCE.TA', 'CZCE.SR', 'CZCE.CF', 'CZCE.OI', 'CZCE.MA',
     'CZCE.FG', 'CZCE.RM', 'CZCE.ZC', 'CZCE.SF', 'CZCE.SM', 'CZCE.AP']
    instruments4DCE = [
     'DCE.A', 'DCE.B', 'DCE.C', 'DCE.CS', 'DCE.I', 'DCE.J',
     'DCE.JD', 'DCE.JM', 'DCE.L', 'DCE.M', 'DCE.P',
     'DCE.PP', 'DCE.V', 'DCE.Y']
    instruments4SHFE = [
     'SHFE.AL', 'SHFE.BU', 'SHFE.CU', 'SHFE.SN', 'SHFE.ZN',
     'SHFE.HC', 'SHFE.NI', 'SHFE.PB', 'SHFE.RB', 'SHFE.RU', 'SHFE.AG', 'SHFE.AU']
    instruments4INE = [
     'INE.SC']
    instruments4CFFEX = [
     'CFFEX.IC', 'CFFEX.IH', 'CFFEX.IF', 'CFFEX.T', 'CFFEX.TF']
    return instruments4CZCE + instruments4DCE + instruments4SHFE + instruments4INE + instruments4CFFEX


def getFullSymbolName(astrList):
    resuList = []
    cList = contracts4wangzong()
    for acStr in astrList:
        for aSy in cList:
            if acStr in aSy:
                resuList.append(aSy)
                break

    return resuList


def getMainContinContract(aSymbol):
    if aSymbol == np.nan:
        return np.nan
    noDigit = re.sub('\\d+', '', aSymbol)
    return noDigit.upper()


def runAQQ(who, msg):
    import win32gui, win32con, win32clipboard as w

    def getText():
        w.OpenClipboard()
        d = w.GetClipboardData(win32con.CF_UNICODETEXT)
        w.CloseClipboard()
        return d

    def setText(aString):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
        w.CloseClipboard()

    to_who1 = who
    content = '机器人信息:' + msg
    setText(content)
    qqhd = win32gui.FindWindow(None, to_who1)
    print(qqhd)
    win32gui.SendMessage(qqhd, 258, 22, 2080193)
    win32gui.SendMessage(qqhd, 770, 0, 0)
    win32gui.SendMessage(qqhd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qqhd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def btStartEndDates():
    import time, datetime
    currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    currDate = currDateTime[0:10]
    aSTimeStr = '08:00:00'
    aeTimeStr = '16:00:00'
    m1dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') + DateOffset(years=(-1), months=(-3))
    m1dtStr = m1dt.strftime('%Y-%m-%d')
    m2dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') + DateOffset(days=(-2))
    m2dtStr = m2dt.strftime('%Y-%m-%d')
    nextYearofToday = datetime.datetime.strptime(currDate, '%Y-%m-%d') + DateOffset(years=1)
    nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
    aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
    aNewTradeCalendar = calendayBylw.customTradeCalendar(aTradingDays)
    backTestsDateT = aNewTradeCalendar.mDatesOffset(m1dtStr, yoffset=0) + ' ' + aSTimeStr
    backTesteDateT = aNewTradeCalendar.mDatesOffset(m2dtStr, yoffset=0) + ' ' + aeTimeStr
    maxLen = 60
    barsNum = 3


def updateMFE(aOrderMFEdict, basicBar_):
    if not aOrderMFEdict is not None:
        raise AssertionError
    else:
        assert basicBar_ is not None
        posi = aOrderMFEdict['orderPosition']
        if posi.barsSinceEntry > 0:
            if posi.barsSinceEntry == 1:
                aOrderMFEdict['HH'] = basicBar_.getHigh()
                aOrderMFEdict['LL'] = basicBar_.getLow()
            else:
                aOrderMFEdict['HH'] = max(aOrderMFEdict['HH'], basicBar_.getHigh())
                aOrderMFEdict['LL'] = min(aOrderMFEdict['LL'], basicBar_.getLow())
            if posi.positionSide == 'long':
                aOrderMFEdict['MFE'] = aOrderMFEdict['HH'] - posi.cost
            if posi.positionSide == 'short':
                aOrderMFEdict['MFE'] = posi.cost - aOrderMFEdict['LL']


def copyFiles2(sourceDir, targetDir, filename=None):
    import os, shutil
    if sourceDir.find('exceptionfolder') > 0:
        return
    elif filename:
        sourceFile = os.path.join(sourceDir, filename)
        targetFile = os.path.join(targetDir, filename)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if os.path.exists(targetFile):
                if not os.path.exists(targetFile) or os.path.getsize(targetFile) != os.path.getsize(sourceFile):
                    open(targetFile, 'wb').write(open(sourceFile, 'rb').read())
                    print(targetFile + ' copy succeeded')
        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)
    else:
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir, file)
            targetFile = os.path.join(targetDir, file)
            if os.path.isfile(sourceFile):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                if not os.path.exists(targetFile) or os.path.exists(targetFile) and os.path.getsize(targetFile) != os.path.getsize(sourceFile):
                    open(targetFile, 'wb').write(open(sourceFile, 'rb').read())
                    print(targetFile + ' copy succeeded')
                if os.path.isdir(sourceFile):
                    copyFiles(sourceFile, targetFile)


def cusCopyFile(sourceDir, targetDir, filename=None):
    import os, shutil
    ss = os.path.dirname(sourceDir)
    abDir = os.path.abspath(sourceDir)
    if filename:
        sourceFile = os.path.join(abDir, filename)
        os.system('copy %s %s' % (sourceFile, targetDir))
    else:
        for file in os.listdir(sourceDir):
            abDirFile = os.path.join(abDir, file)
            if os.path.isfile(abDirFile):
                os.system('copy %s %s' % (abDirFile, targetDir))


def writeLog2console(logInstance='aLogger', msg=None):
    import logging
    loggerCons = logging.getLogger(logInstance)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    loggerCons.addHandler(console_handler)
    loggerCons.setLevel(logging.INFO)
    loggerCons.info(msg)


def writeLog2File(logInstance='aLogger', logfile=None, msg=None):
    import logging
    logger = logging.getLogger(logInstance)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler(logfile, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.info(msg)


def splitDates(sDateTime, eDateTime, step_=3000, moreDataFlag=False):
    from gm.api import get_trading_dates
    import time, datetime
    from pandas.tseries.offsets import DateOffset
    currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    currDate = currDateTime[0:10]
    nextYearofToday = datetime.datetime.strptime(currDate, '%Y-%m-%d') + DateOffset(years=1)
    nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
    aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
    aNewTradeCalendar = calendayBylw.customTradeCalendar(aTradingDays)
    sDate = sDateTime[0:10]
    eDate = eDateTime[0:10]
    if moreDataFlag:
        ssDate = aNewTradeCalendar.mDatesOffset(sDate, doffset=(-1), leftOrright=(-1))
        eeDate = aNewTradeCalendar.mDatesOffset(eDate, doffset=1, leftOrright=1)
    else:
        ssDate = aNewTradeCalendar.mDatesOffset(sDate, doffset=0, leftOrright=1)
        eeDate = aNewTradeCalendar.mDatesOffset(eDate, doffset=0, leftOrright=(-1))
    atradeDateSerial = aNewTradeCalendar.getADateTimeSeries(ssDate, eeDate)
    datesList = []
    sIndex = 0
    eIndex = sIndex + step_ - 1
    while True:
        cSdate = atradeDateSerial.iloc[sIndex]
        if eIndex >= atradeDateSerial.shape[0]:
            cEdate = atradeDateSerial.iloc[(-1)]
        else:
            cEdate = atradeDateSerial.iloc[eIndex]
        datesList.append((cSdate, cEdate))
        if eIndex >= atradeDateSerial.shape[0]:
            break
        else:
            sIndex = sIndex + step_
            eIndex = eIndex + step_

    atuple = datesList[0]
    datesList[0] = (atuple[0] + sDateTime[10:], atuple[1])
    atuple = datesList[(-1)]
    datesList[-1] = (atuple[0], atuple[1] + eDateTime[10:])
    return datesList


def dtToUnixTimeStamp(adt):
    ats = int(adt.timestamp() * 1000)
    return ats


def round_up(value, y):
    import math
    ss = math.pow(10, y)
    vs = round(value * ss) / float(ss)
    return vs


def isCrossDay(symbol, lastDT, currDT):
    lastDate = lastDT[0:10]
    currDate = currDT[0:10]
    lastTime = lastDT[11:]
    nowTime = currDT[11:]
    if lastDate == currDate:
        if lastTime <= FUTURES_CN_Day_ENDTIME:
            if nowTime >= FUTURES_CN_Day_STARTTIME_N001:
                return True
    if lastDate < currDate:
        if lastTime <= FUTURES_CN_Day_ENDTIME:
            if nowTime >= FUTURES_CN_Day_STARTTIME_N002:
                return True
    return False


def readLastLine(filename, encoding='gbk'):
    with open(filename, 'rb') as (hisRecordFile):
        import os
        first = hisRecordFile.readline()
        nextbyte = hisRecordFile.read(1)
        if nextbyte == b'':
            last = first
        else:
            hisRecordFile.seek(-2, os.SEEK_END)
            while nextbyte != b'\n':
                hisRecordFile.seek(-2, os.SEEK_CUR)
                nextbyte = hisRecordFile.read(1)

            last = hisRecordFile.readline()
        lastStr = last.decode(encoding)
        return lastStr.strip('\r\n')


def rangeLeftAndRight(avalue, step, stepCount):
    aList = []
    for i in range(1, stepCount + 1):
        aList.append(avalue - i * step)
        aList.append(avalue + i * step)

    aList.append(avalue)
    return sorted(aList)


import os

def mkdir(path):
    path = path.strip()
    path = path.rstrip('\\')
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)