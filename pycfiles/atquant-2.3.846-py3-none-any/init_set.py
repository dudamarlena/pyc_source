# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\api\init_set.py
# Compiled at: 2018-08-27 20:45:24
# Size of source mod 2**32: 115837 bytes
import os, sys, traceback
from numbers import Number
sys.path.append('..')
from atexit import register
from collections import Iterable
import numpy as np, pandas as pd, atquant.socket_ctrl.tool_box_command as tb_command
from atquant.utils.internal_util import load_mat
import atquant.utils.internal_util as UTILS_UTIL, atquant.utils.datetime_func as UTILS_DT, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR
from atquant.data.const_data import GACV
from atquant.utils.logger import write_syslog, write_userlog
from atquant.utils.internal_exception import ToolBoxErrors
from atquant.utils.arg_checker import verify_that, apply_rule
from atquant.data.const_data import atStringToConst
from atquant.utils.user_class import dotdict
from atquant.utils.arg_checker import ArgumnetChecker
from atquant.data.const_data import atDefineConst
import atquant.at_algorithm.core_algorithm as CORE_ALGO

@register
def exit_clean():
    try:
        try:
            GVAR.g_ATraderSID.disconnect_from_at()
            GVAR.g_ATraderSIDCB.disconnect_from_at()
        except Exception:
            write_syslog(traceback.format_exc(), level='info')

    finally:
        write_syslog('Python interpreter exit!', level='info')


def atCheckIdx(FuncName, HandleIdx, TargetIdx, toarray=True):
    HandleIdx_nd, TargetIdx_nd = (None, None)
    if HandleIdx is not None:
        if isinstance(HandleIdx, (int, float)) and not np.isnan(HandleIdx):
            HandleIdx = int(HandleIdx)
        HandleIdx_nd = np.asarray([HandleIdx], dtype=np.int).ravel()
        ArgumnetChecker.check_ndarray_idx(FuncName, 'HandleIdx', (HandleIdx_nd, 0, GVAR.atHandleIdxCount()), allow_nan=False)
    if TargetIdx is not None:
        if isinstance(TargetIdx, (int, float)) and not np.isnan(TargetIdx):
            TargetIdx = int(TargetIdx)
        TargetIdx_nd = np.asarray([TargetIdx], dtype=np.int).ravel()
        ArgumnetChecker.check_ndarray_idx(FuncName, 'TargetIdx', (TargetIdx_nd, 0, GVAR.atTargetIdxCount()), allow_nan=False)
    if toarray:
        return (HandleIdx_nd if HandleIdx_nd is not None else HandleIdx, TargetIdx_nd if TargetIdx_nd is not None else TargetIdx)
    else:
        return (
         HandleIdx, TargetIdx)


def atSetRealTradeSaveFreshPositionInAppend(atraderSimBaseDatas, arrayTime):
    for kdata in atraderSimBaseDatas:
        if len(kdata['Time']) > 0:
            _t = np.argwhere(kdata['Time'][(-1)] == arrayTime).ravel()
            if np.isnan(GVAR.g_ATraderRealTradeSaveFreshPositionInAppend):
                if len(_t) > 0:
                    GVAR.g_ATraderRealTradeSaveFreshPositionInAppend = _t[0]
                else:
                    if len(_t) > 0 and GVAR.g_ATraderRealTradeSaveFreshPositionInAppend < _t[0]:
                        GVAR.g_ATraderRealTradeSaveFreshPositionInAppend = _t[0]

    if np.isnan(GVAR.g_ATraderRealTradeSaveFreshPositionInAppend):
        GVAR.g_ATraderRealTradeSaveFreshPositionInAppend = 0


def atGetKDataMulti(TargetsList, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ, AccHandle, StrategyName):
    """获取行情数据的接口函数，通过调用LoadFromPro，LoadFromLocal函数获取行情数据"""
    result = LoadFromPro(TargetsList, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ, AccHandle, StrategyName)
    if result.errorFlag:
        raise Exception(result.errormsg)
    KArray = LoadFromLocal(result.matFile, TargetsList, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ, AccHandle, StrategyName)
    for i in range(len(KArray)):
        if 'Time' not in KArray[i] or KArray[i].Time.size < 1:
            KArray[i].Time = np.array([])
            KArray[i].Open = np.array([])
            KArray[i].High = np.array([])
            KArray[i].Low = np.array([])
            KArray[i].Close = np.array([])
            KArray[i].Volume = np.array([])
            KArray[i].TurnOver = np.array([])
            KArray[i].OpenInterest = np.array([])
            KArray[i].BeginBar = np.array([])
        else:
            after_unique_time, after_unique_index = np.unique(KArray[i].Time, return_index=True)
            if len(after_unique_time) != len(KArray[i].Time):
                KArray[i].Time = KArray[i].Time[after_unique_index]
                KArray[i].Open = KArray[i].Open[after_unique_index]
                KArray[i].High = KArray[i].High[after_unique_index]
                KArray[i].Low = KArray[i].Low[after_unique_index]
                KArray[i].Close = KArray[i].Close[after_unique_index]
                KArray[i].Volume = KArray[i].Volume[after_unique_index]
                KArray[i].TurnOver = KArray[i].TurnOver[after_unique_index]
                KArray[i].OpenInterest = KArray[i].OpenInterest[after_unique_index]
                KArray[i].BeginBar = KArray[i].BeginBar[after_unique_index]

    tb_command.atClearMatFileIncludeCurTradeDate(result.matFile, EndDate)
    return KArray


def LoadFromLocal(matFile, TargetsList, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ, AccHandle, StrategyName):
    """从本地mat文件中读取行情数据"""
    results = []
    for j in range(len(TargetsList)):
        results.append(dotdict({filed:np.array([]) for filed in [
         'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'TurnOver', 'OpenInterest',
         'BeginBar']}))
        results[j]['Market'] = TargetsList[j]['Market']
        results[j]['Code'] = TargetsList[j]['Code']

    if not matFile or os.path.exists(matFile) and not os.path.getsize(matFile):
        pass
    else:
        ntimes = 0
        KArray = np.array([])
        while ntimes < 3:
            flag = False
            try:
                mat_content = UTILS_UTIL.load_mat(matFile)
                if 'KArray' in mat_content:
                    KArray = mat_content['KArray']
                if KArray.size < 1:
                    flag = True
                else:
                    break
            except Exception:
                flag = True

            if flag:
                UTILS_UTIL.run_ignore_exception(os.remove, matFile)
                _result = LoadFromPro(TargetsList, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ, AccHandle, StrategyName)
                matFile = _result.matFile
            ntimes += 1

        if len(KArray.shape) == 2 and KArray.shape[1] == len(TargetsList):
            results.clear()
            for j in range(len(TargetsList)):
                results.append(dotdict({filed:KArray[filed][(0, j)].ravel() for filed in KArray[(0,
                                                                                                 0)].dtype.names}))
                results[j]['Market'] = TargetsList[j]['Market']
                results[j]['Code'] = TargetsList[j]['Code']

        else:
            write_syslog('{!r} length not match mat data shape, {}'.format(TargetsList, const_da.Enum_Const.ERROR_NOTCOMPLTE_DATA.value))
    return results


def LoadFromPro(TargetsList, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ, AccHandle, StrategyName):

    def log(handle, strategename, BeginDate, EndDate, KFrequency, KFreNum, Code, Market):
        traderPutLog(handle, strategename, 'Begin preparing data [%d--%d][%s_%d][%s.%s]...' % (
         BeginDate, EndDate, KFrequency, KFreNum, Code, Market))
        write_syslog('获取历史K线数据[%d--%d][%s_%d][%s.%s]...' % (BeginDate, EndDate, KFrequency, KFreNum, Code, Market), level='info')

    _result = dotdict({'errorFlag': 0, 
     'errormsg': '', 
     'matFile': None})
    KFrequency = KFrequency.lower()
    if KFrequency == 'tick':
        Middle = ''.join(['<item Market="%s" Code="%s"/>' % (item['Market'], item['Code']) for item in TargetsList])
        fileName = '%d.mat' % UTILS_UTIL.hashmd5_to_int('%s_%d_%d_%s_%d_%d_%s' % (Middle, BeginDate, EndDate, KFrequency, 1, FilledUp, FQ))
        matFile = os.path.join(GVAR.root_sub_dir('mat'), fileName)
        tb_command.atClearMatFileIncludeCurTradeDate(matFile, EndDate)
        KArray = []
        for target in TargetsList:
            target = dotdict(target)
            log(AccHandle[0], StrategyName, BeginDate, EndDate, KFrequency, KFreNum, target.Code, target.Market)
            info = atGetTickDataPeriod(target.Market, target.Code, BeginDate, EndDate, FQ)
            _t = dotdict({'Time': info.Time, 
             'Open': info.Price, 
             'High': info.Price, 
             'Low': info.Price, 
             'Close': info.Price, 
             'Volume': info.VolumeTick, 
             'TurnOver': info.TurnOver, 
             'OpenInterest': info.OpenInterest, 
             'BeginBar': info.BeginBar})
            KArray.append(_t)

        if len(KArray) > 0:
            if not os.path.exists(GVAR.root_sub_dir('mat')):
                UTILS_UTIL.run_ignore_exception(os.mkdir, GVAR.root_sub_dir('mat'))
            UTILS_UTIL.save_mat(matFile, KArray, struct_name='KArray', oned_as='row')
    else:
        for target in TargetsList:
            target = dotdict(target)
            log(AccHandle[0], StrategyName, BeginDate, EndDate, KFrequency, KFreNum, target.Code, target.Market)
            GVAR.g_ATraderGetKData_NoReturn = True
            traderGetKData(target.Market, target.Code, KFrequency, 1, BeginDate, EndDate, True, FQ)
            GVAR.g_ATraderGetKData_NoReturn = False

        matFile = tb_command.at_send_ATraderGetKDataMulti(TargetsList, BeginDate, EndDate, KFrequency, KFreNum, FilledUp, FQ)
    _result.matFile = matFile
    return _result


def atLoadKDataFromPro(Market, Code, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ):
    """
    从 at 获取频率 'sec' 及其以上的数据，并返回词典序列
    
    rule1 若 KFrequency 为 'sec'  则先获取 'tick' 数据
    rule2 若 KFrequency 为 'week','month', 'year' 则通过 AT 获取 'day' 数据
    rule3 通过 atKDataExtraction 提取数据
    """

    def IsKDataExist(Market, Code, KFrequency, BeginDate, EndDate, FilledUp, FQ):
        KFrequency = KFrequency.lower()
        if KFrequency in ('min', 'day'):
            KFrequency = KFrequency + 'K'
        _t = 'py_{KFrequency}_{Market}_{Code}_{BeginDate}_{EndDate}_{FilledUp}_{FQ}.mat'.format(KFrequency=KFrequency, Market=Market, Code=Code, BeginDate=BeginDate, EndDate=EndDate, FilledUp=FilledUp, FQ=FQ)
        fileLoc = os.path.join(GVAR.root_sub_dir('mat'), _t)
        if not os.path.exists(fileLoc):
            fileLoc = None
        return fileLoc

    info = dotdict({'Time': np.array([]), 
     'Open': np.array([]), 
     'High': np.array([]), 
     'Low': np.array([]), 
     'Close': np.array([]), 
     'Volume': np.array([]), 
     'TurnOver': np.array([]), 
     'OpenInterest': np.array([]), 
     'BeginBar': np.array([])})
    KFrequency = KFrequency.lower()
    oldKFrequency = 'sec' if KFrequency == 'sec' else 'min'
    if KFrequency in ('week', 'month', 'year'):
        oldKFrequency, KFrequency = KFrequency, 'day'
    NoReturn = True if GVAR.g_ATraderGetKData_NoReturn else False
    if KFrequency != 'sec':
        matFile = tb_command.at_send_AtraderGetKData(BeginDate, EndDate, Market, Code, KFrequency, FilledUp, FQ, NoReturn)
        if not matFile:
            return info
            try:
                mat_content = dotdict(UTILS_UTIL.load_mat(matFile))
            except Exception:
                UTILS_UTIL.run_ignore_exception(os.remove, matFile)
                raise ToolBoxErrors.data_download_error(traceback.format_exc() + const_da.Enum_Const.ERROR_DOWNLOAD_DATA.value)

            if 'Time' not in mat_content or 'Time' in mat_content and mat_content.Time.size < 1:
                UTILS_UTIL.run_ignore_exception(os.remove, matFile)
                write_syslog('fail to find Time in the return data of AtraderGetKData', level='warn')
                return info
            tb_command.atClearMatFileIncludeCurTradeDate(matFile, EndDate)
            Time = mat_content.Time
            Open = mat_content.Open
            High = mat_content.High
            Low = mat_content.Low
            Close = mat_content.Close
            Volume = mat_content.Volume
            TurnOver = mat_content.TurnOver
            OpenInterest = mat_content.OpenInterest
            BeginBar = mat_content.BeginBar
    else:
        ToolBoxErrors.not_support_error('Not suport "sec" of KFrequency')
    KFrequency = oldKFrequency if oldKFrequency not in ('min', 'day') else KFrequency
    info = atKDataExtraction(Time, Open, High, Low, Close, Volume, TurnOver, OpenInterest, BeginBar, KFrequency, KFrequency, KFreNum)
    _, indices = np.unique(info.Time, return_index=True)
    uniquetime = info.Time[np.sort(indices)]
    _, tmIdx = CORE_ALGO.ismember(uniquetime, info.Time)
    info.Time = info.Time[tmIdx]
    info.Open = info.Open[tmIdx]
    info.High = info.High[tmIdx]
    info.Low = info.Low[tmIdx]
    info.Close = info.Close[tmIdx]
    info.Volume = info.Volume[tmIdx]
    info.TurnOver = info.TurnOver[tmIdx]
    info.OpenInterest = info.OpenInterest[tmIdx]
    info.BeginBar = info.BeginBar[tmIdx]
    return info


def atKDataExtraction(Time, Open, High, Low, Close, Volume, TurnOver, OpenInterest, BeginBar, BaseKFre, KFrequency, KFreNum):
    info = dotdict({'Time': np.array([]), 
     'Open': np.array([]), 
     'High': np.array([]), 
     'Low': np.array([]), 
     'Close': np.array([]), 
     'Volume': np.array([]), 
     'TurnOver': np.array([]), 
     'OpenInterest': np.array([]), 
     'BeginBar': np.array([])})

    def deal_sec_min():
        nonlocal BeginBar
        nonlocal Close
        nonlocal High
        nonlocal Low
        nonlocal Open
        nonlocal OpenInterest
        nonlocal Time
        nonlocal TurnOver
        nonlocal Volume
        BeginBarPoints = np.where(BeginBar > 0)[0]
        if BeginBarPoints.size < 1:
            return info
        if 0 != BeginBarPoints[0]:
            Time = Time[BeginBarPoints[0]:]
            Volume = Volume[BeginBarPoints[0]:]
            Open = Open[BeginBarPoints[0]:]
            High = High[BeginBarPoints[0]:]
            Low = Low[BeginBarPoints[0]:]
            Close = Close[BeginBarPoints[0]:]
            TurnOver = TurnOver[BeginBarPoints[0]:]
            OpenInterest = OpenInterest[BeginBarPoints[0]:]
            BeginBar = BeginBar[BeginBarPoints[0]:]
            BeginBarPoints = np.where(BeginBar > 0)[0]
        iszeroVol, _ = CORE_ALGO.ismember(Volume, np.array([0]))
        Open[iszeroVol] = 0
        High[iszeroVol] = 0
        Low[iszeroVol] = 0
        del iszeroVol
        if 1 == BeginBarPoints.size:
            endBarPoints = np.array([BeginBarPoints.size])
        else:
            endBarPoints = np.append(BeginBarPoints[1:] - 1, np.array([BeginBar.size - 1]), axis=0)
        otherminpoints = np.array([])
        returnBarPoints = np.array([], dtype=np.int)
        for v1, v2 in zip(BeginBarPoints, endBarPoints):
            tmpotherminpoints = np.concatenate((np.arange(v1, v2 + 1, KFreNum), np.array([v2 + 0.1])))
            returnBarPoints = np.concatenate((
             returnBarPoints, np.arange(v1, v2 + 1, KFreNum) - 1, np.array([v2]))).astype(np.int)
            otherminpoints = np.concatenate((otherminpoints, tmpotherminpoints))

        SubTimes = np.digitize(np.arange(Time.size), np.concatenate((otherminpoints, [np.inf]))) - 1
        returnBarNums = otherminpoints.size - 1
        nvolume = CORE_ALGO.accumarray(SubTimes, Volume, (returnBarNums, 1), np.sum)
        info.Volume = nvolume[(~np.isnan(nvolume))]
        nopen = CORE_ALGO.accumarray(SubTimes, Open, (returnBarNums, 1), lambda x: x[0])
        nopen = nopen[(~np.isnan(nopen))]
        nhigh = CORE_ALGO.accumarray(SubTimes, High, (returnBarNums, 1), np.max)
        nhigh = nhigh[(~np.isnan(nhigh))]
        nlow = CORE_ALGO.accumarray(SubTimes, Low, (returnBarNums, 1), np.min)
        nlow = nlow[(~np.isnan(nlow))]
        nclose = CORE_ALGO.accumarray(SubTimes, Close, (returnBarNums, 1), lambda x: x[(-1)])
        nclose = nclose[(~np.isnan(nclose))]
        nturnover = CORE_ALGO.accumarray(SubTimes, TurnOver, (returnBarNums, 1), np.sum)
        info.TurnOver = nturnover[(~np.isnan(nturnover))]
        nopeninterest = CORE_ALGO.accumarray(SubTimes, OpenInterest, (returnBarNums, 1), lambda x: x[(-1)])
        info.OpenInterest = nopeninterest[(~np.isnan(nopeninterest))]
        LoopIdx = np.where(0 == nclose)[0]
        if len(LoopIdx) > 1:
            nclose[LoopIdx] = nclose[(LoopIdx - 1)]
        info.Close = nclose
        LoopIdx = np.where(nopen == 0)[0]
        if len(LoopIdx) > 1:
            nopen[LoopIdx] = nclose[(LoopIdx - 1)]
        if len(LoopIdx) > 0 and LoopIdx[0] == 0:
            nopen[0] = nclose[0]
        info.Open = nopen
        LoopIdx = np.where(nhigh == 0)[0]
        if len(LoopIdx) > 1:
            nhigh[LoopIdx] = nclose[(LoopIdx - 1)]
        if len(LoopIdx) > 0 and LoopIdx[0] == 0:
            nhigh[0] = nclose[0]
        info.High = nhigh
        LoopIdx = np.where(nlow == 0)[0]
        if len(LoopIdx) > 1:
            nlow[LoopIdx] = nclose[(LoopIdx - 1)]
        if len(LoopIdx) > 0 and LoopIdx[0] == 0:
            nlow[0] = nclose[0]
        info.Low = nlow
        returnBarPoints = returnBarPoints[(returnBarPoints >= 0)]
        _, indices = np.unique(returnBarPoints, return_index=True)
        returnBarPoints = returnBarPoints[np.sort(indices)]
        info.Time = Time[returnBarPoints]
        info.BeginBar = BeginBar[returnBarPoints]
        return info

    def deal_day():
        MinBeginBarNum = np.where(BeginBar == 1)[0]
        daynum = np.sum(BeginBar)
        info.Time = np.ones((daynum, 1))
        info.Open = np.ones((daynum, 1))
        info.Close = np.ones((daynum, 1))
        info.OpenInterest = np.ones((daynum, 1))
        info.High = np.ones((daynum, 1))
        info.Low = np.ones((daynum, 1))
        info.Volume = np.ones((daynum, 1))
        info.TurnOver = np.ones((daynum, 1))
        info.BeginBar = np.ones((daynum, 1))
        for i in range(daynum):
            DayB = MinBeginBarNum[i]
            if daynum == 1:
                DayE = len(Time)
            else:
                DayE = MinBeginBarNum[(i + 1)]
            info.Time[i] = Time[(DayE - 1)]
            info.Open[i] = Open[DayB]
            info.Close[i] = Close[(DayE - 1)]
            info.OpenInterest[i] = OpenInterest[(DayE - 1)]
            info.High[i] = np.max(High[DayB:DayE])
            info.Low[i] = np.min(Low[DayB:DayE])
            info.Volume[i] = np.sum(Volume[DayB:DayE])
            info.TurnOver[i] = np.sum(TurnOver[DayB:DayE])
            info.BeginBar[i] = 1

    if Time.size < 1:
        return info
    if BaseKFre == KFrequency and KFreNum == 1:
        info.Time = Time
        info.Open = Open
        info.Close = Close
        info.OpenInterest = OpenInterest
        info.High = High
        info.Low = Low
        info.Volume = Volume
        info.TurnOver = TurnOver
        info.BeginBar = BeginBar
        return info
    if BaseKFre == 'sec':
        if KFrequency == 'sec':
            return deal_sec_min()
        if KFrequency == 'day':
            return deal_day()
    else:
        if BaseKFre == 'min':
            if KFrequency == 'min':
                return deal_sec_min()
            if KFrequency == 'day':
                return deal_day()
        elif BaseKFre == 'day':
            if BeginBar.size < 1:
                return info
            returnBarPoints = np.concatenate((np.arange(KFreNum, len(BeginBar), KFreNum), np.array([len(BeginBar)])))
            _, indices = np.unique(returnBarPoints, return_index=True)
            returnBarPoints = returnBarPoints[np.sort(indices)]
            info.Time = Time[returnBarPoints]
            info.Open = Open[returnBarPoints]
            info.Close = Close[returnBarPoints]
            info.OpenInterest = OpenInterest[returnBarPoints]
            info.High = High[returnBarPoints]
            info.Low = Low[returnBarPoints]
            info.Volume = Volume[returnBarPoints]
            info.TurnOver = TurnOver[returnBarPoints]
            info.BeginBar = BeginBar[returnBarPoints]
    return info


def atGetTickDataPeriod(Market, Code, BeginDate, EndDate, FQ):
    totalLen = 0
    Days = traderGetTradingDays(BeginDate, EndDate)
    TickSingles = [dotdict({}) for j in range(len(Days))]
    for j, day in enumerate(Days):
        info = tb_command.atLoadTickDataFromPro(Market, Code, day, FQ)
        info.BeginBar = np.zeros((len(info.Time), 1))
        TickSingles[j] = info
        totalLen += len(info.Time)

    info = dotdict({'Time': np.zeros((totalLen, 1)), 
     'Price': np.zeros((totalLen, 1)), 
     'Volume': np.zeros((totalLen, 1)), 
     'VolumeTick': np.zeros((totalLen, 1)), 
     'TurnOver': np.zeros((totalLen, 1)), 
     'OpenInterest': np.zeros((totalLen, 1)), 
     'BidPrice': np.zeros((totalLen, 5)), 
     'BidVolume': np.zeros((totalLen, 5)), 
     'AskPrice': np.zeros((totalLen, 5)), 
     'AskVolume': np.zeros((totalLen, 5)), 
     'BeginBar': np.zeros((totalLen, 1))})
    sPosB = 0
    for item in TickSingles:
        sPosE = sPosB + len(item.Time)
        if sPosE >= sPosB:
            info.Time[sPosB:sPosE, :] = item.Time
            info.Price[sPosB:sPosE, :] = item.Price
            info.Volume[sPosB:sPosE, :] = item.Volume
            info.VolumeTick[sPosB:sPosE, :] = item.VolumeTick
            info.TurnOver[sPosB:sPosE, :] = item.TurnOver
            info.OpenInterest[sPosB:sPosE, :] = item.OpenInterest
            info.BidPrice[sPosB:sPosE, :] = item.BidPrice[:]
            info.BidVolume[sPosB:sPosE, :] = item.BidVolume[:]
            info.AskPrice[sPosB:sPosE, :] = item.AskPrice[:]
            info.AskVolume[sPosB:sPosE, :] = item.AskVolume[:]
            info.BeginBar[sPosB:sPosE, :] = item.BeginBar
        sPosB = sPosE

    return info


def atBornSecData(tickdata, secbartime):
    """通过tick数据合成1秒钟频率数据"""
    _, indices = np.unique(secbartime, return_index=True)
    secbartime = secbartime[np.sort(indices)]
    Idx = np.digitize(tickdata[:, 0], np.append([1], secbartime)) - 1
    tmplogic = np.greater_equal(Idx, 0)
    Idx = Idx[tmplogic]
    tickdata = tickdata[tmplogic, :]
    returnBarNums = len(secbartime)
    nopen = CORE_ALGO.accumarray(Idx, tickdata[:, 1], (returnBarNums, 1), lambda x: x[0])
    nhigh = CORE_ALGO.accumarray(Idx, tickdata[:, 1], (returnBarNums, 1), np.max)
    nlow = CORE_ALGO.accumarray(Idx, tickdata[:, 1], (returnBarNums, 1), np.min)
    nclose = CORE_ALGO.accumarray(Idx, tickdata[:, 1], (returnBarNums, 1), lambda x: x[(-1)])
    nvolume = CORE_ALGO.accumarray(Idx, tickdata[:, 2], (returnBarNums, 1), np.sum)
    nturnover = CORE_ALGO.accumarray(Idx, tickdata[:, 3], (returnBarNums, 1), np.sum)
    nopeninterest = CORE_ALGO.accumarray(Idx, tickdata[:, 4], (returnBarNums, 1), lambda x: x[(-1)])
    tmpIdx = np.where(nclose > 0)[0]
    tmpIdx = tmpIdx[0] if tmpIdx.size > 0 else 0
    LoopIdx = np.where(0 == nclose)[0]
    if len(LoopIdx) > 1:
        nclose[LoopIdx] = nclose[(LoopIdx - 1)]
    if len(LoopIdx) > 0 and LoopIdx[0] == 0:
        nclose[0] = nclose[tmpIdx]
    LoopIdx = np.where(nopen == 0)[0]
    if len(LoopIdx) > 1:
        nopen[LoopIdx] = nclose[(LoopIdx - 1)]
    if len(LoopIdx) > 0 and LoopIdx[0] == 0:
        nopen[0] = nclose[0]
    LoopIdx = np.where(nhigh == 0)[0]
    if len(LoopIdx) > 1:
        nhigh[LoopIdx] = nclose[(LoopIdx - 1)]
    if len(LoopIdx) > 0 and LoopIdx[0] == 0:
        nhigh[0] = nclose[0]
    LoopIdx = np.where(nlow == 0)[0]
    if len(LoopIdx) > 1:
        nlow[LoopIdx] = nclose[(LoopIdx - 1)]
    if len(LoopIdx) > 0 and LoopIdx[0] == 0:
        nlow[0] = nclose[0]
    LoopIdx = np.where(nopeninterest == 0)[0]
    if len(LoopIdx) > 1:
        _t = nopeninterest[0]
        nopeninterest[LoopIdx] = nopeninterest[(LoopIdx - 1)]
        nopeninterest[0] = _t
    info = dotdict({'Open': nopen, 
     'High': nhigh, 
     'Low': nlow, 
     'Close': nclose, 
     'Volume': nvolume, 
     'TurnOver': nturnover, 
     'OpenInterest': nopeninterest})
    tmparrayTime = secbartime.copy()
    alltraderDay = np.unique(np.floor(secbartime))
    TraderDateEndPoint = 0.666666666666667
    allendTimePoint = alltraderDay + 0.625
    tflag, _ = CORE_ALGO.ismember(secbartime, allendTimePoint)
    realTraderDate = np.unique(np.floor(secbartime[tflag]))
    insertTimePoint = (realTraderDate + TraderDateEndPoint).reshape((-1, 1))
    secbartime = np.union1d(secbartime, insertTimePoint)
    beginbar = np.zeros((len(secbartime), 1))
    _, Idx = CORE_ALGO.ismember(insertTimePoint, secbartime)
    Idx = Idx[:-1]
    Idx = np.append([0], Idx + 1, axis=0)
    beginbar[Idx] = 1
    tmflag, _ = CORE_ALGO.ismember(secbartime, tmparrayTime)
    beginbar = beginbar[tmflag]
    info.BeginBar = beginbar
    info.Time = tmparrayTime
    return info


def atInitTargetInfo(Costfee):
    GVAR.g_ATraderFutureInfoMapV2 = pd.DataFrame([])
    for target in GVAR.g_ATraderStraInputInfo.TargetList:
        info = traderGetTargetInfo(target['Market'], target['Code'])
        GVAR.g_ATraderFutureInfoMapV2[GVAR.g_ATraderFutureInfoMapV2.shape[1]] = pd.Series(info)

    if not np.isnan(Costfee):
        for column in GVAR.g_ATraderFutureInfoMapV2.columns:
            GVAR.g_ATraderFutureInfoMapV2.loc[('TradingFeeOpen', column)] = Costfee
            GVAR.g_ATraderFutureInfoMapV2.loc[('TradingFeeOpen', column)] = Costfee
            GVAR.g_ATraderFutureInfoMapV2.loc[('TradingFeeClose', column)] = Costfee
            GVAR.g_ATraderFutureInfoMapV2.loc[('TradingFeeCloseToday', column)] = Costfee


def FindOrFillBaseKMatrix(iFreq):
    """
    查找或者填充基础频率矩阵【与用户要求频率一致的KFreNum为1的矩阵】，如果已有基础数据则直接返回，
    否则递归的找到最相近的基础频率矩阵，然后进行合成，最终返回【与用户要求频率一致的KFreNum为1的矩阵】

    :param iFreq: 频率,整型
    :return: 矩阵在 g_ATraderKDatas 中的索引
    """
    targets = GVAR.g_ATraderStraInputInfo.TargetList
    begindate = GVAR.g_ATraderStraInputInfo.BeginDate
    enddate = GVAR.g_ATraderStraInputInfo.EndDate
    higherFreqBase = -1
    if iFreq == 0:
        raise ValueError(const_da.Enum_Const.ERROR_INVALID_HIGHDATA.value)
    if GACV.KFreq_Sec <= iFreq <= GACV.KFreq_Day:
        iBaseFreq = iFreq - 1
    else:
        if iFreq in [GACV.KFreq_Week, GACV.KFreq_Month, GACV.KFreq_Year]:
            iBaseFreq = GACV.KFreq_Day
        else:
            raise ValueError(const_da.Enum_Const.ERROR_INPUT_FREQUENCY.value)
    for i in range(len(GVAR.g_ATraderKDatas)):
        if GVAR.g_ATraderKDatas[i]['iFreq'] == iFreq and GVAR.g_ATraderKDatas[i]['FreqNum'] == 1:
            return i
        if GVAR.g_ATraderKDatas[i]['iFreq'] == iBaseFreq and GVAR.g_ATraderKDatas[i]['FreqNum'] == 1:
            higherFreqBase = i

    if higherFreqBase == -1:
        higherFreqBase = FindOrFillBaseKMatrix(iBaseFreq)
    arrayTime, dayPos = traderGetTradingTime(targets, iFreq, begindate, enddate)
    if len(arrayTime) == 0:
        raise ValueError(const_da.Enum_Const.ERROR_EMPTY_TIMELINE.value)
    bP = np.zeros((len(arrayTime),), dtype=np.int)
    eP = np.zeros((len(arrayTime),), dtype=np.int)
    _Matrix = GVAR.generate_base_ndarray(len(targets), len(arrayTime))
    _Matrix[GACV.KMatrixPos_TimeLine] = arrayTime
    _Matrix[GACV.KMatrixPos_DayPos] = dayPos
    hfreqkdata = GVAR.g_ATraderKDatas[higherFreqBase].Matrix
    highBLen = len(hfreqkdata[GACV.KMatrixPos_TimeLine])
    for i in range(len(arrayTime)):
        if i > 0:
            bP[i] = eP[(i - 1)] + 1
            eP[i] = bP[i]
        while eP[i] < highBLen - 1 and hfreqkdata[(GACV.KMatrixPos_TimeLine, eP[i])] < arrayTime[i]:
            eP[i] = eP[i] + 1

        if eP[i] > 0 and hfreqkdata[(GACV.KMatrixPos_TimeLine, eP[i])] > arrayTime[i]:
            eP[i] = eP[i] - 1
        if hfreqkdata[(GACV.KMatrixPos_TimeLine, bP[i])] < arrayTime[i]:
            step = GVAR.atBarItemsLen()
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_Open, 0, True)
            _Matrix[begin::step, i] = hfreqkdata[begin::step, bP[i]]
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_High, 0, True)
            _Matrix[begin::step, i] = np.max(hfreqkdata[begin::step, bP[i]:eP[i] + 1], axis=1)
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_Low, 0, True)
            _Matrix[begin::step, i] = np.min(hfreqkdata[begin::step, bP[i]:eP[i] + 1], axis=1)
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_Close, 0, True)
            _Matrix[begin::step, i] = hfreqkdata[begin::step, eP[i]]
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_Volume, 0, True)
            _Matrix[begin::step, i] = np.sum(hfreqkdata[begin::step, bP[i]:eP[i] + 1], axis=1)
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_TurnOver, 0, True)
            _Matrix[begin::step, i] = np.sum(hfreqkdata[begin::step, bP[i]:eP[i] + 1], axis=1)
            begin = GVAR.atKMatixBarItemPos(GACV.KMatrix_OpenInterest, 0, True)
            _Matrix[begin::step, i] = hfreqkdata[begin::step, eP[i]]

    _UnfilledBarRef, _UnfilledIdx = CORE_ALGO.atMatrixUnfillComplete(_Matrix, GACV.KMatrixPos_End + 1, GVAR.atBarItemsLen(), GACV.KMatrix_Volume)
    GVAR.g_ATraderKDatas.append(dotdict({'iFreq': iFreq, 
     'FreqNum': 1, 
     'Matrix': _Matrix, 
     'UnfilledBarRef': _UnfilledBarRef, 
     'UnfilledIdx': _UnfilledIdx, 
     'baseMatrixPos': higherFreqBase, 
     'freComplete': np.array([]), 
     'baseBegin': bP, 
     'baseEnd': eP, 
     'CurrentBar': CORE_ALGO.atFillKMatrixFreshBar(_Matrix)}))
    KmatrixPos = len(GVAR.g_ATraderKDatas) - 1
    return KmatrixPos


def atStopOrderV2(HandleIdx, StopOrderType, TargetIdx, TargetOrderID, TargetPrice, StopGap, StopType, TrailingGap, TrailingType, Contracts, OrderAct, OrderCtg, OrderTag):
    """
    止盈止损单的底层下单接口，所有对用户开放的止盈止损下单函数最终都有要调用这个函数。
    正常返回新的ClientOrderID【ClientOrderID >= 0】,如果出错返回np.nan
    """
    ClientOrderID = np.nan
    if GVAR.atBeInBackTestMode():
        StopGap = np.float64(StopGap)
        TrailingGap = np.float64(TrailingGap)
        temp_array = np.zeros((GVAR.atSimStopOrderItemsLen(), 1))
        ClientOrderID = GVAR.g_ATraderSimUnfiredStopOrders.shape[1] if len(GVAR.g_ATraderSimUnfiredStopOrders.shape) == 2 else 0
        temp_array[GACV.SimStopOrder_ClientID] = ClientOrderID
        temp_array[GACV.SimStopOrder_HandleIdx] = HandleIdx
        temp_array[GACV.SimStopOrder_StopOrderType] = atStringToConst('StopOrderType', StopOrderType)
        temp_array[GACV.SimStopOrder_TargetIdx] = TargetIdx
        temp_array[GACV.SimStopOrder_TargetOrderID] = TargetOrderID
        temp_array[GACV.SimStopOrder_TargetPrice] = TargetPrice
        g_Matrix = GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx]
        temp_array[GACV.SimStopOrder_EntryTime] = g_Matrix.Matrix[(
         GACV.KMatrixPos_TimeLine, g_Matrix.CurrentBar[GVAR.g_ATraderSimCurBarFresh])]
        temp_array[GACV.SimStopOrder_FireTime] = 0
        temp_array[GACV.SimStopOrder_StopGap] = StopGap
        temp_array[GACV.SimStopOrder_StopGapType] = atStringToConst('StopGapType', StopType)
        temp_array[GACV.SimStopOrder_TrailingGap] = TrailingGap
        temp_array[GACV.SimStopOrder_TrailingType] = atStringToConst('TrailingType', TrailingType)
        temp_array[GACV.SimStopOrder_TrailingHigh] = 0
        temp_array[GACV.SimStopOrder_TrailingLow] = 0
        temp_array[GACV.SimStopOrder_Contracts] = Contracts
        temp_array[GACV.SimStopOrder_OrderAct] = atStringToConst('OrderAct', OrderAct)
        temp_array[GACV.SimStopOrder_OrderCtg] = atStringToConst('OrderCtg', OrderCtg)
        temp_array[GACV.SimStopOrder_OrderTag] = 0
        temp_array[GACV.SimStopOrder_BeginTrailingPrice] = 0
        temp_array[GACV.SimStopOrder_InBeginTrailingBar] = False
        temp_array[GACV.SimStopOrder_IsBeginTrailing] = False
        temp_array[GACV.SimStopOrder_MPrice] = TargetPrice
        temp_array[GACV.SimStopOrder_StopTrailingPrice] = 0
        if TargetPrice > 0:
            temp_array[GACV.SimStopOrder_Status] = GACV.StopOrderStatus_Holding
        elif TargetOrderID >= 0:
            temp_array[GACV.SimStopOrder_Status] = GACV.StopOrderStatus_PreHolding
            temp_array[GACV.SimStopOrder_TargetIdx] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_TargetIdx, TargetOrderID)]
            temp_array[GACV.SimStopOrder_OrderAct] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderAct, TargetOrderID)]
            temp_array[GACV.SimStopOrder_Contracts] = GVAR.g_ATraderSimOrders[(GACV.SimOrder_Contracts, TargetOrderID)]
        if temp_array[GACV.SimStopOrder_StopOrderType] == GACV.StopOrderType_Trailing and TargetPrice > 0:
            if temp_array[GACV.SimStopOrder_OrderAct] == GACV.OrderAct_Buy:
                if temp_array[GACV.SimStopOrder_TrailingType] == GACV.StopGapType_Point:
                    temp_array[GACV.SimStopOrder_BeginTrailingPrice] = TargetPrice + TrailingGap
                elif temp_array[GACV.SimStopOrder_TrailingType] == GACV.StopGapType_Percent:
                    temp_array[GACV.SimStopOrder_BeginTrailingPrice] = TargetPrice * (1 + TrailingGap / 100)
            else:
                if temp_array[GACV.SimStopOrder_OrderAct] == GACV.OrderAct_Sell:
                    if temp_array[GACV.SimStopOrder_TrailingType] == GACV.StopGapType_Point:
                        temp_array[GACV.SimStopOrder_BeginTrailingPrice] = TargetPrice - TrailingGap
                else:
                    if temp_array[GACV.SimStopOrder_TrailingType] == GACV.StopGapType_Percent:
                        temp_array[GACV.SimStopOrder_BeginTrailingPrice] = TargetPrice * (1 - TrailingGap / 100)
                    if np.isnan(TargetOrderID):
                        temp_array[GACV.SimStopOrder_InBarBegin] = True
                    else:
                        if (GVAR.g_ATraderSimUnfilledOrders == TargetOrderID).any():
                            temp_array[GACV.SimStopOrder_InBarBegin] = False
                        else:
                            if GVAR.g_ATraderSimTrades.size > 0 and (GVAR.g_ATraderSimTrades[GACV.SimTrade_OrderID] == TargetOrderID).any():
                                temp_array[GACV.SimStopOrder_InBarBegin] = False
                            else:
                                write_userlog('止盈止损单对应的标的单不存在!', level='warn')
                                temp_array[GACV.SimStopOrder_Status] = GACV.StopOrderStatus_Cancelled
                                if GVAR.g_ATraderSimStopOrders.size < 1:
                                    GVAR.g_ATraderSimStopOrders = temp_array.reshape((-1,
                                                                                      1)).copy()
                                else:
                                    GVAR.g_ATraderSimStopOrders = np.append(GVAR.g_ATraderSimStopOrders, temp_array, axis=1)
            if GVAR.g_ATraderSimUnfiredStopOrders.size < 1 or len(GVAR.g_ATraderSimUnfiredStopOrders.shape) != 2:
                GVAR.g_ATraderSimUnfiredStopOrders = temp_array.reshape((-1, 1)).copy()
            else:
                GVAR.g_ATraderSimUnfiredStopOrders = np.append(GVAR.g_ATraderSimUnfiredStopOrders, temp_array, axis=1)
    if GVAR.atBeInRealMode():
        if TargetIdx >= 0:
            Market = GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Market']
            Code = GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Code']
        else:
            Market = ''
            Code = ''
        params = {'StrategyName': GVAR.g_ATraderStrategyName, 
         'Handle': GVAR.g_ATraderRealHandles[HandleIdx], 
         'Market': Market, 
         'Code': Code, 
         'Contracts': Contracts, 
         'StopGap': StopGap, 
         'OrderAct': OrderAct, 
         'OrderCtg': OrderCtg, 
         'targetPrice': TargetPrice, 
         'targetOrder': TargetOrderID, 
         'StopBy': StopType, 
         'StopType': StopOrderType, 
         'TrailingStopGap': TrailingGap, 
         'TrailingStopBy': TrailingType, 
         'OrderTag': OrderTag}
        ClientOrderID = tb_command.atSendCmdATraderSTTradeStopOrder(params)
    return ClientOrderID


def atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, OrderCtg, OrderAct, OffsetFlag, OrderTag):
    """具体下单的函数，将各个报单所需要的参数保存在g_ATraderSimOrders中"""
    orderID = np.nan
    GVAR.atResetAlgoOrderSignal()
    if GVAR.atBeInBackTestMode():
        GVAR.atEnterDirectOrderMode()
        g_Matrix = GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx]
        orderID = GVAR.g_ATraderSimOrders.shape[1] if len(GVAR.g_ATraderSimOrders.shape) == 2 else 0
        temp_array = np.zeros(GVAR.atSimOrderItemsLen())
        temp_array[GACV.SimOrder_HandleIdx] = HandleIdx
        temp_array[GACV.SimOrder_OrderID] = orderID
        temp_array[GACV.SimOrder_OrderTime] = g_Matrix.Matrix[(
         GACV.KMatrixPos_TimeLine, g_Matrix['CurrentBar'][GVAR.g_ATraderSimCurBarFresh])]
        temp_array[GACV.SimOrder_Status] = GACV.OrderStatus_PreHolding
        temp_array[GACV.SimOrder_TargetIdx] = TargetIdx
        temp_array[GACV.SimOrder_Contracts] = Contracts
        temp_array[GACV.SimOrder_Price] = Price
        temp_array[GACV.SimOrder_OrderCtg] = atStringToConst('OrderCtg', OrderCtg)
        temp_array[GACV.SimOrder_OrderAct] = atStringToConst('OrderAct', OrderAct)
        temp_array[GACV.SimOrder_OffsetFlag] = atStringToConst('OffsetFlag', OffsetFlag)
        temp_array[GACV.SimOrder_OrderTag] = 0
        temp_array[GACV.SimOrder_RemainNum] = Contracts
        if temp_array[GACV.SimOrder_OrderCtg] == GACV.OrderCtg_Limit:
            temp_array[GACV.SimOrder_OpenFrozenPrice] = Price
        else:
            temp_array[GACV.SimOrder_OpenFrozenPrice] = 0
        temp_array[GACV.SimOrder_FilledTime] = 0
        GVAR.g_ATraderSimUnfilledOrders = np.append(GVAR.g_ATraderSimUnfilledOrders, np.array([orderID], dtype=np.int))
        if len(GVAR.g_ATraderSimOrders.shape) != 2 or GVAR.g_ATraderSimOrders.size < 1:
            GVAR.g_ATraderSimOrders = temp_array.reshape((-1, 1)).copy()
        else:
            GVAR.g_ATraderSimOrders = np.append(GVAR.g_ATraderSimOrders, temp_array.reshape((-1,
                                                                                             1)), axis=1)
    else:
        if GVAR.atBeInRealMode():
            if GVAR.atBeInAlgorithmTradeMode():
                raise Exception('TODO it')
                GVAR.atGenerateAlgoOrderSignal()
                Market = GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Market']
                Code = GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Code']
                if GVAR.g_ATraderRealCurBarOperation.empty:
                    GVAR.g_ATraderRealCurBarOperation[0] = np.nan
                    GVAR.g_ATraderRealCurBarOperation[0].HandleIdx = HandleIdx
                    GVAR.g_ATraderRealCurBarOperation[0].Market = Market
                    GVAR.g_ATraderRealCurBarOperation[0].Code = Code
                    GVAR.g_ATraderRealCurBarOperation[0].Contracts = Contracts
                    GVAR.g_ATraderRealCurBarOperation[0].Price = Price
                    GVAR.g_ATraderRealCurBarOperation[0].OrderCtg = OrderCtg
                    GVAR.g_ATraderRealCurBarOperation[0].OrderAct = OrderAct
                    GVAR.g_ATraderRealCurBarOperation[0].OffsetFlag = OffsetFlag
                    GVAR.g_ATraderRealCurBarOperation[0].OrderTag = OrderTag
                    GVAR.g_ATraderRealCurBarOperation[0].RemainNum = Contracts
            else:
                ls = list(GVAR.g_ATraderRealCurBarOperation.columns)
                ls.append(-1)
                curlen = np.max(ls) + 1
                markets = GVAR.g_ATraderRealCurBarOperation.loc['Market']
                codes = GVAR.g_ATraderRealCurBarOperation.loc['Code']
                markets_codes = np.array(['%s%s' % (c, m) for c, m in zip(codes, markets)])
                _, Idx = CORE_ALGO.ismember(np.array(['%s%s' % (Code, Market)]), markets_codes)
                if Idx.size > 0:
                    GVAR.g_ATraderRealCurBarOperation[Idx[0]].Contracts += Contracts
                    GVAR.g_ATraderRealCurBarOperation[Idx[0]].RemainNum += Contracts
                else:
                    GVAR.g_ATraderRealCurBarOperation[curlen] = np.nan
                    GVAR.g_ATraderRealCurBarOperation[curlen].HandleIdx = HandleIdx
                    GVAR.g_ATraderRealCurBarOperation[curlen].Market = Market
                    GVAR.g_ATraderRealCurBarOperation[curlen].Code = Code
                    GVAR.g_ATraderRealCurBarOperation[curlen].Contracts = Contracts
                    GVAR.g_ATraderRealCurBarOperation[curlen].Price = Price
                    GVAR.g_ATraderRealCurBarOperation[curlen].OrderCtg = OrderCtg
                    GVAR.g_ATraderRealCurBarOperation[curlen].OrderAct = OrderAct
                    GVAR.g_ATraderRealCurBarOperation[curlen].OffsetFlag = OffsetFlag
                    GVAR.g_ATraderRealCurBarOperation[curlen].OrderTag = OrderTag
                    GVAR.g_ATraderRealCurBarOperation[curlen].RemainNum = Contracts
                if not GVAR.atExistAlgoOrderSignal():
                    OrderTag = 'undefined' if len(OrderTag) == 0 else OrderTag
                    params = dotdict({'Market': GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Market'], 
                     'Code': GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Code'], 
                     'StrategyName': GVAR.g_ATraderStrategyName, 
                     'Handle': GVAR.g_ATraderRealHandles[HandleIdx], 
                     'Price': Price, 
                     'Contracts': Contracts, 
                     'OrderAct': OrderAct, 
                     'OrderCtg': OrderCtg, 
                     'OffsetFlag': OffsetFlag, 
                     'OrderTag': OrderTag})
                    orderID = tb_command.atSendATraderSTTradeOperation(params)
        else:
            ToolBoxErrors.unexpect_switch_error('runmode')
    return orderID


@apply_rule(verify_that('MarketOrderHolding').is_instance_of(bool))
def traderSetMarketOrderHoldingType(MarketOrderHolding):
    GVAR.g_ATraderMarketOrderHolding = bool(MarketOrderHolding)


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('StrategyName').is_instance_of(str), verify_that('Log').is_instance_of(str))
def traderPutLog(HandleIdx, StrategyName, Log):
    """显示提示信息，函数调用后，理财牛主程序会在工具栏弹出内容为strNotice的提示框"""
    HandleIdx = int(HandleIdx)
    return tb_command.at_send_cmd_TraderPutLog(HandleIdx, StrategyName, Log)


@apply_rule(verify_that('Market').is_instance_of(str), verify_that('Code').is_instance_of(str))
def traderGetFutureInfo(Market, Code):
    return tb_command.at_send_cmd_TraderGetFutureInfo(Market, Code)


@apply_rule(verify_that('TargetIdxA').is_instance_of((int, float, Iterable)))
def traderGetFutureInfoV2(TargetIdxA):
    _, TargetIdxA = atCheckIdx('traderGetFutureInfoV2', None, TargetIdxA, toarray=True)
    df = pd.DataFrame()
    if not GVAR.g_ATraderFutureInfoMapV2.empty:
        df = GVAR.g_ATraderFutureInfoMapV2[TargetIdxA]
    return df


@apply_rule(verify_that('TargetIdxA').is_instance_of((int, float, Iterable)))
def traderGetTargetInfoV2(TargetIdxA):
    _, TargetIdxA = atCheckIdx('traderGetTargetInfoV2', None, TargetIdxA, toarray=True)
    if GVAR.g_ATraderFutureInfoMapV2.empty:
        raise ValueError('Only support in BackTest, RealTrade and Replay')
    Infos = GVAR.g_ATraderFutureInfoMapV2[TargetIdxA]
    return Infos


@apply_rule(verify_that('Market').is_instance_of(str), verify_that('Code').is_instance_of(str))
def traderGetTargetInfo(Market, Code):
    """根据标的的市场名称与标的名称，获取标的的基本信息"""
    temp_id = '%s_%s' % (Market, Code)
    if temp_id in GVAR.g_ATraderFutureInfoMap:
        info = GVAR.g_ATraderFutureInfoMap[temp_id]
    else:
        info = tb_command.at_send_cmd_TraderGetFutureInfo(Market, Code)
        GVAR.g_ATraderFutureInfoMap[temp_id] = info
    return info


@apply_rule(verify_that('TargetList').is_instance_of((list, tuple)), verify_that('freq').is_instance_of((int, str)), verify_that('BeginDay').is_instance_of(int), verify_that('EndDay').is_instance_of(int))
def traderGetTradingTime(TargetList, freq, BeginDay, EndDay):
    """获取指定日期内的交易时间轴，AT返回的为一个交易时间索引和具体的交易时间"""
    atDefineConst()
    iFreq = freq if isinstance(freq, int) else atStringToConst('KBaseFreq', freq)
    askFreq = 'sec' if iFreq == GACV.KFreq_Sec else 'min'
    DayPos = np.array([])
    Time = np.array([])
    matFile = tb_command.at_send_ATraderGetTradingTime(TargetList, askFreq, BeginDay, EndDay)
    try:
        mat_content = load_mat(matFile, error='raise')
    except Exception:
        UTILS_UTIL.run_ignore_exception(os.remove, matFile)

    tb_command.atClearMatFileIncludeZeroDate(matFile, EndDay)
    if 'DayPos' in mat_content and 'Time' in mat_content:
        DayPos = mat_content['DayPos'].flatten().astype(np.int)
        Time = mat_content['Time'].flatten()
    if iFreq >= GACV.KFreq_Day:
        dayEndPos = np.where(DayPos == 1)[0]
        dayEndPos = np.array(dayEndPos) - 1
        dayEndPos = np.append(dayEndPos, np.array([len(DayPos) - 1]))
        dayEndPos = dayEndPos[(dayEndPos >= 0)]
        Time = Time[dayEndPos]
        if iFreq == GACV.KFreq_Week:
            Time = Time[(UTILS_DT.weekday(Time) == 6)]
        if iFreq == GACV.KFreq_Month:
            arrayTimeM = []
            for i in range(len(Time)):
                if i == len(Time) - 1 or UTILS_DT.month(Time[(i + 1)]) > UTILS_DT.month(Time[i]):
                    arrayTimeM.append(Time[i])

            Time = np.array(arrayTimeM)
        if iFreq == GACV.KFreq_Year:
            arrayTimeY = []
            for i in range(len(Time)):
                if i == len(Time) - 1 or UTILS_DT.year(Time[(i + 1)]) > UTILS_DT.year(Time[i]):
                    arrayTimeY.append(Time[i])

            Time = np.array(arrayTimeY)
        DayPos = np.ones((len(Time),), dtype=np.int)
    return (Time, DayPos)


@apply_rule(verify_that('BeginDay').is_valid_date(), verify_that('EndDay').is_instance_of(int))
def traderGetTradingDays(BeginDay, EndDay):
    if len(GVAR.g_ATraderTradingDays) < 1:
        GVAR.g_ATraderTradingDays = tb_command.at_send_cmd_ATraderGetTradingDays()
    if EndDay == 0:
        EndDay = tb_command.atSendCmdGetCurTradeDate()
    BeginDay_Position = np.where(GVAR.g_ATraderTradingDays >= BeginDay)
    if len(BeginDay_Position[0]) < 1:
        raise ValueError(const_da.Enum_Const.ERROR_INPUT_START_DATE.value)
    BeginDay_Position = BeginDay_Position[0][0]
    EndDay_Position = np.where(GVAR.g_ATraderTradingDays <= EndDay)
    if len(EndDay_Position[0]) < 1:
        raise ValueError(const_da.Enum_Const.ERROR_INPUT_END_DATE.value)
    EndDay_Position = EndDay_Position[0][(-1)]
    Days = GVAR.g_ATraderTradingDays[BeginDay_Position:EndDay_Position + 1]
    return Days


@apply_rule(verify_that('KFrequency').is_valid_frequency(), verify_that('DateSpan').is_greater_or_equal_than(0), verify_that('FillUp').is_instance_of(bool))
def traderAppendKDataScope(KFrequency, DateSpan, FillUp):
    """调用获取行情数据接口函数，并根据输入的频率，和日期跨度，对基础数据进行处理，填充全局行情数据变量"""
    if not GVAR.g_ATraderStraInputInfo:
        raise ValueError(const_da.Enum_Const.ERROR_EMPTY_TARGETLIST.value)
    iKFreq = atStringToConst('KBaseFreq', KFrequency)
    BeginDate = GVAR.g_ATraderStraInputInfo.BeginDate
    EndDate = GVAR.g_ATraderStraInputInfo.EndDate
    if DateSpan > 0:
        Days = traderGetTradingDays(0, 99999999)
        _index = np.argwhere(Days > BeginDate)
        if _index.size > 0:
            BeginDate = Days[max(0, _index[(0, 0)] - DateSpan)]
    ATraderSimBaseDatas = atGetKDataMulti(GVAR.g_ATraderStraInputInfo.TargetList, KFrequency, 1, BeginDate, EndDate, FillUp, GVAR.g_ATraderStraInputInfo.FQ, GVAR.g_ATraderAccountHandleArray, GVAR.g_ATraderStrategyName)
    if len(ATraderSimBaseDatas) == 0:
        raise ValueError(const_da.Enum_Const.ERROR_EMPTY_HISTORY_DATA.value)
    if iKFreq == GACV.KFreq_Tick:
        arrayTime, dayPos = CORE_ALGO.atCalculateTimeLineAndDayPos(ATraderSimBaseDatas)
    else:
        if EndDate == 0 or BeginDate <= EndDate:
            arrayTime, dayPos = traderGetTradingTime(GVAR.g_ATraderStraInputInfo.TargetList, KFrequency, BeginDate, EndDate)
        else:
            arrayTime = np.array([])
            dayPos = np.array([])
    if arrayTime.size < 1:
        raise ValueError(const_da.Enum_Const.ERROR_EMPTY_TIMELINE.value)
    atSetRealTradeSaveFreshPositionInAppend(ATraderSimBaseDatas, arrayTime)
    _Matrix = GVAR.generate_base_ndarray(len(ATraderSimBaseDatas), len(arrayTime))
    _Matrix[GACV.KMatrixPos_TimeLine] = arrayTime
    _Matrix[GACV.KMatrixPos_DayPos] = dayPos
    _t = GACV.KMatrixPos_End + 1 + len(GVAR.g_ATraderStraInputInfo.TargetList) * GVAR.atBarItemsLen()
    _Matrix[GACV.KMatrixPos_End + 1:_t] = CORE_ALGO.atFillToTimeLine(arrayTime, ATraderSimBaseDatas, iKFreq)
    _UnfilledBarRef, _UnfilledIdx = CORE_ALGO.atMatrixUnfillComplete(_Matrix, GACV.KMatrixPos_End + 1, GVAR.atBarItemsLen(), GACV.KMatrix_Volume)
    GVAR.g_ATraderKDatas.append(dotdict({'iFreq': iKFreq, 
     'FreqNum': 1, 
     'Matrix': _Matrix, 
     'UnfilledBarRef': _UnfilledBarRef, 
     'UnfilledIdx': _UnfilledIdx, 
     'CurrentBar': CORE_ALGO.atFillKMatrixFreshBar(_Matrix)}))


@apply_rule(verify_that('TargetIdx').is_instance_of((int, float)).is_greater_or_equal_than(0), verify_that('Date').is_valid_date(), verify_that('FQ').is_valid_fq())
def traderGetTickDataV2(TargetIdx, Date, FQ):
    _, TargetIdx = atCheckIdx('traderGetTickDataV2', None, TargetIdx, toarray=False)
    if 'TargetList' in GVAR.g_ATraderStraInputInfo:
        Market = GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Market']
        Code = GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx]['Code']
    else:
        raise ValueError(const_da.Enum_Const.ERROR_SUPPORT_REALTRADE_REPLAY.value)
    info = tb_command.atLoadTickDataFromPro(Market, Code, Date, 'NA')
    return (
     info.Time, info.Price, info.Volume, info.VolumeTick, info.TurnOver, info.OpenInterest, info.BidPrice, info.BidVolume, info.AskPrice, info.AskVolume)


@apply_rule(verify_that('InitialCash').is_instance_of((int, float)), verify_that('Costfee').is_instance_of((int, float)), verify_that('Rate').is_instance_of((int, float)), verify_that('SlidePrice').is_instance_of((int, float)))
def traderSetBacktest(InitialCash, Costfee, Rate, SlidePrice, *args):
    function_name = sys._getframe().f_code.co_name
    GVAR.g_AtraderSetInfo['PriceLoc'] = 1
    GVAR.g_AtraderSetInfo['DealType'] = 0
    GVAR.g_AtraderSetInfo['LimitType'] = 0
    GVAR.g_AtraderSetInfo['InitialCash'] = InitialCash
    GVAR.g_AtraderSetInfo['Costfee'] = Costfee
    GVAR.g_AtraderSetInfo['Rate'] = Rate
    GVAR.g_AtraderSetInfo['SlidePrice'] = SlidePrice
    if len(args) > 0:
        verify_that('PriceLoc')._is_instance_of((int, float), function_name, args[0])._is_greater_or_equal_than(0, function_name, args[0])
        GVAR.g_AtraderSetInfo['PriceLoc'] = args[0]
    if len(args) > 1:
        verify_that('DealType')._is_in(function_name, args[1], [0, 1, 2], ignore_value=False)
        GVAR.g_AtraderSetInfo['DealType'] = args[1]
    if len(args) > 2:
        verify_that('LimitType')._is_in(function_name, args[2], [0, 1], ignore_value=False)
        GVAR.g_AtraderSetInfo['LimitType'] = args[2]


@apply_rule(verify_that('bParalMode').is_in([True, False], ignore_value=False))
def traderSetParalMode(bParalMode):
    GVAR.g_Parral = bParalMode


@apply_rule(verify_that('KFrequency').is_valid_frequency(), verify_that('KFreNum').is_instance_of(int).is_greater_or_equal_than(1))
def traderRegKData(KFrequency, KFreNum):
    """
    Idx = [A B C], A为g_ATraderKDatas索引, B为g_ATraderKDataMatrix中Matrix索引, C为DataValueFresh中索引
    """
    baseFreqMatrix = np.nan
    TargetListLen = len(GVAR.g_ATraderStraInputInfo.TargetList)
    iFreq = atStringToConst('KBaseFreq', KFrequency)
    Idx = np.array([[np.nan] * TargetListLen, [0] * TargetListLen, [0] * TargetListLen]).T
    if iFreq < GVAR.g_ATraderStraInputInfo.KFrequencyI:
        raise ValueError(const_da.Enum_Const.ERROR_FREQ_TOO_HIGH.value)
    else:
        if GACV.KFreq_Tick == iFreq and KFreNum != 1:
            raise ValueError(const_da.Enum_Const.ERROR_NOTSUPPORT_TICK_MULTI_FREQNUM.value)
        for i in range(len(GVAR.g_ATraderKDatas)):
            if GVAR.g_ATraderKDatas[i].iFreq != iFreq:
                pass
            else:
                if GVAR.g_ATraderKDatas[i].FreqNum == KFreNum and GVAR.g_ATraderStraInputInfo.KFrequencyI == iFreq and (KFreNum == 1 or GVAR.g_ATraderStraInputInfo.KFreNum == KFreNum):
                    Idx = np.array([[i] * TargetListLen, range(TargetListLen), [np.nan] * TargetListLen]).T
                    return Idx
                if GVAR.g_ATraderKDatas[i]['FreqNum'] == 1:
                    baseFreqMatrix = i

        perbarLen = GVAR.atBarItemsLen()
        np_fmax = np.fmax
        np_fmin = np.fmin
        if np.isnan(baseFreqMatrix):
            baseFreqMatrix = FindOrFillBaseKMatrix(iFreq)
            if KFreNum == 1:
                Idx = np.array([[baseFreqMatrix] * TargetListLen, range(TargetListLen), [np.nan] * TargetListLen]).T
            if np.isnan(Idx[0][0]):
                BaseTMLine = GVAR.g_ATraderKDatas[baseFreqMatrix].Matrix.shape[1]
                eP = np.arange(BaseTMLine)
                base_freq_kdata = GVAR.g_ATraderKDatas[baseFreqMatrix].Matrix
                ind_d = {i:i for i in range(base_freq_kdata.shape[0])}
                CombinedMatrix = base_freq_kdata.copy()
                matrix_cache = np.zeros((base_freq_kdata.shape[0], 1))
                _H = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_High + 1)]
                _L = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_Low + 1)]
                _V = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_Volume + 1)]
                _T = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_TurnOver + 1)]
                _O = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_Open + 1)]
                _C = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_Close + 1)]
                _I = ind_d[(GACV.KMatrixPos_End + GACV.KMatrix_OpenInterest + 1)]
                baseDayPos = base_freq_kdata[GACV.KMatrixPos_DayPos]
                if iFreq <= GACV.KFreq_Min:
                    modValue = np.array(baseDayPos % KFreNum)
                else:
                    modValue = np.arange(1, 1 + BaseTMLine) % KFreNum
                freComplete = np.where(modValue == 0, True, False)
                bP = np.where(modValue == 0, 1 - KFreNum, 1 - modValue)
                bP = (bP + np.arange(BaseTMLine)).astype(np.int)
                matrix_cache[:, 0] = CombinedMatrix[:, 0]
                for i in range(BaseTMLine):
                    if bP[i] == eP[i]:
                        matrix_cache[_H::perbarLen, 0] = CombinedMatrix[_H::perbarLen, bP[i]]
                        matrix_cache[_L::perbarLen, 0] = CombinedMatrix[_L::perbarLen, bP[i]]
                        matrix_cache[_V::perbarLen, 0] = CombinedMatrix[_V::perbarLen, bP[i]]
                        matrix_cache[_T::perbarLen, 0] = CombinedMatrix[_T::perbarLen, bP[i]]
                    else:
                        CombinedMatrix[_H::perbarLen, i] = np_fmax(matrix_cache[_H::perbarLen, 0], CombinedMatrix[_H::perbarLen, eP[i]])
                        CombinedMatrix[_L::perbarLen, i] = np_fmin(matrix_cache[_L::perbarLen, 0], CombinedMatrix[_L::perbarLen, eP[i]])
                        CombinedMatrix[_V::perbarLen, i] = matrix_cache[_V::perbarLen, 0] + CombinedMatrix[_V::perbarLen, eP[i]]
                        CombinedMatrix[_T::perbarLen, i] = matrix_cache[_T::perbarLen, 0] + CombinedMatrix[_T::perbarLen, eP[i]]
                        matrix_cache[_H::perbarLen, 0] = CombinedMatrix[_H::perbarLen, i]
                        matrix_cache[_L::perbarLen, 0] = CombinedMatrix[_L::perbarLen, i]
                        matrix_cache[_V::perbarLen, 0] = CombinedMatrix[_V::perbarLen, i]
                        matrix_cache[_T::perbarLen, 0] = CombinedMatrix[_T::perbarLen, i]

                CombinedMatrix[_O::perbarLen, :] = CombinedMatrix[_O::perbarLen, bP]
                CombinedMatrix[_C::perbarLen, :] = CombinedMatrix[_C::perbarLen, eP]
                CombinedMatrix[_I::perbarLen, :] = CombinedMatrix[_I::perbarLen, eP]
                if iFreq <= GACV.KFreq_Min:
                    dayFinishPos = np.where(baseDayPos == 1)[0]
                    dayFinishPos = dayFinishPos[(dayFinishPos - 1 >= 0)] - 1
                    dayFinishPos = np.append(dayFinishPos, len(baseDayPos) - 1)
                    freComplete[dayFinishPos] = True
                _Matrix = CombinedMatrix[:, freComplete]
                _UnfilledBarRef, _UnfilledIdx = CORE_ALGO.atMatrixUnfillComplete(_Matrix, GACV.KMatrixPos_End + 1, GVAR.atBarItemsLen(), GACV.KMatrix_Volume)
                GVAR.g_ATraderKDatas.append(dotdict({'iFreq': iFreq, 
                 'FreqNum': KFreNum, 
                 'Matrix': _Matrix, 
                 'baseMatrixPos': baseFreqMatrix, 
                 'baseBegin': bP, 
                 'baseEnd': eP, 
                 'freComplete': freComplete, 
                 'CurrentBar': CORE_ALGO.atFillKMatrixFreshBar(_Matrix), 
                 'UnfilledBarRef': _UnfilledBarRef, 
                 'UnfilledIdx': _UnfilledIdx}))
                NewKMatrixPos = len(GVAR.g_ATraderKDatas) - 1
                Idx = np.array([[NewKMatrixPos] * TargetListLen, range(TargetListLen), [np.nan] * TargetListLen]).T
            if iFreq != GVAR.g_ATraderStraInputInfo.KFrequencyI or KFreNum != GVAR.g_ATraderStraInputInfo.KFreNum:
                NewKMatrixPos = int(Idx[0][0])
                base0_matrix = GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_End + 1:]
                base0_tl = GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine]
                base0_fi = GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_FreshIdx]
                BaseTMLine = base0_matrix.shape[1]
                CombinedLen = GVAR.g_ATraderKDatas[NewKMatrixPos].Matrix.shape[1]
                shape = (perbarLen * TargetListLen, BaseTMLine)
                CombinedMatrix = np.zeros(shape)
                matrix_cache = np.zeros((shape[0], 1))
                ind_d = {i:i for i in range(shape[0])}
                targetTMPos = np.zeros((BaseTMLine,), dtype=np.int)
                bP = np.arange(BaseTMLine)
                eP = np.arange(BaseTMLine)
                _H = ind_d[GACV.KMatrix_High]
                _L = ind_d[GACV.KMatrix_Low]
                _V = ind_d[GACV.KMatrix_Volume]
                _T = ind_d[GACV.KMatrix_TurnOver]
                _O = ind_d[GACV.KMatrix_Open]
                _C = ind_d[GACV.KMatrix_Close]
                _I = ind_d[GACV.KMatrix_OpenInterest]
                _BB = ind_d[GACV.KMatrix_Bar_Begin]
                ref_tl = GVAR.g_ATraderKDatas[NewKMatrixPos].Matrix[GACV.KMatrixPos_TimeLine]
                for i in range(BaseTMLine):
                    freshTM = base0_tl[i]
                    if i > 0:
                        targetTMPos[i] = targetTMPos[(i - 1)]
                    while targetTMPos[i] < CombinedLen - 1 and ref_tl[targetTMPos[i]] < freshTM:
                        targetTMPos[i] = targetTMPos[i] + 1

                    while bP[i] > 0 and targetTMPos[(bP[i] - 1)] == targetTMPos[i]:
                        bP[i] = bP[i] - 1

                    if bP[i] == eP[i]:
                        matrix_cache[_H::perbarLen, 0] = base0_matrix[_H::perbarLen, bP[i]]
                        matrix_cache[_L::perbarLen, 0] = base0_matrix[_L::perbarLen, bP[i]]
                        matrix_cache[_V::perbarLen, 0] = base0_matrix[_V::perbarLen, bP[i]]
                        matrix_cache[_T::perbarLen, 0] = base0_matrix[_T::perbarLen, bP[i]]
                        CombinedMatrix[_H::perbarLen, bP[i]] = matrix_cache[_H::perbarLen, 0]
                        CombinedMatrix[_L::perbarLen, bP[i]] = matrix_cache[_L::perbarLen, 0]
                        CombinedMatrix[_V::perbarLen, bP[i]] = matrix_cache[_V::perbarLen, 0]
                        CombinedMatrix[_T::perbarLen, bP[i]] = matrix_cache[_T::perbarLen, 0]
                    else:
                        CombinedMatrix[_H::perbarLen, i] = np_fmax(matrix_cache[_H::perbarLen, 0], base0_matrix[_H::perbarLen, eP[i]])
                        CombinedMatrix[_L::perbarLen, i] = np_fmin(matrix_cache[_L::perbarLen, 0], base0_matrix[_L::perbarLen, eP[i]])
                        CombinedMatrix[_V::perbarLen, i] = matrix_cache[_V::perbarLen, 0] + base0_matrix[_V::perbarLen, eP[i]]
                        CombinedMatrix[_T::perbarLen, i] = matrix_cache[_T::perbarLen, 0] + base0_matrix[_T::perbarLen, eP[i]]
                        matrix_cache[_H::perbarLen, 0] = CombinedMatrix[_H::perbarLen, i]
                        matrix_cache[_L::perbarLen, 0] = CombinedMatrix[_L::perbarLen, i]
                        matrix_cache[_V::perbarLen, 0] = CombinedMatrix[_V::perbarLen, i]
                        matrix_cache[_T::perbarLen, 0] = CombinedMatrix[_T::perbarLen, i]

                CombinedMatrix[_O::perbarLen, :] = base0_matrix[_O::perbarLen, bP]
                CombinedMatrix[_C::perbarLen, :] = base0_matrix[_C::perbarLen, eP]
                CombinedMatrix[_I::perbarLen, :] = base0_matrix[_I::perbarLen, eP]
                oldRows = GACV.KMatrixPos_TimeLine + len(GVAR.g_ATraderRegKDataInfo) * TargetListLen * perbarLen
                newRows = GACV.KMatrixPos_TimeLine + (len(GVAR.g_ATraderRegKDataInfo) + 1) * TargetListLen * perbarLen
                GVAR.g_ATraderDataValueFresh = np.append(GVAR.g_ATraderDataValueFresh, CombinedMatrix[_BB:, base0_fi.astype(np.bool)], axis=0)
                GVAR.g_ATraderRegKDataInfo.append(dotdict({'KFrequency': KFrequency, 'KFreNum': KFreNum, 'iFreq': iFreq, 'kMatrixPos': NewKMatrixPos, 
                 'rowBegin': oldRows + 1, 'rowEnd': newRows, 'beginPos': bP, 'endPos': eP}))
                _t = len(GVAR.g_ATraderRegKDataInfo)
                Idx = np.array([[NewKMatrixPos] * TargetListLen, range(TargetListLen),
                 np.arange((_t - 1) * TargetListLen, _t * TargetListLen)]).T
            else:
                Idx = np.array([[NewKMatrixPos] * TargetListLen, range(TargetListLen), [np.nan] * TargetListLen]).T
    return Idx


@apply_rule(verify_that('Idx').is_instance_of((list, np.ndarray)), verify_that('length').is_greater_or_equal_than(1), verify_that('FilledUp').is_instance_of(bool))
def traderGetRegKData(Idx, length, FilledUp, *args):
    if len(args) > 0:
        v_ACV = args[0][0] if isinstance(args[0][0], dotdict) else dotdict(args[0][0])
        v_ATraderSimCurBarFresh = args[0][1]
        v_ATraderDataValueFresh = args[0][2]
        v_ATraderKDataMatrix = args[0][3]
    else:
        v_ACV = GACV
        v_ATraderSimCurBarFresh = GVAR.g_ATraderSimCurBarFresh
        v_ATraderDataValueFresh = GVAR.g_ATraderDataValueFresh
        v_ATraderKDataMatrix = GVAR.g_ATraderKDatas
    Idx = np.asarray(Idx)
    if len(Idx) < 1 or Idx.size < 1:
        raise ValueError('Idx expect type<numpy.ndarry> size>1')
    if len(Idx.shape) != 2:
        Idx = Idx.reshape(-1, 3)
    targetLen = Idx.shape[0]
    perbarLen = GVAR.atBarItemsLen()
    out_ndarray = np.ones((targetLen * (perbarLen + 1), length)) * np.nan
    if FilledUp:
        _t00 = int(Idx[(0, 0)])
        _bar00 = v_ATraderKDataMatrix[_t00].CurrentBar
        startPos = int(max(_bar00[v_ATraderSimCurBarFresh] - length + 1, 0))
        dataLen = int(_bar00[v_ATraderSimCurBarFresh] - startPos) + 1
        for i in range(targetLen):
            _t2 = int(_bar00[v_ATraderSimCurBarFresh]) + 1
            _tl = i * (perbarLen + 1)
            out_ndarray[_tl, -dataLen:] = v_ATraderKDataMatrix[_t00].Matrix[v_ACV.KMatrixPos_TimeLine, startPos:_t2]
            _idxi0 = int(Idx[(i, 0)])
            _idxi1 = int(Idx[(i, 1)])
            _mxi0 = v_ATraderKDataMatrix[_idxi0].Matrix
            _t2 = v_ATraderKDataMatrix[_idxi0].CurrentBar[v_ATraderSimCurBarFresh] + 1
            _rl = GVAR.atKMatixBarItemPos(v_ACV.KMatrix_Bar_Begin, _idxi1, contain_head=True)
            _rr = GVAR.atKMatixBarItemPos(v_ACV.KMatrix_Bar_End, _idxi1, contain_head=True) + 1
            _ll = i * (perbarLen + 1) + 1
            _lr = (i + 1) * (perbarLen + 1)
            out_ndarray[_ll:_lr, -dataLen:] = _mxi0[_rl:_rr, startPos:_t2]
            if not np.isnan(Idx[(i, 2)]):
                _idxi1 = int(Idx[i][1])
                _tl = i * (perbarLen + 1)
                out_ndarray[(_tl, -1)] = v_ATraderDataValueFresh[(v_ACV.KMatrixPos_TimeLine, v_ATraderSimCurBarFresh)]
                _rs = i * (perbarLen + 1) + 1
                _re = (i + 1) * (perbarLen + 1)
                _rs1 = v_ACV.KMatrixPos_TimeLine + _idxi1 * perbarLen + v_ACV.KMatrix_Bar_Begin + 1
                _re1 = v_ACV.KMatrixPos_TimeLine + _idxi1 * perbarLen + v_ACV.KMatrix_Bar_End + 2
                out_ndarray[_rs:_re, -1] = v_ATraderDataValueFresh[_rs1:_re1, v_ATraderSimCurBarFresh]

    else:
        for i in range(targetLen):
            _idxi0 = int(Idx[(i, 0)])
            _idxi1 = int(Idx[(i, 1)])
            endBarPos = v_ATraderKDataMatrix[_idxi0].CurrentBar[v_ATraderSimCurBarFresh]
            UnfillIdxPos = v_ATraderKDataMatrix[_idxi0].UnfilledBarRef[_idxi1][endBarPos]
            if not np.isnan(UnfillIdxPos):
                UnfillIdxPos = int(max(UnfillIdxPos - length, 0))
                startPos = int(v_ATraderKDataMatrix[_idxi0].UnfilledIdx[_idxi1][UnfillIdxPos])
                SingleMatrix = np.zeros((perbarLen + 1, endBarPos - startPos + 1))
                SingleMatrix[0, :] = v_ATraderKDataMatrix[_idxi0].Matrix[v_ACV.KMatrixPos_TimeLine,
                 startPos:endBarPos + 1]
                _t1 = GVAR.atKMatixBarItemPos(v_ACV.KMatrix_Bar_Begin, _idxi1, contain_head=True)
                _t2 = GVAR.atKMatixBarItemPos(v_ACV.KMatrix_Bar_End, _idxi1, contain_head=True)
                SingleMatrix[v_ACV.KMatrixPos_TimeLine + 1:perbarLen + 1, :] = v_ATraderKDataMatrix[_idxi0].Matrix[
                 _t1:_t2 + 1, startPos:endBarPos + 1]
                if not np.isnan(Idx[(i, 2)]):
                    _idxi2 = int(Idx[(i, 2)])
                    SingleMatrix[(0, -1)] = v_ATraderDataValueFresh[(v_ACV.KMatrixPos_TimeLine, v_ATraderSimCurBarFresh)]
                    _t1 = v_ACV.KMatrixPos_TimeLine + _idxi2 * perbarLen + v_ACV.KMatrix_Bar_Begin + 1
                    _t2 = v_ACV.KMatrixPos_TimeLine + _idxi2 * perbarLen + v_ACV.KMatrix_Bar_End + 2
                    SingleMatrix[v_ACV.KMatrixPos_TimeLine + 1:perbarLen + 1, -1] = v_ATraderDataValueFresh[_t1:_t2,
                     v_ATraderSimCurBarFresh]
                unFillPos = SingleMatrix[1 + v_ACV.KMatrix_Volume, :] > 0
                SingleMatrix = SingleMatrix[:, unFillPos]
                fillLen = min(SingleMatrix.shape[1], length)
                _t1 = out_ndarray.shape[1] - fillLen
                _t2 = SingleMatrix.shape[1] - fillLen
                out_ndarray[i * (perbarLen + 1):(i + 1) * (perbarLen + 1), _t1:] = SingleMatrix[:, _t2:]

    return out_ndarray


@apply_rule(verify_that('Market').is_instance_of((str,)), verify_that('Code').is_instance_of((str,)), verify_that('KFrequency').is_valid_frequency(), verify_that('KFreNum').is_instance_of(int).is_greater_or_equal_than(1), verify_that('BeginDate').is_valid_date().is_future_date(), verify_that('EndDate').is_valid_date().is_future_date(), verify_that('FilledUp').is_instance_of(bool), verify_that('FQ').is_valid_fq())
def traderGetKData(Market, Code, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ):
    info = atLoadKDataFromPro(Market, Code, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ)
    return (info.Time, info.Open, info.High, info.Low, info.Close, info.Volume, info.TurnOver, info.OpenInterest)


@apply_rule(verify_that('F').is_callable())
def traderRegUserIndi(F, *args):
    """将使用用户具体计算函数计算出的交易因子保存在g_ATraderDataValueFreshUserD中"""

    def parallel_computing_F(user_input_function_name, user_input_args, pf_ATraderSimCurBarFresh, pf_ACV, pf_ATraderDataValueFresh, pf_ATraderKDataMatrix, pf_ATraderUserD):
        result = user_input_function_name(user_input_args, (pf_ACV, pf_ATraderSimCurBarFresh, pf_ATraderDataValueFresh,
         pf_ATraderKDataMatrix, pf_ATraderUserD))
        return result

    result_F = [
     None] * GVAR.g_ATraderDataValueFresh.shape[1]
    pf_ATraderDataValueFresh = GVAR.g_ATraderDataValueFresh
    pf_ATraderKDatas = GVAR.g_ATraderKDatas
    pf_ATraderDataValueFreshUserD = GVAR.g_ATraderDataValueFreshUserD
    for i in range(GVAR.g_ATraderDataValueFresh.shape[1]):
        pf_ATraderSimCurBarFresh = i
        if args:
            temp_array = F(args[0], (
             GACV, pf_ATraderSimCurBarFresh, pf_ATraderDataValueFresh, pf_ATraderKDatas,
             pf_ATraderDataValueFreshUserD))
        else:
            temp_array = F((GACV, pf_ATraderSimCurBarFresh, pf_ATraderDataValueFresh, pf_ATraderKDatas,
             pf_ATraderDataValueFreshUserD))
        result_F[i] = temp_array

    indiData = np.column_stack(result_F)
    del result_F
    shape = GVAR.g_ATraderDataValueFreshUserD.shape
    GVAR.g_ATraderDataValueFreshUserD = UTILS_UTIL.append_or_assign_2d_array_axis0(GVAR.g_ATraderDataValueFreshUserD, indiData, shape[0])
    Idx = list(range(shape[0], shape[0] + indiData.shape[0]))
    GVAR.g_ATraderRegIndiCalc.append(dotdict({'F': F, 'cellPar': args}))
    return Idx


@apply_rule(verify_that('Idx').is_instance_of((list, int, np.ndarray)), verify_that('length').is_greater_or_equal_than(1))
def traderGetRegUserIndi(Idx, length, *args):
    if len(args) == 0:
        v_ATraderSimCurBarFresh = GVAR.g_ATraderSimCurBarFresh
        v_ATraderDataValueFreshUserD = GVAR.g_ATraderDataValueFreshUserD
    else:
        v_ATraderSimCurBarFresh = args[1]
        v_ATraderDataValueFreshUserD = args[4]
    value = np.array([np.nan])
    rowFreshUserD, colFreshUserD = v_ATraderDataValueFreshUserD.shape
    if v_ATraderSimCurBarFresh is None:
        v_ATraderSimCurBarFresh = colFreshUserD - 1
    if rowFreshUserD >= np.max(Idx):
        if v_ATraderSimCurBarFresh >= length - 1:
            value = v_ATraderDataValueFreshUserD[Idx, v_ATraderSimCurBarFresh - length + 1:v_ATraderSimCurBarFresh + 1]
    else:
        value = v_ATraderDataValueFreshUserD[Idx, 0:v_ATraderSimCurBarFresh + 1]
    return value


def traderGetCurrentBarV2():
    """
    获取当前bar的时间和序号
    
    :return: barNum, barTime
    """
    barNum = GVAR.g_ATraderSimCurBarFresh
    barTime = GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderSimCurBarFresh)]
    return (barNum, barTime)


def traderGetTargetList():
    """
    获取标的列表
    
    :return: 列表词典
    """
    if GVAR.atBeInBackTestMode():
        TargetList = GVAR.g_ATraderStraInputInfo.TargetList.copy()
    else:
        TargetList = GVAR.g_ATraderStraInputInfo.TargetList.copy()
    return TargetList


@apply_rule(verify_that('Market').is_instance_of((str,)), verify_that('Code').is_instance_of((str,)), verify_that('BeginDate').is_valid_date().is_future_date(), verify_that('EndDate').is_valid_date().is_future_date())
def traderGetMainContract(Market, Code, BeginDate, EndDate):
    if BeginDate > EndDate:
        raise ValueError(const_da.Enum_Const.ERROR_INPUT_BEGIN_GT_ENDDATE.value)
    df = tb_command.atSendCmdATraderGetTargetIns(Market, Code, BeginDate, EndDate)
    return df


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float, Iterable)))
def traderGetAccountInfoV2(HandleIdx):
    HandleIdx, _ = atCheckIdx('traderGetAccountInfoV2', HandleIdx, None, toarray=True)
    if GVAR.atBeInBackTestMode():
        PositionProfit = 0
        ValidCash = GVAR.atGetTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_ValidCash)
        OrderFrozen = GVAR.atGetTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_OrderFrozen)
        MarginFrozen = GVAR.atGetTraderAccountMatrixValue(HandleIdx, 0, GACV.ACMatrix_MarginFrozen)
        for i in range(len(GVAR.g_ATraderStraInputInfo.TargetList)):
            close_idx = GVAR.atKMatixBarItemPos(GACV.KMatrix_Close, i, True)
            curbarfresh = int(GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx].CurrentBar[GVAR.g_ATraderSimCurBarFresh])
            close = GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx].Matrix[(close_idx, curbarfresh)]
            close = 0 if np.isnan(close) else close
            Info = traderGetTargetInfoV2(i)
            targetIdex = i + 1
            _v1 = GVAR.atGetTraderAccountMatrixValue(HandleIdx, targetIdex, GACV.ACMatrix_LongPos)
            _v2 = GVAR.atGetTraderAccountMatrixValue(HandleIdx, targetIdex, GACV.ACMatrix_LongFrozen)
            _v3 = GVAR.atGetTraderAccountMatrixValue(HandleIdx, targetIdex, GACV.ACMatrix_LongAvg)
            _v4 = GVAR.atGetTraderAccountMatrixValue(HandleIdx, targetIdex, GACV.ACMatrix_ShortPos)
            _v5 = GVAR.atGetTraderAccountMatrixValue(HandleIdx, targetIdex, GACV.ACMatrix_ShortFrozen)
            _v6 = GVAR.atGetTraderAccountMatrixValue(HandleIdx, targetIdex, GACV.ACMatrix_ShortAvg)
            PositionProfit = PositionProfit + (_v1 + _v2) * (close - _v3) * Info.iloc[:, 0].loc['Multiple'] + (_v4 + _v5) * (_v6 - close) * Info.iloc[:, 0].loc['Multiple']

        HandListCap = ValidCash + OrderFrozen + MarginFrozen + PositionProfit
    else:
        if GVAR.atBeInRealMode():
            ValidCash = np.zeros((HandleIdx.size,))
            HandListCap = np.zeros((HandleIdx.size,))
            OrderFrozen = np.zeros((HandleIdx.size,))
            MarginFrozen = np.zeros((HandleIdx.size,))
            PositionProfit = np.zeros((HandleIdx.size,))
            for i in range(HandleIdx.size):
                real_handle = GVAR.g_ATraderRealHandles[HandleIdx[i]]
                tb_command.atSendCmdGetAccountInfo(np.array([real_handle]))
                HandleAccInfo = GVAR.g_ATraderAccountInfo[real_handle]
                HandListCap[i] = np.fix(HandleAccInfo['HandListCap'])
                ValidCash[i] = np.fix(HandleAccInfo['ValidCash'])
                OrderFrozen[i] = np.fix(HandleAccInfo['OrderFrozen'])
                MarginFrozen[i] = np.fix(HandleAccInfo['MarginFrozen'])
                PositionProfit[i] = np.fix(HandleAccInfo['PositionProfit'])

        else:
            ToolBoxErrors.unexpect_switch_error('runmode')
    write_syslog('traderGetAccountInfoV2 HandleIdx {!r}, ValidCash {!r}, HandListCap {!r}, OrderFrozen {!r}, MarginFrozen {!r}, PositionProfit {!r}'.format(HandleIdx, ValidCash, HandListCap, OrderFrozen, MarginFrozen, PositionProfit), level='info', trace_debug=True)
    return (
     ValidCash, HandListCap, OrderFrozen, MarginFrozen, PositionProfit)


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Contracts').is_greater_or_equal_than(1), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderBuyV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag):
    HandleIdx, TargetIdx = atCheckIdx('traderBuyV2', HandleIdx, TargetIdx, toarray=False)
    if GVAR.atBeInBackTestMode():
        Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Short')
        Pos = -(Position[(0, 0)] - Frozen[(0, 0)])
    else:
        if GVAR.atBeInRealMode():
            Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Short')
            Pos = -(Position[(0, 0)] - Frozen[(0, 0)])
        else:
            raise ToolBoxErrors.unexpect_switch_error('runmode')
    if Pos < 0:
        atTradeOperationV2(HandleIdx, TargetIdx, abs(Pos), Price, PriceType, 'buy', 'close', OrderTag)
    orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'buy', 'open', OrderTag)
    write_syslog('traderBuyV2 HandleIdx {!r}, TargetIdx {!r}, Contracts {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Contracts').is_greater_or_equal_than(1), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderSellShortV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag):
    HandleIdx, TargetIdx = atCheckIdx('traderSellShortV2', HandleIdx, TargetIdx, toarray=False)
    if GVAR.atBeInBackTestMode():
        Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Long')
        Pos = Position[(0, 0)] - Frozen[(0, 0)]
    else:
        if GVAR.atBeInRealMode():
            Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Long')
            Pos = Position[(0, 0)] - Frozen[(0, 0)]
        else:
            ToolBoxErrors.unexpect_switch_error('runmode')
    if Pos > 0:
        atTradeOperationV2(HandleIdx, TargetIdx, Pos, Price, PriceType, 'sell', 'close', OrderTag)
    orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'sell', 'open', OrderTag)
    write_syslog('traderSellShortV2 HandleIdx {!r}, TargetIdx {!r}, Contracts {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderBuyToCoverV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag):
    """
    买入平仓, 前提是有空仓, 否则操作无效
    回测处理逻辑, 回测时开多仓位管理为正数, 开空时仓位管理为负数, 并且日内所有持仓(不管期货现货)都可平, 不涉及双向持仓
    实盘或者回放时, 可能有之前的合约单子, 回放实盘现货(期权视为期货)日内不可平, 可能涉及双向持仓
    """
    HandleIdx, TargetIdx = atCheckIdx('traderBuyToCoverV2', HandleIdx, TargetIdx, toarray=False)
    Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Short')
    Pos = -(Position[(0, 0)] - Frozen[(0, 0)])
    if Pos >= 0:
        return
    if isinstance(Contracts, Number):
        if Contracts > abs(Pos):
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, abs(Pos), Price, PriceType, 'buy', 'close', OrderTag)
        else:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'buy', 'close', OrderTag)
    elif Contracts == 'all':
        orderID = atTradeOperationV2(HandleIdx, TargetIdx, abs(Pos), Price, PriceType, 'buy', 'close', OrderTag)
    write_syslog('traderBuyToCoverV2 HandleIdx {!r}, TargetIdx {!r}, Contracts {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Contracts').is_greater_or_equal_than(1), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderDirectBuyV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag):
    HandleIdx, TargetIdx = atCheckIdx('traderDirectBuyV2', HandleIdx, TargetIdx, toarray=False)
    orderID = np.nan
    Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Short')
    Pos = -(Position[(0, 0)] - Frozen[(0, 0)])
    if Pos < 0:
        if Contracts + Pos > 0:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, abs(Pos), Price, PriceType, 'buy', 'close', OrderTag)
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts + Pos, Price, PriceType, 'buy', 'open', OrderTag)
        else:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'buy', 'close', OrderTag)
    else:
        orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'buy', 'open', OrderTag)
    write_syslog('traderDirectBuyV2 HandleIdx {!r}, TargetIdx {!r}, Contracts {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderSellV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag):
    HandleIdx, TargetIdx = atCheckIdx('traderSellV2', HandleIdx, TargetIdx, toarray=False)
    Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Long')
    Pos = Position[(0, 0)] - Frozen[(0, 0)]
    if Pos <= 0:
        return np.nan
    if isinstance(Contracts, Number):
        if Contracts >= Pos:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Pos, Price, PriceType, 'sell', 'close', OrderTag)
        else:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'sell', 'close', OrderTag)
    elif Contracts == 'all':
        orderID = atTradeOperationV2(HandleIdx, TargetIdx, Pos, Price, PriceType, 'sell', 'close', OrderTag)
    write_syslog('traderSellV2 HandleIdx {!r}, TargetIdx {!r}, Contracts {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Contracts').is_instance_of((int, float)), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderDirectSellV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag):
    HandleIdx, TargetIdx = atCheckIdx('traderDirectSellV2', HandleIdx, TargetIdx, toarray=False)
    Position, Frozen, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Long')
    Pos = Position[(0, 0)] - Frozen[(0, 0)]
    if Pos > 0:
        if Pos - Contracts < 0:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Pos, Price, PriceType, 'sell', 'close', OrderTag)
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts - Pos, Price, PriceType, 'sell', 'open', OrderTag)
        else:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'sell', 'close', OrderTag)
    else:
        orderID = atTradeOperationV2(HandleIdx, TargetIdx, Contracts, Price, PriceType, 'sell', 'open', OrderTag)
    write_syslog('traderDirectSellV2 HandleIdx {!r}, TargetIdx {!r}, Contracts {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Contracts, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx').is_instance_of((int, float)), verify_that('Position').is_instance_of((int, float)), verify_that('Price').is_instance_of((int, float)), verify_that('PriceType').is_price_type(), verify_that('OrderTag').is_instance_of(str))
def traderPositionToV2(HandleIdx, TargetIdx, Position, Price, PriceType, OrderTag):
    """
    不管当前的仓位，将仓位调整至用户指定位置
    """
    HandleIdx, TargetIdx = atCheckIdx('traderPositionToV2', HandleIdx, TargetIdx, toarray=False)
    orderID = np.nan
    PositionL, FrozenL, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Long')
    PositionS, FrozenS, _ = traderGetAccountPositionDirV2(HandleIdx, TargetIdx, 'Short')
    PosL = PositionL[(0, 0)] - FrozenL[(0, 0)]
    PosS = PositionS[(0, 0)] - FrozenS[(0, 0)]
    if Position > 0:
        if PosS > 0:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, PosS, Price, PriceType, 'buy', 'close', OrderTag)
        if Position > PosL:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, Position - PosL, Price, PriceType, 'buy', 'open', OrderTag)
        elif Position < PosL:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, PosL - Position, Price, PriceType, 'sell', 'close', OrderTag)
    else:
        if Position < 0:
            if PosL > 0:
                orderID = atTradeOperationV2(HandleIdx, TargetIdx, PosL, Price, PriceType, 'sell', 'close', OrderTag)
            if -Position > PosS:
                orderID = atTradeOperationV2(HandleIdx, TargetIdx, -Position - PosS, Price, PriceType, 'sell', 'open', OrderTag)
            elif -Position < PosS:
                orderID = atTradeOperationV2(HandleIdx, TargetIdx, PosS + Position, Price, PriceType, 'buy', 'close', OrderTag)
        elif PosS > 0:
            orderID = atTradeOperationV2(HandleIdx, TargetIdx, PosS, Price, PriceType, 'buy', 'close', OrderTag)
    if PosL > 0:
        orderID = atTradeOperationV2(HandleIdx, TargetIdx, PosL, Price, PriceType, 'sell', 'close', OrderTag)
    write_syslog('traderPositionToV2 HandleIdx {!r}, TargetIdx {!r}, Position {!r}, Price {!r}, PriceType {!r}, OrderTag {!r}, orderID{!r}'.format(HandleIdx, TargetIdx, Position, Price, PriceType, OrderTag, orderID), level='info', trace_debug=True)
    return orderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float, Iterable)))
def traderCloseAllV2(HandleIdx):
    """平指定帐号所有持仓(不包含冻结部分)"""
    HandleIdx, _ = atCheckIdx('traderCloseAllV2', HandleIdx, None, toarray=True)
    if GVAR.atBeInBackTestMode():
        return
    if GVAR.atBeInRealMode():
        for handleidx in HandleIdx:
            if handleidx >= len(GVAR.g_ATraderAccountHandleArray) or handleidx < 0:
                write_userlog('HandleIdx范围在(%d-%d)' % (0, len(GVAR.g_ATraderAccountHandleArray)), level='warn')
                continue
                tb_command.atSendCmdATraderCloseOperation(handleidx)

    else:
        raise ValueError(const_da.Enum_Const.ERROR_SUPPORT_REALTRADE_REPLAY.value)


@apply_rule(verify_that('block').is_instance_of(str))
def traderGetCodeList(block, **kwargs):
    """
    获得指数（包含权重和成分股）、行业板块（没有权重，只有成分股）、地域板块（没有权重，只有成分股）、期权板块的信息，包括成分股及权重等信息
    """
    mat_content = tb_command.at_send_cmd_ATraderGetCodeList(block, **kwargs)
    df = pd.DataFrame(mat_content['IDPWeightArray'], columns=['Market', 'Code', 'Name', 'BlockName', 'Weight'])
    result = list(df.T.head().to_dict().values())
    return result


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float, Iterable)), verify_that('TargetIdx').is_instance_of((int, float, Iterable)))
def traderGetAccountPositionV2(HandleIdx, TargetIdx):
    HandleIdx, TargetIdx = atCheckIdx('traderGetAccountPositionV2', HandleIdx, TargetIdx, toarray=True)
    Position = np.zeros((HandleIdx.size, TargetIdx.size))
    Frozen = np.zeros((HandleIdx.size, TargetIdx.size))
    AvgPrice = np.zeros((HandleIdx.size, TargetIdx.size))
    if GVAR.atBeInBackTestMode():
        TargetIdx = TargetIdx + 1
        PositionL = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos)
        FrozenL = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongFrozen)
        AvgPriceL = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongAvg)
        PositionS = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos)
        FrozenS = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortFrozen)
        AvgPriceS = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortAvg)
        Position = (PositionL - PositionS).reshape(HandleIdx.size, TargetIdx.size)
        Frozen = (FrozenL - FrozenS).reshape(HandleIdx.size, TargetIdx.size)
        AvgPrice = (AvgPriceL * (Position > 0) + AvgPriceS * (Position < 0)).reshape(HandleIdx.size, TargetIdx.size)
    else:
        if GVAR.atBeInRealMode():
            for j in range(HandleIdx.size):
                for i in range(TargetIdx.size):
                    Position[(j, i)], Frozen[(j, i)], AvgPrice[(j, i)] = tb_command.atSendCmdATraderSTGetAccountPosition(GVAR.g_ATraderRealHandles[HandleIdx[j]], GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx[i]]['Market'], GVAR.g_ATraderStraInputInfo.TargetList[TargetIdx[i]]['Code'])

        else:
            ToolBoxErrors.unexpect_switch_error('runmode')
    write_syslog('traderGetAccountPositionV2 Position {!r}, Frozen {!r}, AvgPrice {!r}'.format(Position, Frozen, AvgPrice), level='info', trace_debug=True)
    return (
     Position, Frozen, AvgPrice)


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float, Iterable)), verify_that('TargetIdx').is_instance_of((int, float, Iterable)), verify_that('LongShort').is_in(['Long', 'Short']))
def traderGetAccountPositionDirV2(HandleIdx, TargetIdx, LongShort):
    """根据用户选择持仓方向，返回当前持仓，冻结持仓，持仓总价"""
    HandleIdx, TargetIdx = atCheckIdx('traderGetAccountPositionDirV2', HandleIdx, TargetIdx, toarray=True)
    Position = np.zeros((HandleIdx.size, TargetIdx.size))
    Frozen = np.zeros((HandleIdx.size, TargetIdx.size))
    AvgPrice = np.zeros((HandleIdx.size, TargetIdx.size))
    if GVAR.atBeInBackTestMode():
        TargetIdx = TargetIdx + 1
        if LongShort == 'Long':
            Position = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongPos).reshape(HandleIdx.size, TargetIdx.size)
            Frozen = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongFrozen).reshape(HandleIdx.size, TargetIdx.size)
            AvgPrice = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_LongAvg).reshape(HandleIdx.size, TargetIdx.size)
        else:
            Position = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortPos).reshape(HandleIdx.size, TargetIdx.size)
            Frozen = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortFrozen).reshape(HandleIdx.size, TargetIdx.size)
            AvgPrice = GVAR.atGetTraderAccountMatrixValue(HandleIdx, TargetIdx, GACV.ACMatrix_ShortAvg).reshape(HandleIdx.size, TargetIdx.size)
    else:
        if GVAR.atBeInRealMode():
            for i, t in enumerate(TargetIdx):
                Position[(0, i)], Frozen[(0, i)], AvgPrice[(0, i)] = tb_command.atSendCmdATraderSTGetAccountPosition(GVAR.g_ATraderRealHandles[HandleIdx[0]], GVAR.g_ATraderStraInputInfo.TargetList[t]['Market'], GVAR.g_ATraderStraInputInfo.TargetList[t]['Code'], LongShort)

        else:
            ToolBoxErrors.unexpect_switch_error('runmode')
    write_syslog('traderGetAccountPositionDirV2 Position {!r}, Frozen {!r}, AvgPrice {!r}'.format(Position, Frozen, AvgPrice), level='info', trace_debug=True)
    return (
     Position, Frozen, AvgPrice)


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetIdx_bool').is_instance_of((int, float, Iterable)), verify_that('ConfigArray').is_instance_of((int, float, Iterable)))
def traderConfigTo(HandleIdx, TargetIdx_bool, ConfigArray):
    """
    ConfigArray【-1<Config<1时为账户比率 -代表空头持仓，ConfigArray<=-1 ConfigArray>=-1表示持仓手数】
    """
    HandleIdx, _ = atCheckIdx('traderConfigTo', HandleIdx, None, toarray=False)
    write_syslog('traderConfigTo HandleIdx {!r}, TargetIdx_bool {!r}, Config {!r}'.format(HandleIdx, TargetIdx_bool, ConfigArray), level='info', trace_debug=True)
    if isinstance(TargetIdx_bool, (int, float)):
        TargetIdx_bool = [
         TargetIdx_bool]
    TargetIdx_bool = np.asarray(TargetIdx_bool).astype(np.bool).ravel()
    if isinstance(ConfigArray, (int, float)):
        ConfigArray = [
         ConfigArray]
    ConfigArray = np.asarray(ConfigArray)
    if GVAR.atBeInBackTestMode():
        GVAR.atEnterConfigurationOrderMode()
        GVAR.g_ATraderAccountConfigBarOper.append(dotdict({'HandleIdx': HandleIdx, 
         'TargetIdx': TargetIdx_bool, 
         'Config': ConfigArray}))
    elif GVAR.atBeInRealMode():
        if GVAR.g_ATraderRTAccountConfig.size < 1:
            GVAR.g_ATraderRTAccountConfig = np.zeros((
             len(GVAR.g_ATraderAccountHandleArray), len(GVAR.g_ATraderStraInputInfo.TargetList)))
        GVAR.g_ATraderRTAccountConfig[(HandleIdx, TargetIdx_bool)] = ConfigArray[TargetIdx_bool]
        TargetsList = [target for i, target in enumerate(GVAR.g_ATraderStraInputInfo.TargetList) if TargetIdx_bool[i]]
        tb_command.atSendCmdATraderAccountConfigTo(TargetsList, ConfigArray[TargetIdx_bool], GVAR.g_ATraderStrategyName, GVAR.g_ATraderRealHandles[HandleIdx])


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float, Iterable)), verify_that('TargetIdx').is_instance_of((int, float, Iterable)))
def traderGetAccountConfig(HandleIdx, TargetIdx):
    """或者配置矩阵前一根bar的信息"""
    HandleIdx, TargetIdx = atCheckIdx('traderGetAccountConfig', HandleIdx, TargetIdx, toarray=True)
    if GVAR.g_ATraderSimCurBarFresh > 1:
        Config = GVAR.g_ATraderAccountConfigMatrix[(HandleIdx, TargetIdx, GVAR.g_ATraderSimCurBarFresh - 1)]
        Config = Config.reshape(HandleIdx.size, TargetIdx.size)
    else:
        Config = np.zeros((len(HandleIdx), len(TargetIdx)))
    write_syslog('traderGetAccountConfig HandleIdx {!r}, TargetIdx {!r}, Config {!r}'.format(HandleIdx, TargetIdx, Config), level='info', trace_debug=True)
    return Config


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetOrderID').is_instance_of((int, float)), verify_that('StopGap').is_instance_of((int, float)), verify_that('StopType').is_stop_type(), verify_that('OrderCtg').is_oder_ctg())
def traderStopLossByOrderV2(HandleIdx, TargetOrderID, StopGap, StopType, OrderCtg, OrderTag):
    """根据订单下止损单，固定止损，返回为 numpy.nan 表示跟踪单无效"""
    ClientOrderID = np.nan
    HandleIdx, _ = atCheckIdx('traderStopLossByOrderV2', HandleIdx, None, toarray=False)
    if TargetOrderID < 0 or np.isnan(TargetOrderID):
        write_userlog(const_da.Enum_Const.ERROR_ORDERID.value, level='warn')
        return ClientOrderID
    write_syslog('traderStopLossByOrderV2 HandleIdx {!r}, TargetOrderID {!r}, StopGap {!r}, StopType {!r}, OrderCtg {!r}, OrderTag {!r}'.format(HandleIdx, TargetOrderID, StopGap, StopType, OrderCtg, OrderTag), level='info', trace_debug=True)
    ClientOrderID = atStopOrderV2(HandleIdx, 'loss', 0, TargetOrderID, 0, StopGap, StopType, 1, '', 0, '', OrderCtg, OrderTag)
    return ClientOrderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetOrderID').is_instance_of((int, float)), verify_that('StopGap').is_instance_of((int, float)), verify_that('StopType').is_stop_type(), verify_that('OrderCtg').is_oder_ctg())
def traderStopProfitByOrderV2(HandleIdx, TargetOrderID, StopGap, StopType, OrderCtg, OrderTag):
    """根据订单下止盈单，固定止盈，返回为 numpy.nan 表示跟踪单无效"""
    ClientOrderID = np.nan
    HandleIdx, _ = atCheckIdx('traderStopProfitByOrderV2', HandleIdx, None, toarray=False)
    if TargetOrderID < 0 or np.isnan(TargetOrderID):
        write_userlog(const_da.Enum_Const.ERROR_ORDERID.value, level='warn')
        return ClientOrderID
    write_syslog('traderStopProfitByOrderV2 HandleIdx {!r}, TargetOrderID {!r}, StopGap {!r}, StopType {!r}, OrderCtg {!r}, OrderTag {!r}'.format(HandleIdx, TargetOrderID, StopGap, StopType, OrderCtg, OrderTag), level='info', trace_debug=True)
    ClientOrderID = atStopOrderV2(HandleIdx, 'profit', 0, TargetOrderID, 0, StopGap, StopType, 1, '', 0, '', OrderCtg, OrderTag)
    return ClientOrderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('TargetOrderID').is_instance_of((int, float)), verify_that('StopGap').is_instance_of((int, float)), verify_that('StopType').is_stop_type(), verify_that('TrailingGap').is_instance_of((int, float)), verify_that('TrailingType').is_trailing_type(), verify_that('OrderCtg').is_oder_ctg())
def traderStopTrailingByOrderV2(HandleIdx, TargetOrderID, StopGap, StopType, TrailingGap, TrailingType, OrderCtg, OrderTag):
    """根据订单下跟踪止盈单，返回为 numpy.nan 表示跟踪单无效"""
    ClientOrderID = np.nan
    HandleIdx, _ = atCheckIdx('traderStopTrailingByOrderV2', HandleIdx, None, toarray=False)
    if TargetOrderID < 0 or np.isnan(TargetOrderID):
        write_userlog(const_da.Enum_Const.ERROR_ORDERID.value, level='warn')
        return ClientOrderID
    write_syslog('traderStopTrailingByOrderV2 HandleIdx {!r}, TargetOrderID {!r}, StopGap {!r}, StopType {!r}, TrailingGap {!r}, TrailingType {!r}, OrderCtg {!r}, OrderTag {!r}'.format(HandleIdx, TargetOrderID, StopGap, StopType, TrailingGap, TrailingType, OrderCtg, OrderTag), level='info', trace_debug=True)
    ClientOrderID = atStopOrderV2(HandleIdx, 'trailing', 0, TargetOrderID, 0, StopGap, StopType, TrailingGap, TrailingType, 0, '', OrderCtg, OrderTag)
    return ClientOrderID


@apply_rule(verify_that('HandleIdx').is_instance_of((int, float)), verify_that('OrderID').is_instance_of((int, float)))
def traderCancelOrderV2(HandleIdx, OrderID):
    HandleIdx, _ = atCheckIdx('traderCancelOrderV2', HandleIdx, None, toarray=False)
    if GVAR.atBeInBackTestMode():
        orderPos = np.where(GVAR.g_ATraderSimUnfilledOrders == OrderID)[0]
        if orderPos.size < 1 or GVAR.g_ATraderSimOrders[(GACV.SimOrder_OrderCtg, OrderID)] != GACV.OrderCtg_Limit:
            error_text = 'No such limit order'
            write_userlog(error_text, level='warn', console=error_text)
        else:
            GVAR.g_ATraderSimOrders[(GACV.SimOrder_Status, OrderID)] = GACV.OrderStatus_Cancelled
    else:
        if GVAR.atBeInRealMode():
            tb_command.atSendCmdCancelOrder(GVAR.g_ATraderStrategyName, GVAR.g_ATraderRealHandles[HandleIdx], OrderID)
        else:
            ToolBoxErrors.unexpect_switch_error('runmode')
    return OrderID