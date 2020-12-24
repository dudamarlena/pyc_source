# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\run_mode\run_mode_common.py
# Compiled at: 2018-08-27 20:45:24
# Size of source mod 2**32: 55109 bytes
import select
from datetime import datetime
import numpy as np, pandas as pd, atquant.api as api, atquant.at_algorithm.core_algorithm as CORE_ALGO, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR, atquant.socket_ctrl.tool_box_command as tb_command
from atquant.data.const_data import GACV
from atquant.utils.datetime_func import matlab_float_time_to_int_date
from atquant.utils.datetime_func import matlab_float_time_to_str_datetime
from atquant.utils.internal_exception import ToolBoxErrors
from atquant.utils.internal_util import append_or_assign_2d_array_axis0
from atquant.utils.logger import write_syslog
from atquant.utils.user_class import dotdict

def atRealTradeInitV2(TargetList, KFrequency, KFreNum, BeginDate, EndDate, FQ):
    """
    实盘模式开始刷新策略之前进行历史数据的组合与全局变量的设置
    :param mode:  "replay" or "real"
    """
    const_da.atDefineConst()
    GVAR.g_ATraderStraInputInfo = dotdict({'TargetList': TargetList, 
     'KFrequency': KFrequency, 
     'KFreNum': KFreNum, 
     'BeginDate': BeginDate, 
     'EndDate': EndDate, 
     'FQ': FQ, 
     'KFrequencyI': const_da.atStringToConst('KBaseFreq', KFrequency), 
     'FreshMatrixIdx': 0 if KFreNum == 1 else 1})
    api.traderAppendKDataScope(KFrequency, 0, False)
    GVAR.g_ATraderKDatas[0].baseMatrixPos = np.nan
    GVAR.g_ATraderKDatas[0].baseBegin = np.array([])
    GVAR.g_ATraderKDatas[0].baseEnd = np.array([])
    GVAR.g_ATraderKDatas[0].freComplete = np.array([])
    base0_matrix = GVAR.g_ATraderKDatas[0].Matrix
    if KFreNum == 1:
        GVAR.g_ATraderDataValueFresh = append_or_assign_2d_array_axis0(GVAR.g_ATraderDataValueFresh, base0_matrix[GACV.KMatrixPos_TimeLine], GACV.KMatrixPos_TimeLine)
        base0_matrix[GACV.KMatrixPos_FreshIdx] = np.ones([1, len(base0_matrix[GACV.KMatrixPos_FreshIdx])])
        GVAR.g_ATraderKDatas[0].CurrentBar = CORE_ALGO.atFillKMatrixFreshBar(GVAR.atGetBaseMx(0))
    else:
        idxFreshArray = CORE_ALGO.atCalculateReshIdxArray(base0_matrix, KFreNum)
        base0_matrix[GACV.KMatrixPos_FreshIdx] = idxFreshArray
        GVAR.g_ATraderDataValueFresh = append_or_assign_2d_array_axis0(GVAR.g_ATraderDataValueFresh, base0_matrix[(
         GACV.KMatrixPos_TimeLine, idxFreshArray)], GACV.KMatrixPos_TimeLine)
        GVAR.g_ATraderKDatas[0].CurrentBar = CORE_ALGO.atFillKMatrixFreshBar(GVAR.atGetBaseMx(0))
        api.traderRegKData(KFrequency, KFreNum)
    _mask = base0_matrix[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderRealTradeSaveFreshPositionInAppend)] <= GVAR.g_ATraderDataValueFresh[GACV.KMatrixPos_TimeLine]
    GVAR.g_ATraderRealTradeSaveFreshPosition = np.where(_mask)[0][0]
    api.init_set.atInitTargetInfo(float('nan'))
    tb_command.atSendCmdGetAccountInfo(GVAR.g_ATraderRealHandles.flatten())
    GVAR.g_ATraderKDatas[0].Matrix = base0_matrix


def atTradeLoopV2(TradeFun, varFunParameter, TargetList, KFrequency, KFreNum, AlgoTradeFunction):
    """实盘策略主循环"""
    if KFrequency == 'tick':
        atTickFresh(TradeFun, varFunParameter, TargetList, KFrequency, KFreNum, AlgoTradeFunction)
    else:
        atKFresh(TradeFun, varFunParameter, TargetList, KFrequency, KFreNum, AlgoTradeFunction)


def atTickFresh(TradeFun, varFunParameter, TargetList, KFrequency, KFreNum, AlgoTradeFunction):
    assert KFrequency.lower() == 'tick', 'KFrequency must be tick'
    GVAR.g_ATraderLastHeartBeat = datetime.now()
    GVAR.atSetATraderSimCurBarFresh(GVAR.g_ATraderRealTradeSaveFreshPosition)
    unfilledBeginCalcPos = np.array([item.CurrentBar[GVAR.g_ATraderSimCurBarFresh] for item in GVAR.g_ATraderKDatas])
    dailyStopFresh = False
    dayEnd = 0.625
    nightBegin = 0.875
    targetListLen = len(GVAR.g_ATraderStraInputInfo.TargetList)
    tickExistStatus = np.zeros((targetListLen, 1))
    if len(GVAR.g_ATraderKDatas) > 1:
        GVAR.g_ATraderOldMaxKTime = GVAR.g_ATraderKDatas[1].Matrix[(GACV.KMatrixPos_TimeLine, -1)]
    else:
        GVAR.g_ATraderOldMaxKTime = np.nan
    perbarLen = GVAR.atBarItemsLen()
    GVAR.g_ATraderLatestTick = GVAR.g_ATraderKDatas[0].Matrix[:, -1]
    _V = GACV.KMatrixPos_End + GACV.KMatrix_Volume + 1
    _T = GACV.KMatrixPos_End + GACV.KMatrix_TurnOver + 1
    GVAR.g_ATraderLatestTick[_V::perbarLen, -1] = 0
    GVAR.g_ATraderLatestTick[_T::perbarLen, -1] = 0
    tickFresh_Idx = 0
    tickFresh_IsBegin = 1
    tickFresh_Time = 2
    tickFresh_LastPrice = 3
    tickFresh_VolumeTick = 4
    tickFresh_Volume = 5
    tickFresh_TurnOver = 6
    tickFresh_OpenInt = 7
    while 1:
        heart_beat_elapsed_time = datetime.now() - GVAR.g_ATraderLastHeartBeat
        heart_beat_elapsed_time_seconds = heart_beat_elapsed_time.total_seconds()
        if heart_beat_elapsed_time_seconds >= 30:
            GVAR.g_ATraderSIDCB.reconnect_to_at()
            tb_command.atSendCmdSubscribeIns(TargetList, KFrequency)
            tb_command.atSendCmdSubscribeAcc(GVAR.g_ATraderRealHandles)
            tb_command.atSendCmdATraderKeepActive()
        else:
            if heart_beat_elapsed_time_seconds >= 10:
                tb_command.atSendCmdATraderKeepActive()
            inputs = [GVAR.g_ATraderSIDCB.client]
            outputs = []
            timeout = 0.01
            readable, writeable, exceptional = select.select(inputs, outputs, inputs, timeout)
            if not (readable or writeable or exceptional):
                continue
            else:
                rtFreshList, StopRun = tb_command.atGetAllSocketData()
            if StopRun:
                break
        if len(rtFreshList) < 1:
            pass
        else:
            sortIdx = np.argsort(rtFreshList[tickFresh_Time, :])
            rtFreshList = rtFreshList[:, sortIdx]
            for rtNum in range(rtFreshList.shape[1]):
                notExistTheTarget = not tickExistStatus[rtFreshList[(tickFresh_Idx, rtNum)]]
                if notExistTheTarget and np.sum(tickExistStatus) != targetListLen - 1:
                    tickExistStatus[rtFreshList[(tickFresh_Idx, rtNum)]] = True
                    GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, -1)] = np.max(GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, -1)], rtFreshList[(tickFresh_Time, rtNum)])
                    targetBasicLocation = GACV.KMatrixPos_End + (rtFreshList[(tickFresh_Idx, rtNum)] - 1) * perbarLen + 1
                    GVAR.g_ATraderLatestTick[targetBasicLocation + GACV.KMatrix_Open:GACV.KMatrix_Close + 1, -1] = rtFreshList[(tickFresh_LastPrice, rtNum)]
                    GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_Volume, -1)] = rtFreshList[(
                     tickFresh_VolumeTick, rtNum)]
                    GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_TurnOver, -1)] = rtFreshList[(
                     tickFresh_TurnOver, rtNum)]
                    GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_OpenInterest, -1)] = rtFreshList[(
                     tickFresh_OpenInt, rtNum)]
                else:
                    if notExistTheTarget:
                        GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, -1)] = np.max(GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, -1)], rtFreshList[(tickFresh_Time, rtNum)])
                        targetBasicLocation = GACV.KMatrixPos_End + (rtFreshList[(tickFresh_Idx, rtNum)] - 1) * perbarLen + 1
                        GVAR.g_ATraderLatestTick[targetBasicLocation + GACV.KMatrix_Open:GACV.KMatrix_Close + 1, -1] = rtFreshList[(tickFresh_LastPrice, rtNum)]
                        GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_Volume, -1)] = rtFreshList[(
                         tickFresh_VolumeTick, rtNum)]
                        GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_TurnOver, -1)] = rtFreshList[(
                         tickFresh_TurnOver, rtNum)]
                        GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_OpenInterest, -1)] = rtFreshList[(
                         tickFresh_OpenInt, rtNum)]
                    GVAR.g_ATraderLatestTick = np.append(GVAR.g_ATraderLatestTick, GVAR.g_ATraderLatestTick[:, -1], axis=1)
                    _V = GACV.KMatrixPos_End + GACV.KMatrix_Volume + 1
                    _T = GACV.KMatrixPos_End + GACV.KMatrix_TurnOver + 1
                    GVAR.g_ATraderLatestTick[_V::perbarLen, -1] = 0
                    GVAR.g_ATraderLatestTick[_T::perbarLen, -1] = 0
                    tickExistStatus = np.zeros((targetListLen, 1))
                    if notExistTheTarget:
                        continue
                    tickExistStatus[rtFreshList[(tickFresh_Idx, rtNum)]] = True
                    GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, -1)] = np.max(GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, -1)], rtFreshList[(tickFresh_Time, rtNum)])
                    targetBasicLocation = GACV.KMatrixPos_End + (rtFreshList[(tickFresh_Idx, rtNum)] - 1) * perbarLen + 1
                    GVAR.g_ATraderLatestTick[targetBasicLocation + GACV.KMatrix_Open:GACV.KMatrix_Close + 1, -1] = rtFreshList[(tickFresh_LastPrice, rtNum)]
                    GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_Volume, -1)] = rtFreshList[(
                     tickFresh_VolumeTick, rtNum)]
                    GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_TurnOver, -1)] = rtFreshList[(
                     tickFresh_TurnOver, rtNum)]
                    GVAR.g_ATraderLatestTick[(targetBasicLocation + GACV.KMatrix_OpenInterest, -1)] = rtFreshList[(
                     tickFresh_OpenInt, rtNum)]

            GVAR.g_ATraderLatestTick[GACV.KMatrixPos_FreshIdx, :] = True
            newTickBar = GVAR.g_ATraderLatestTick[:, 0:-1]
            GVAR.g_ATraderLatestTick = GVAR.g_ATraderLatestTick[:, -1]
            if newTickBar.size < 1:
                pass
            else:
                unfilledBeginCalcPos[0] = np.min(unfilledBeginCalcPos[0], GVAR.g_ATraderDataValueFresh.shape[1])
                maxTickTime = GVAR.g_ATraderLatestTick[(GVAR.KMatrixPos_TimeLine, -1)]
                if maxTickTime > GVAR.g_ATraderOldMaxKTime:
                    newMaxKTime = atTickExpandTimeLine(newTickBar, maxTickTime)
                else:
                    newMaxKTime = atTickExpandTimeLine(newTickBar)
                GVAR.g_ATraderOldMaxKTime = np.max(newMaxKTime, GVAR.g_ATraderOldMaxKTime)
                unfilledBeginCalcPos = atRecalculateKDataMatrix(GVAR.g_ATraderLatestTick[(GACV.KMatrixPos_TimeLine, 0)], unfilledBeginCalcPos)
                endFreshBar = GVAR.g_ATraderDataValueFresh.shape[1]
                atRecalculateDataValueFresh(GVAR.g_ATraderKDatas[0].CurrentBar[GVAR.g_ATraderSimCurBarFresh])
                atRealTradeCalculateUnfilledComplete(unfilledBeginCalcPos, endFreshBar)
                atRealTradeFreshCurBarIndi(endFreshBar - GVAR.g_ATraderSimCurBarFresh + 1)
        if GVAR.atBeInDataFreshMode():
            for freshNum in range(GVAR.g_ATraderSimCurBarFresh, endFreshBar + 1):
                barTime = GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderSimCurBarFresh)]
                if dailyStopFresh is True and barTime - np.floor(barTime) > dayEnd:
                    dailyStopFresh = False
                if dailyStopFresh is False and GVAR.atExistDailyCloseTimeSetting() and barTime - np.floor(barTime) >= GVAR.g_ATraderDailyCloseTime:
                    dailyStopFresh = True
                    for handleNum in range(len(GVAR.g_ATraderRealHandles)):
                        api.traderCloseAllV2(handleNum)

                Log = 'Run strategy timeline at %s ' % matlab_float_time_to_str_datetime(GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderSimCurBarFresh)])
                if Log != GVAR.g_ATraderLastLog:
                    api.traderPutLog(GVAR.g_ATraderRealHandles[0], GVAR.g_ATraderStrategyName, Log)
                    write_syslog(Log, trace_debug=True)
                    GVAR.g_ATraderLastLog = Log
                bDayBegin = True
                if 0 == GVAR.g_ATraderSimCurBarFresh:
                    preBar = -1
                else:
                    preBar = GVAR.g_ATraderKDatas[0].CurrentBar[(GVAR.g_ATraderSimCurBarFresh - 1)]
                curBar = GVAR.g_ATraderKDatas[0].CurrentBar[GVAR.g_ATraderSimCurBarFresh]
                if len(np.where(GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_DayPos, preBar + 1:curBar + 1] == 1)[0]) < 1:
                    bDayBegin = False
                if dailyStopFresh is False:
                    TradeFun(False, bDayBegin, varFunParameter)
                GVAR.g_ATraderSimCurBarFresh += 1


def atKFresh(TradeFun, varFunParameter, TargetList, KFrequency, KFreNum, AlgoTradeFunction):
    kFresh_Idx = 0
    kFresh_Time = 1
    kFresh_Open = 2
    kFresh_End = 8
    GVAR.g_ATraderLastHeartBeat = datetime.now()
    GVAR.atSetATraderSimCurBarFresh(GVAR.g_ATraderRealTradeSaveFreshPosition)
    unfilledBeginCalcPos = np.array([item.CurrentBar[GVAR.g_ATraderSimCurBarFresh] for item in GVAR.g_ATraderKDatas])
    unfilledBeginCalcPos[unfilledBeginCalcPos < 0] = 0
    dailyStopFresh = False
    dayEnd = 0.635416
    nightBegin = 0.875
    targetListLen = len(GVAR.g_ATraderStraInputInfo.TargetList)
    firstRunFilter = True
    while 1:
        heart_beat_elapsed_time = datetime.now() - GVAR.g_ATraderLastHeartBeat
        heart_beat_elapsed_time_seconds = heart_beat_elapsed_time.total_seconds()
        if heart_beat_elapsed_time_seconds >= 30:
            GVAR.g_ATraderSIDCB.reconnect_to_at()
            tb_command.atSendCmdSubscribeIns(TargetList, KFrequency)
            tb_command.atSendCmdSubscribeAcc(GVAR.g_ATraderRealHandles)
            tb_command.atSendCmdATraderKeepActive()
        else:
            if heart_beat_elapsed_time_seconds >= 10:
                tb_command.atSendCmdATraderKeepActive()
            inputs, outputs = [GVAR.g_ATraderSIDCB.client], []
            readable, writeable, exceptional = select.select(inputs, outputs, inputs, 0.01)
            if not (readable or writeable or exceptional):
                continue
            else:
                kFreshList, StopRun = tb_command.atGetAllSocketData()
            if StopRun:
                break
        if len(kFreshList) < 1:
            pass
        else:
            write_syslog('Receive kfresh data', matlab_float_time_to_str_datetime(kFreshList[kFresh_Time, :]), '\n', pd.DataFrame(kFreshList), 'DataValueFresh[TimeLine,-1]', matlab_float_time_to_str_datetime(GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, -1)]), trace_debug=True)
            assert np.all(kFreshList[kFresh_Idx] >= 0) and np.all(kFreshList[kFresh_Idx] < targetListLen)
            if not np.all(GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, -1)] >= kFreshList[kFresh_Time]):
                exceedTime = kFreshList[(kFresh_Time,
                 np.where(GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, -1)] < kFreshList[kFresh_Time])[0][0])]
                atMinuteExpandTimeLine(exceedTime)
                tempPos = GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, -1)] > kFreshList[kFresh_Time, :]
                if not np.all(tempPos):
                    tempT = kFreshList[(kFresh_Time, tempPos)]
                    err = 'Strategy Name：%s, Fatal time line error again for DataValueFresh last time: %s, KTime: %s' % (
                     GVAR.g_ATraderStrategyName,
                     matlab_float_time_to_str_datetime(GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, -1)]),
                     matlab_float_time_to_str_datetime(tempT))
                    raise Exception(err)
                minTargetTime = np.nan
                for targetIdx in range(targetListLen):
                    targetTime = kFreshList[(kFresh_Time, kFreshList[kFresh_Idx, :] == targetIdx)]
                    targetK = kFreshList[kFresh_Open:kFresh_End + 1, kFreshList[kFresh_Idx, :] == targetIdx]
                    if targetTime.size < 1:
                        pass
                    else:
                        timeExist, timeLoc = CORE_ALGO.ismember(targetTime, GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine, :])
                        targetTime, targetK = atRidNotAsecKData(timeExist, timeLoc, targetTime, targetK, targetIdx)
                        if targetTime.size < 1:
                            pass
                        else:
                            assert np.all(timeExist) and np.all(np.diff(timeLoc) >= 0), "Data Error, timeExist {!r}, timeLoc {!r} targetTime: {!r} is not in KDataMatrix0's time line".format(timeExist, timeLoc, matlab_float_time_to_str_datetime(targetTime))
                            minTargetTime = np.fmin(targetTime[0], minTargetTime)
                            _O = GVAR.atKMatixBarItemPos(GACV.KMatrix_Open, targetIdx, True)
                            _E = GVAR.atKMatixBarItemPos(GACV.KMatrix_Bar_End, targetIdx, True) + 1
                            GVAR.g_ATraderKDatas[0].Matrix[_O:_E, timeLoc] = targetK
                            targetK[GACV.KMatrix_Open:GACV.KMatrix_Low + 1, :] = np.tile(targetK[GACV.KMatrix_Close, :], (3,
                                                                                                                          1))
                            targetK[GACV.KMatrix_Volume:GACV.KMatrix_TurnOver + 1, :] = np.zeros((2, targetK.shape[1]))
                            for kNum in range(1, targetK.shape[1]):
                                shape_axis1 = timeLoc[kNum] - timeLoc[(kNum - 1)] - 1
                                if shape_axis1 > 0:
                                    GVAR.g_ATraderKDatas[0].Matrix[_O:_E, timeLoc[(kNum - 1)] + 1:timeLoc[kNum]] = np.tile(targetK[:, kNum - 1].reshape(-1, 1), (1, shape_axis1))

                    GVAR.g_ATraderKDatas[0].Matrix[_O:_E, timeLoc[(-1)] + 1:] = np.tile(targetK[:, -1].reshape(-1, 1), (
                     1, GVAR.g_ATraderKDatas[0].Matrix.shape[1] - timeLoc[(-1)] - 1))

                if np.isnan(minTargetTime):
                    pass
                else:
                    baseBeginPos = np.where(GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine, :] <= minTargetTime)[0]
                    assert baseBeginPos.size > 0, 'baseBeginPos.size need >0'
                    baseBeginTime = GVAR.g_ATraderKDatas[0].Matrix[(GACV.KMatrixPos_TimeLine, baseBeginPos[(-1)])]
                    unfilledBeginCalcPos[0] = np.fmin(unfilledBeginCalcPos[0], baseBeginPos[(-1)])
                    unfilledBeginCalcPos = atRecalculateKDataMatrix(baseBeginTime, unfilledBeginCalcPos)
                    unfilledBeginCalcPos[unfilledBeginCalcPos < 0] = 0
                    endFreshBar = np.where(GVAR.g_ATraderDataValueFresh[GACV.KMatrixPos_TimeLine, :] <= np.max(kFreshList[kFresh_Time, :]))[0][(-1)]
                    if endFreshBar < GVAR.g_ATraderSimCurBarFresh:
                        pass
                    else:
                        atRecalculateDataValueFresh(GVAR.g_ATraderKDatas[0].CurrentBar[GVAR.g_ATraderSimCurBarFresh])
                        unfilledBeginCalcPos = atRealTradeCalculateUnfilledComplete(unfilledBeginCalcPos, endFreshBar)
                        atRealTradeFreshCurBarIndi(endFreshBar - GVAR.g_ATraderSimCurBarFresh + 1)
                        if GVAR.atBeInDataFreshMode():
                            if firstRunFilter is True:
                                GVAR.atSetATraderSimCurBarFresh(endFreshBar)
                                firstRunFilter = False
                            for freshNum in range(GVAR.g_ATraderSimCurBarFresh, endFreshBar + 1):
                                barTime = GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderSimCurBarFresh)]
                                if dailyStopFresh is True and barTime - np.floor(barTime) > dayEnd:
                                    dailyStopFresh = False
                                if dailyStopFresh is False and GVAR.atExistDailyCloseTimeSetting() and barTime - np.floor(barTime) >= GVAR.g_ATraderDailyCloseTime:
                                    dailyStopFresh = True
                                    for handleNum in range(len(GVAR.g_ATraderRealHandles)):
                                        api.traderCloseAllV2(handleNum)

                                Log = 'FreshNum %d, Run strategy timeline at %s ' % (freshNum, matlab_float_time_to_str_datetime(barTime))
                                if Log != GVAR.g_ATraderLastLog:
                                    api.traderPutLog(GVAR.g_ATraderRealHandles[0], GVAR.g_ATraderStrategyName, Log)
                                    write_syslog(Log, trace_debug=True)
                                    GVAR.g_ATraderLastLog = Log
                                bDayBegin = True
                                if 0 == GVAR.g_ATraderSimCurBarFresh:
                                    preBar = -1
                                else:
                                    preBar = GVAR.g_ATraderKDatas[0].CurrentBar[(GVAR.g_ATraderSimCurBarFresh - 1)]
                                curBar = GVAR.g_ATraderKDatas[0].CurrentBar[GVAR.g_ATraderSimCurBarFresh]
                                if len(np.where(GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_DayPos, preBar + 1:curBar + 1] == 1)[0]) < 1:
                                    bDayBegin = False
                                if dailyStopFresh is False:
                                    TradeFun(False, bDayBegin, varFunParameter)
                                GVAR.g_ATraderSimCurBarFresh += 1


def atGetNewTimeLineAndDayPosition(newDate, freqArray, targetList, filterTime):
    arrayNewTradingTime = []
    for freq in freqArray:
        _freq = const_da.atConstToString('KBaseFreq', freq)
        moreTime, moreDayPos = api.traderGetTradingTime(targetList, _freq, newDate, 0)
        if moreTime.size < 1:
            err = 'Strategy Name: {!r}, [moreTime, moreDayPos] = traderGetTradingTime({!r},{!r},{!r}, 0), moreTime.size<1 timeline is empty'.format(GVAR.g_ATraderStrategyName, targetList, _freq, newDate)
            ToolBoxErrors.data_download_error(err)
        realMoreTimePos = np.where(moreTime > filterTime)[0]
        if realMoreTimePos.size < 1:
            err = 'Strategy Name: {!r}, [moreTime, moreDayPos] = traderGetTradingTime({!r},{!r},{!r}, 0), filterTime={!r}, moreTime > filterTime is empty'.format(GVAR.g_ATraderStrategyName, targetList, _freq, newDate, filterTime)
            raise Exception(err)
        else:
            realMoreTimePos = realMoreTimePos[0]
            moreTime = moreTime[realMoreTimePos:]
            moreDayPos = moreDayPos[realMoreTimePos:]
        arrayNewTradingTime.append(dotdict({'moreTime': moreTime, 
         'moreDayPos': moreDayPos}))

    return arrayNewTradingTime


def atTickExpandTimeLine(newTickBar, expandTime=None):
    assert newTickBar.size > 0
    newTickBarLen = newTickBar.shape[1]
    perbarLen = GVAR.atBarItemsLen()
    _O = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Open + 1
    _H = GACV.KMatrixPos_TimeLine + GACV.KMatrix_High + 1
    _L = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Low + 1
    _V = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Volume + 1
    _T = GACV.KMatrixPos_TimeLine + GACV.KMatrix_TurnOver + 1
    _C = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Close + 1
    repeatBase = GVAR.g_ATraderDataValueFresh[:, -1].reshape(-1, 1).copy()
    repeatBase[_O::perbarLen, :] = repeatBase[_C::perbarLen, :]
    repeatBase[_H::perbarLen, :] = repeatBase[_C::perbarLen, :]
    repeatBase[_L::perbarLen, :] = repeatBase[_C::perbarLen, :]
    repeatBase[_V::perbarLen, :] = 0
    repeatBase[_T::perbarLen, :] = 0
    GVAR.g_ATraderDataValueFresh = np.append(GVAR.g_ATraderDataValueFresh, np.tile(repeatBase, (1, newTickBarLen)), axis=1)
    GVAR.g_ATraderDataValueFresh[GACV.KMatrixPos_TimeLine, -newTickBarLen:] = newTickBar[GACV.KMatrixPos_TimeLine, :]
    GVAR.g_ATraderKDatas[0].Matrix = np.append(GVAR.g_ATraderKDatas[0].Matrix, newTickBar, axis=1)
    if len(GVAR.g_ATraderKDatas) >= 2:
        arrayTime = GVAR.g_ATraderKDatas[1].Matrix[GACV.KMatrixPos_TimeLine, :]
        bP = GVAR.g_ATraderKDatas[1].baseBegin
        eP = GVAR.g_ATraderKDatas[1].baseEnd
        highBLen = len(GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine, :])
        for pos in range(GVAR.g_ATraderKDatas[1].CurrentBar[(GVAR.g_ATraderSimCurBarFresh - 1)], len(bP) + 1):
            if pos > 0:
                if eP[(pos - 1)] + 1 < highBLen:
                    bP[pos] = eP[(pos - 1)] + 1
                else:
                    bP[pos] = eP[(pos - 1)]
                    eP[pos] = bP[pos]
                while GVAR.g_ATraderKDatas[0].Matrix[(GACV.KMatrixPos_TimeLine, eP[pos])] < arrayTime[pos] and eP[pos] < highBLen - 1:
                    eP[pos] += 1

                if GVAR.g_ATraderKDatas[0].Matrix[(GACV.KMatrixPos_TimeLine, eP[pos])] > arrayTime[pos] and eP[pos] > 0:
                    eP[pos] -= 1

        GVAR.g_ATraderKDatas[1].baseBegin = bP
        GVAR.g_ATraderKDatas[1].baseEnd = eP
    newMaxKTime = np.nan
    if expandTime is not None:
        unKDataMatrixFreq = np.unique([item.iFreq for item in GVAR.g_ATraderKDatas])
        arrayNewTradingTime = atGetNewTimeLineAndDayPosition(matlab_float_time_to_int_date(expandTime), unKDataMatrixFreq, GVAR.g_ATraderStraInputInfo.TargetList, GVAR.g_ATraderKDatas[1].Matrix[(
         GACV.KMatrixPos_TimeLine, -1)])
        atAppendNewTimeLineToKDataMatrix(True, unKDataMatrixFreq, arrayNewTradingTime)
        newMaxKTime = GVAR.g_ATraderKDatas[1].Matrix[(GACV.KMatrixPos_TimeLine, -1)]
    atUpdateRegKDataInfo(newTickBarLen)
    for kDataMatrixPos in range(len(GVAR.g_ATraderKDatas)):
        GVAR.g_ATraderKDatas[kDataMatrixPos].CurrentBar = CORE_ALGO.atFillKMatrixFreshBar(GVAR.atGetBaseMx(kDataMatrixPos))

    return newMaxKTime


def atRealTradeFreshCurBarIndi(freshLength):
    """实盘刷新用户计算因子函数"""
    for freshBar in range(GVAR.g_ATraderSimCurBarFresh, GVAR.g_ATraderSimCurBarFresh + freshLength):
        idxBegin = -1
        for calcNum in range(len(GVAR.g_ATraderRegIndiCalc)):
            F = GVAR.g_ATraderRegIndiCalc[calcNum]['F']
            args = GVAR.g_ATraderRegIndiCalc[calcNum]['cellPar']
            indiData = F(args[0], (
             GACV, freshBar, GVAR.g_ATraderDataValueFresh, GVAR.g_ATraderKDatas,
             GVAR.g_ATraderDataValueFreshUserD))
            if not isinstance(indiData, np.ndarray):
                indiData = np.asarray(indiData)
            if len(indiData.shape) != 2:
                indiData = indiData.reshape((-1, 1))
            indiNum, indiLen = indiData.shape
            assert not (indiLen > 1 and indiNum > 1), 'except function %s return value size > 1 got size=0' % F.__name__
            if indiLen > 1:
                indiData = indiData.T
                indiNum, indiLen = indiData.shape
            indiData = indiData.flatten().T
            row = GVAR.g_ATraderDataValueFreshUserD.shape[0]
            while freshBar >= GVAR.g_ATraderDataValueFreshUserD.shape[1]:
                GVAR.g_ATraderDataValueFreshUserD = np.append(GVAR.g_ATraderDataValueFreshUserD, np.array([np.nan] * row).reshape((-1,
                                                                                                                                   1)), axis=1)

            GVAR.g_ATraderDataValueFreshUserD[idxBegin + 1:idxBegin + indiNum + 1, freshBar] = indiData
            write_syslog('g_ATraderDataValueFreshUserD[{!r}:{!r}, {!r}]={!r}'.format(idxBegin + 1, idxBegin + indiNum + 1, freshBar, indiData), level='info', trace_debug=True)
            idxBegin = idxBegin + indiNum


def atRecalculateDataValueFresh(kMatrixUpdateBegin):
    ref_kmatrix0 = GVAR.g_ATraderKDatas[0].Matrix
    baseTimeLineLen = ref_kmatrix0[GACV.KMatrixPos_TimeLine, :].size
    targetListLen = len(GVAR.g_ATraderStraInputInfo.TargetList)
    perbarLen = GVAR.atBarItemsLen()
    _O = GVAR.atKMatixBarItemPos(GACV.KMatrix_Open, 0, True)
    _H = GVAR.atKMatixBarItemPos(GACV.KMatrix_High, 0, True)
    _L = GVAR.atKMatixBarItemPos(GACV.KMatrix_Low, 0, True)
    _C = GVAR.atKMatixBarItemPos(GACV.KMatrix_Close, 0, True)
    _V = GVAR.atKMatixBarItemPos(GACV.KMatrix_Volume, 0, True)
    _T = GVAR.atKMatixBarItemPos(GACV.KMatrix_TurnOver, 0, True)
    _I = GVAR.atKMatixBarItemPos(GACV.KMatrix_OpenInterest, 0, True)
    updatelen = baseTimeLineLen - kMatrixUpdateBegin
    for RegKDataPos in range(len(GVAR.g_ATraderRegKDataInfo)):
        CombinedMatrix = np.zeros((perbarLen * targetListLen, updatelen))
        ref_regkdata = GVAR.g_ATraderRegKDataInfo[RegKDataPos]
        for tmlNum in range(updatelen):
            tmlPos = kMatrixUpdateBegin + tmlNum
            t2 = ref_regkdata.beginPos[tmlPos]
            t3 = ref_regkdata.endPos[tmlPos] + 1
            CombinedMatrix[GACV.KMatrix_High::perbarLen, tmlNum] = np.max(ref_kmatrix0[_H::perbarLen, t2:t3], axis=1)
            CombinedMatrix[GACV.KMatrix_Low::perbarLen, tmlNum] = np.min(ref_kmatrix0[_L::perbarLen, t2:t3], axis=1)
            CombinedMatrix[GACV.KMatrix_Volume::perbarLen, tmlNum] = np.sum(ref_kmatrix0[_V::perbarLen, t2:t3], axis=1)
            CombinedMatrix[GACV.KMatrix_TurnOver::perbarLen, tmlNum] = np.sum(ref_kmatrix0[_T::perbarLen, t2:t3], axis=1)

        _t2 = ref_regkdata.beginPos[kMatrixUpdateBegin:baseTimeLineLen]
        CombinedMatrix[GACV.KMatrix_Open::perbarLen, :] = ref_kmatrix0[_O::perbarLen, _t2]
        _t2 = ref_regkdata.endPos[kMatrixUpdateBegin:baseTimeLineLen]
        CombinedMatrix[GACV.KMatrix_Close::perbarLen, :] = ref_kmatrix0[_C::perbarLen, _t2]
        _t2 = ref_regkdata.endPos[kMatrixUpdateBegin:baseTimeLineLen]
        CombinedMatrix[GACV.KMatrix_OpenInterest::perbarLen, :] = ref_kmatrix0[_I::perbarLen, _t2]
        _t1 = ref_regkdata.rowBegin
        _t2 = ref_regkdata.rowEnd + 1
        _t3 = int(np.sum(ref_kmatrix0[GACV.KMatrixPos_FreshIdx, kMatrixUpdateBegin:baseTimeLineLen]))
        _t4 = ref_kmatrix0[GACV.KMatrixPos_FreshIdx, kMatrixUpdateBegin:baseTimeLineLen].astype(np.bool)
        GVAR.g_ATraderDataValueFresh[_t1:_t2, -_t3:] = CombinedMatrix[:, _t4]


def atRealTradeCalculateUnfilledComplete(beginCalcalutePos, endFreshBar):
    targetListLen = len(GVAR.g_ATraderStraInputInfo.TargetList)
    for kDataMatrixPos in range(len(GVAR.g_ATraderKDatas)):
        ref_kdatas = GVAR.g_ATraderKDatas[kDataMatrixPos]
        beginPos = int(beginCalcalutePos[kDataMatrixPos])
        endPos = int(ref_kdatas.CurrentBar[endFreshBar])
        assert beginPos <= endPos, 'beginPos>endPos is error'
        newUnfilledBarRef, newUnfilledIdx = CORE_ALGO.atMatrixUnfillComplete(ref_kdatas.Matrix[:, beginPos:endPos + 1], GACV.KMatrixPos_End + 1, GVAR.atBarItemsLen())
        if beginPos == 0:
            for targetPos in range(targetListLen):
                if endPos + 1 <= len(ref_kdatas.UnfilledBarRef[targetPos]):
                    ref_kdatas.UnfilledBarRef[targetPos][beginPos:endPos + 1] = newUnfilledBarRef[targetPos]
                else:
                    ref_kdatas.UnfilledBarRef[targetPos] = np.append(ref_kdatas.UnfilledBarRef[targetPos][beginPos:], newUnfilledBarRef[targetPos])
                ref_kdatas.UnfilledIdx[targetPos] = newUnfilledIdx[targetPos]

        else:
            oldUnfilledBarRef = ref_kdatas.UnfilledBarRef
            oldUnfilledIdx = ref_kdatas.UnfilledIdx
            for targetPos in range(targetListLen):
                if np.isnan(newUnfilledBarRef[targetPos][0]):
                    _barrefpos = oldUnfilledBarRef[targetPos][beginPos]
                    _beginpos = beginPos
                else:
                    _barrefpos = oldUnfilledBarRef[targetPos][(beginPos - 1)]
                    _beginpos = beginPos - 1
                if np.isnan(_barrefpos):
                    ref_kdatas.UnfilledIdx[targetPos] = np.append(np.array([]), newUnfilledIdx[targetPos] + beginPos)
                else:
                    _barrefpos = int(_barrefpos)
                    ref_kdatas.UnfilledIdx[targetPos] = np.append(oldUnfilledIdx[targetPos][:_barrefpos], newUnfilledIdx[targetPos] + beginPos)
                _newunfilledbarref = newUnfilledBarRef[targetPos] + np.tile(oldUnfilledBarRef[targetPos][_beginpos], (
                 endPos - beginPos + 1,))
                ref_kdatas.UnfilledBarRef[targetPos] = np.append(ref_kdatas.UnfilledBarRef[targetPos][:beginPos], _newunfilledbarref)

        beginCalcalutePos[kDataMatrixPos] = endPos
        GVAR.g_ATraderKDatas[kDataMatrixPos] = ref_kdatas

    return beginCalcalutePos


def atMinuteExpandTimeLine(expandTime):
    """
    :param expandTime: numpy.ndarray(N)
    """
    unKDataMatrixFreq = np.unique([item.iFreq for item in GVAR.g_ATraderKDatas])
    arrayNewTradingTime = atGetNewTimeLineAndDayPosition(matlab_float_time_to_int_date(expandTime), unKDataMatrixFreq, GVAR.g_ATraderStraInputInfo.TargetList, GVAR.g_ATraderKDatas[0].Matrix[(GACV.KMatrixPos_TimeLine, -1)])
    freqPos = np.where(unKDataMatrixFreq == GVAR.g_ATraderStraInputInfo.KFrequencyI)[0][0]
    if 1 == GVAR.g_ATraderStraInputInfo.KFreNum:
        idxFreshArray = np.ones((arrayNewTradingTime[freqPos].moreTime.size,))
    else:
        idxFreshArray = np.mod(np.arange(1, arrayNewTradingTime[freqPos].moreDayPos.size + 1, 1), GVAR.g_ATraderStraInputInfo.KFreNum) == 0
        idxFreshArray[-1] = True
    perbarLen = GVAR.atBarItemsLen()
    _O = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Open + 1
    _H = GACV.KMatrixPos_TimeLine + GACV.KMatrix_High + 1
    _L = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Low + 1
    _V = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Volume + 1
    _T = GACV.KMatrixPos_TimeLine + GACV.KMatrix_TurnOver + 1
    _C = GACV.KMatrixPos_TimeLine + GACV.KMatrix_Close + 1
    repeatBase = GVAR.g_ATraderDataValueFresh[:, -1].reshape(-1, 1).copy()
    repeatBase[_O::perbarLen, :] = repeatBase[_C::perbarLen, :]
    repeatBase[_H::perbarLen, :] = repeatBase[_C::perbarLen, :]
    repeatBase[_L::perbarLen, :] = repeatBase[_C::perbarLen, :]
    repeatBase[_V::perbarLen, :] = 0
    repeatBase[_T::perbarLen, :] = 0
    sum_idxfresharray = int(np.sum(idxFreshArray))
    GVAR.g_ATraderDataValueFresh = np.append(GVAR.g_ATraderDataValueFresh, np.tile(repeatBase, (1, sum_idxfresharray)), axis=1)
    GVAR.g_ATraderDataValueFresh[GACV.KMatrixPos_TimeLine, -sum_idxfresharray:] = arrayNewTradingTime[freqPos].moreTime[idxFreshArray.astype(np.bool)]
    atAppendNewTimeLineToKDataMatrix(False, unKDataMatrixFreq, arrayNewTradingTime)
    freqPos = np.where(unKDataMatrixFreq == GVAR.g_ATraderKDatas[0].iFreq)[0][0]
    appendBaseTimeLen = arrayNewTradingTime[freqPos].moreTime.size
    GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_FreshIdx, -appendBaseTimeLen:] = idxFreshArray
    atUpdateRegKDataInfo(appendBaseTimeLen)


def atAppendNewTimeLineToKDataMatrix(bIsTickFreq, unKDataMatrixFreq, arrayNewTradingTime):
    """
    追加时间轴

    :param bIsTickFreq: bool, True是Tick数据，反之不是
    :param unKDataMatrixFreq: numpy.ndarray(N), g_ATraderKDatas中所有非重复的频率
    :param arrayNewTradingTime: 列表词典，具体内容参考：def atGetNewTimeLineAndDayPosition 函数的返回值
    """
    matrixBegin = 1 if bIsTickFreq else 0
    perbarLen = GVAR.atBarItemsLen()
    perbarHeadLen = GVAR.atBarHeadLen()
    _O = perbarHeadLen + GACV.KMatrix_Open
    _H = perbarHeadLen + GACV.KMatrix_High
    _L = perbarHeadLen + GACV.KMatrix_Low
    _V = perbarHeadLen + GACV.KMatrix_Volume
    _T = perbarHeadLen + GACV.KMatrix_TurnOver
    _C = perbarHeadLen + GACV.KMatrix_Close
    for kDataMatrixPos in range(matrixBegin, len(GVAR.g_ATraderKDatas)):
        bP, eP, freComplete = np.array([]), np.array([]), np.array([])
        if 1 == GVAR.g_ATraderKDatas[kDataMatrixPos].FreqNum:
            freqPos = np.where(unKDataMatrixFreq == GVAR.g_ATraderKDatas[kDataMatrixPos].iFreq)[0][0]
            appendColumnLength = arrayNewTradingTime[freqPos].moreTime.size
            repeatBase = GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[:, -1].reshape(-1, 1).copy()
            repeatBase[_O::perbarLen, :] = repeatBase[_C::perbarLen, :]
            repeatBase[_H::perbarLen, :] = repeatBase[_C::perbarLen, :]
            repeatBase[_L::perbarLen, :] = repeatBase[_C::perbarLen, :]
            repeatBase[_V::perbarLen, :] = 0
            repeatBase[_T::perbarLen, :] = 0
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix = np.append(GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix, np.tile(repeatBase, (1, appendColumnLength)), axis=1)
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[GACV.KMatrixPos_TimeLine, -appendColumnLength:] = arrayNewTradingTime[freqPos].moreTime
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[GACV.KMatrixPos_DayPos, -appendColumnLength:] = arrayNewTradingTime[freqPos].moreDayPos
            if not np.isnan(GVAR.g_ATraderKDatas[kDataMatrixPos].baseMatrixPos):
                arrayTime = GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[GACV.KMatrixPos_TimeLine, :]
                newTimeLineLen = arrayTime.size
                oldTimeLineLen = GVAR.g_ATraderKDatas[kDataMatrixPos].baseBegin.size
                bP = np.ones((newTimeLineLen,), dtype=np.int)
                eP = np.ones((newTimeLineLen,), dtype=np.int)
                bP[0:oldTimeLineLen] = GVAR.g_ATraderKDatas[kDataMatrixPos].baseBegin
                eP[0:oldTimeLineLen] = GVAR.g_ATraderKDatas[kDataMatrixPos].baseEnd
                higherFreqBase = GVAR.g_ATraderKDatas[kDataMatrixPos].baseMatrixPos
                highBLen = GVAR.g_ATraderKDatas[higherFreqBase].Matrix[GACV.KMatrixPos_TimeLine, :].size
                start_pos = 0 if oldTimeLineLen < 1 else oldTimeLineLen - 1
                for pos in range(start_pos, newTimeLineLen):
                    if pos > 0:
                        bP[pos] = eP[(pos - 1)] + 1
                        eP[pos] = bP[pos]
                    while GVAR.g_ATraderKDatas[higherFreqBase].Matrix[(GACV.KMatrixPos_TimeLine, eP[pos])] < arrayTime[pos] and eP[pos] < highBLen - 1:
                        eP[pos] += 1

                    if GVAR.g_ATraderKDatas[higherFreqBase].Matrix[(GACV.KMatrixPos_TimeLine, eP[pos])] > arrayTime[pos] and eP[pos] > 0:
                        eP[pos] -= 1

        else:
            baseMatrixPos = GVAR.g_ATraderKDatas[kDataMatrixPos].baseMatrixPos
            freqPos = np.where(unKDataMatrixFreq == GVAR.g_ATraderKDatas[kDataMatrixPos].iFreq)[0][0]
            baseExpandColumnLength = arrayNewTradingTime[freqPos].moreTime.size
            baseDayPos = GVAR.g_ATraderKDatas[baseMatrixPos].Matrix[GACV.KMatrixPos_DayPos, :]
            if GVAR.g_ATraderKDatas[baseMatrixPos].iFreq <= GACV.KFreq_Min:
                dayFinishPos = np.where(baseDayPos == 1)[0]
                dayFinishPos = dayFinishPos[(dayFinishPos - 1 >= 0)] - 1
                dayFinishPos = np.append(dayFinishPos, len(baseDayPos) - 1)
                freComplete = baseDayPos.copy()
                freComplete[dayFinishPos] = 0
                bP = np.ceil(baseDayPos / GVAR.g_ATraderKDatas[kDataMatrixPos].FreqNum)
                bpLastNum, bpLastPos = bP[0], 0
                for bpPos in range(len(bP)):
                    if bpLastNum == bP[bpPos]:
                        bP[bpPos] = bpLastPos
                    else:
                        bpLastNum, bpLastPos, bP[bpPos] = bP[bpPos], bpPos, bpPos

            else:
                freComplete = np.arange(1, len(baseDayPos) + 1)
                bP = np.ceil(np.arange(1, len(baseDayPos) + 1) / GVAR.g_ATraderKDatas[kDataMatrixPos].FreqNum)
            freComplete = np.mod(freComplete, GVAR.g_ATraderKDatas[kDataMatrixPos].FreqNum) == 0
            freComplete = freComplete[-baseExpandColumnLength:]
            appendColumnLength = np.sum(freComplete)
            eP = np.arange(len(baseDayPos))
            repeatBase = GVAR.g_ATraderKDatas[baseMatrixPos].Matrix[:, -1].reshape(-1, 1).copy()
            freComplete = freComplete.astype(np.bool)
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix = np.append(GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix, np.tile(repeatBase, (1, appendColumnLength)), axis=1)
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[GACV.KMatrixPos_TimeLine, -appendColumnLength:] = arrayNewTradingTime[freqPos].moreTime[freComplete]
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[GACV.KMatrixPos_DayPos, -appendColumnLength:] = arrayNewTradingTime[freqPos].moreDayPos[freComplete]
        GVAR.g_ATraderKDatas[kDataMatrixPos].baseBegin = bP
        GVAR.g_ATraderKDatas[kDataMatrixPos].baseEnd = eP
        GVAR.g_ATraderKDatas[kDataMatrixPos].freComplete = np.append(GVAR.g_ATraderKDatas[kDataMatrixPos].freComplete, freComplete)
        if bIsTickFreq is False:
            GVAR.g_ATraderKDatas[kDataMatrixPos].CurrentBar = CORE_ALGO.atFillKMatrixFreshBar(GVAR.atGetBaseMx(kDataMatrixPos))


def atUpdateRegKDataInfo(appendLen):
    baseTimeLineLen = GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine, :].size
    for RegKDataPos in range(len(GVAR.g_ATraderRegKDataInfo)):
        kMatrixPos = GVAR.g_ATraderRegKDataInfo[RegKDataPos].kMatrixPos
        CombinedLen = len(GVAR.g_ATraderKDatas[kMatrixPos].Matrix[GACV.KMatrixPos_TimeLine, :])
        targetTMPos = np.zeros((baseTimeLineLen,), dtype=np.int)
        bP = np.arange(baseTimeLineLen).astype(np.int)
        start_pos = baseTimeLineLen - appendLen - 1
        base0_tl = GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine]
        ref_tl = GVAR.g_ATraderKDatas[kMatrixPos].Matrix[GACV.KMatrixPos_TimeLine]
        for i in range(start_pos, baseTimeLineLen):
            freshTM = base0_tl[i]
            if i > 0:
                targetTMPos[i] = targetTMPos[(i - 1)]
            while targetTMPos[i] < CombinedLen - 1 and ref_tl[targetTMPos[i]] < freshTM:
                targetTMPos[i] += 1

            while bP[i] > 0 and targetTMPos[(bP[i] - 1)] == targetTMPos[i]:
                bP[i] -= 1

        GVAR.g_ATraderRegKDataInfo[RegKDataPos].beginPos = np.append(GVAR.g_ATraderRegKDataInfo[RegKDataPos].beginPos, bP[start_pos + 1:baseTimeLineLen])
        GVAR.g_ATraderRegKDataInfo[RegKDataPos].endPos = np.arange(baseTimeLineLen)


def atRecalculateKDataMatrix(baseBeginTime, unfilledBeginCalcPos):
    perbarLen = GVAR.atBarItemsLen()
    for kDataMatrixPos in range(1, len(GVAR.g_ATraderKDatas)):
        bP = GVAR.g_ATraderKDatas[kDataMatrixPos].baseBegin.astype(np.int)
        eP = GVAR.g_ATraderKDatas[kDataMatrixPos].baseEnd.astype(np.int)
        _O = GACV.KMatrixPos_End + GACV.KMatrix_Open + 1
        _H = GACV.KMatrixPos_End + GACV.KMatrix_High + 1
        _L = GACV.KMatrixPos_End + GACV.KMatrix_Low + 1
        _C = GACV.KMatrixPos_End + GACV.KMatrix_Close + 1
        _V = GACV.KMatrixPos_End + GACV.KMatrix_Volume + 1
        _T = GACV.KMatrixPos_End + GACV.KMatrix_TurnOver + 1
        _I = GACV.KMatrixPos_End + GACV.KMatrix_OpenInterest + 1
        if len(GVAR.g_ATraderKDatas[kDataMatrixPos].freComplete) > 0:
            ref_base_matrix = GVAR.g_ATraderKDatas[GVAR.g_ATraderKDatas[kDataMatrixPos].baseMatrixPos].Matrix
            beginPos = np.where(ref_base_matrix[GACV.KMatrixPos_TimeLine, :] <= baseBeginTime)[0][(-1)]
            CombinedMatrix = ref_base_matrix[:, beginPos:].copy()
            for pos in range(CombinedMatrix.shape[1]):
                basePos = beginPos + pos
                CombinedMatrix[_H::perbarLen, pos] = np.max(ref_base_matrix[_H::perbarLen, bP[basePos]:eP[basePos] + 1], axis=1)
                CombinedMatrix[_L::perbarLen, pos] = np.min(ref_base_matrix[_L::perbarLen, bP[basePos]:eP[basePos] + 1], axis=1)
                CombinedMatrix[_V::perbarLen, pos] = np.sum(ref_base_matrix[_V::perbarLen, bP[basePos]:eP[basePos] + 1], axis=1)
                CombinedMatrix[_T::perbarLen, pos] = np.sum(ref_base_matrix[_T::perbarLen, bP[basePos]:eP[basePos] + 1], axis=1)

            CombinedMatrix[_O::perbarLen, :] = ref_base_matrix[_O::perbarLen, bP[beginPos:]]
            CombinedMatrix[_C::perbarLen, :] = ref_base_matrix[_C::perbarLen, eP[beginPos:]]
            CombinedMatrix[_I::perbarLen, :] = ref_base_matrix[_I::perbarLen, eP[beginPos:]]
            _sum = np.sum(GVAR.g_ATraderKDatas[kDataMatrixPos].freComplete[beginPos:])
            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix[:, -_sum:] = CombinedMatrix[:,
             GVAR.g_ATraderKDatas[kDataMatrixPos].freComplete[beginPos:]]
            unfilledBeginCalcPos[kDataMatrixPos] = np.fmin(unfilledBeginCalcPos[kDataMatrixPos], np.sum(GVAR.g_ATraderKDatas[kDataMatrixPos].freComplete[:beginPos + 1]))
        else:
            ref_k_kmatrix = GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix
            higherFreqBase = GVAR.g_ATraderKDatas[kDataMatrixPos].baseMatrixPos
            higherBeginPos = np.where(ref_k_kmatrix[GACV.KMatrixPos_TimeLine, :] <= baseBeginTime)[0][(-1)]
            beginPos = np.where(bP <= higherBeginPos)[0][(-1)]
            ref_h_kmatrix = GVAR.g_ATraderKDatas[higherFreqBase].Matrix
            for pos in range(beginPos, ref_k_kmatrix.shape[1]):
                ref_k_kmatrix[_O::perbarLen, pos] = ref_h_kmatrix[_O::perbarLen, bP[pos]]
                ref_k_kmatrix[_H::perbarLen, pos] = np.max(ref_h_kmatrix[_H::perbarLen, bP[pos]:eP[pos] + 1], axis=1)
                ref_k_kmatrix[_L::perbarLen, pos] = np.min(ref_h_kmatrix[_L::perbarLen, bP[pos]:eP[pos] + 1], axis=1)
                ref_k_kmatrix[_C::perbarLen, pos] = ref_h_kmatrix[_C::perbarLen, eP[pos]]
                ref_k_kmatrix[_V::perbarLen, pos] = np.sum(ref_h_kmatrix[_V::perbarLen, bP[pos]:eP[pos] + 1], axis=1)
                ref_k_kmatrix[_T::perbarLen, pos] = np.sum(ref_h_kmatrix[_T::perbarLen, bP[pos]:eP[pos] + 1], axis=1)
                ref_k_kmatrix[_I::perbarLen, pos] = ref_h_kmatrix[_I::perbarLen, eP[pos]]

            GVAR.g_ATraderKDatas[kDataMatrixPos].Matrix = ref_k_kmatrix
            GVAR.g_ATraderKDatas[higherFreqBase].Matrix = ref_h_kmatrix
            unfilledBeginCalcPos[kDataMatrixPos] = np.fmin(unfilledBeginCalcPos[kDataMatrixPos], beginPos)

    return unfilledBeginCalcPos


def atRidNotAsecKData(timeExist, timeLoc, targetTime, targetK, targetIdx):
    """
    实盘或回放时，AT传输过来的数据，需要剔除非单增且不在历史矩阵中的时间线的时间点数据
    Exist and increase monotonically, same means more than one turn in the data list
    Erase the one does not meet
        
    :param timeExist: bool类型列表,记录值是否在时间线中
    :param timeLoc: int,记录值是在时间线中的位置
    :param targetTime: numpy.ndarray(N), AT传过来的 kFreshList中targetIdx的时间轴
    :param targetK: numpy.ndarray(7*N), AT传过来的 kFreshList中targetIdx的OHLCVT
    :return: targetTime,targetK
    """
    timeExist = np.asarray(timeExist, dtype=bool)
    timeLoc = np.asarray(timeLoc, dtype=np.int)
    if not np.all(timeExist) or not np.all(np.diff(timeLoc) >= 0):
        timeLocKeep = np.ones((len(timeExist),), dtype=np.bool)
        timeLocDiff = np.diff(timeLoc)
        for tPos in range(len(timeLocDiff)):
            if not not timeLocKeep[(tPos + 1)]:
                if timeLocDiff[tPos] >= 0:
                    pass
                else:
                    timeLocKeep[tPos + 1:] = timeLocKeep[tPos + 1:] & (timeLoc[tPos + 1:] >= timeLoc[tPos])

        timeKeep = timeExist & timeLocKeep
        wrongTime = targetTime[np.logical_not(timeKeep)]
        write_syslog('Wrong K data,StrategyName:{!r},targetIdx:{!r},targetTime:{!r},wrongTime{!r},timeExist{!r},timeLoc{!r}'.format(GVAR.g_ATraderStrategyName, targetIdx, matlab_float_time_to_str_datetime(targetTime), matlab_float_time_to_str_datetime(wrongTime), timeExist, timeLoc), level='warn', trace_debug=False)
        targetTime = targetTime[timeKeep]
        targetK = targetK[:, timeKeep]
    return (targetTime, targetK)