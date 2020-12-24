# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\run_mode\trader_run_back_test.py
# Compiled at: 2018-08-27 20:45:24
# Size of source mod 2**32: 46031 bytes
import datetime, os, traceback, types, scipy.io as sio, atquant.at_algorithm.core_algorithm as CORE_ALGO, atquant.socket_ctrl.tool_box_command as tb_command
from atquant import api
from atquant.account.account_checker import AccountChecker
from atquant.socket_ctrl import base_socket
from atquant.trade.back_test_trade import *
from atquant.utils.arg_checker import ArgumnetChecker, ATInvalidArgument
from atquant.utils.arg_checker import verify_that, apply_rule
from atquant.utils.datetime_func import change_to_y_M_D_H_m_s
from atquant.utils.datetime_func import check_begindate_enddate
from atquant.utils.datetime_func import matlab_float_time_to_str_date, matlab_float_time_to_datetime
from atquant.utils.internal_exception import ToolBoxErrors
from atquant.utils.internal_util import SimpleTimer
from atquant.utils.internal_util import append_or_assign_2d_array_axis0
from atquant.utils.internal_util import trace_time
from atquant.utils.logger import write_syslog, write_userlog
from atquant.utils.user_class import dotdict

@apply_rule(verify_that('StrategyName').is_instance_of(str), verify_that('TradeFun').is_instance_of(types.FunctionType), verify_that('varFunParameter').is_instance_of(tuple), verify_that('AccountList').is_instance_of(list).is_empty_or_not(empty=False), verify_that('TargetList').is_instance_of(list).is_empty_or_not(empty=False), verify_that('KFrequency').is_valid_frequency(), verify_that('KFreNum').is_instance_of(int).is_greater_or_equal_than(1), verify_that('BeginDate').is_valid_date(), verify_that('EndDate').is_valid_date(), verify_that('FQ').is_valid_fq())
def traderRunBacktestV2(StrategyName, TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, EndDate, FQ, *args):
    """
    主回测函数
    """
    try:
        try:
            write_syslog('Begin Prepare traderRunBacktestV2', level='info', trace_debug=True)
            TradeFun = trace_time(TradeFun)
            if GVAR.g_ATraderRegisterRealK:
                ToolBoxErrors.not_support_error(const_da.Enum_Const.ERROR_NOTSUPPORT_WHEN_REALMODE.value)
            if len(AccountList) > 1:
                raise ValueError(const_da.Enum_Const.ERROR_NOTSUPPORT_MULTI_ACCOUNT_BACKTESTMODE.value)
            ArgumnetChecker.is_algorithm_func_and_args(traderRunBacktestV2.__name__, *args)
            check_begindate_enddate(BeginDate, EndDate)
            AccountChecker.check_run_back_test_account(AccountList)
            TargetList = GVAR.atRemoveInvalidTarget(TargetList)
            GVAR.g_ATraderAccountOrderMode = 0
            GVAR.atResetAlgorithmTradeMode()
            GVAR.rm_root_sub_dir('record')
            if len(args) > 0:
                raise Exception('TODO it')
            GVAR.generatingStrategyName(StrategyName)
            base_socket.atClearAllTCPIP()
            mode = tb_command.atSendCmdGetCurMode()
            ToolBoxErrors.at_mode_error(mode, 'backtest')
            api.traderSetMarketOrderHoldingType(False)
        except ATInvalidArgument as e:
            write_userlog(traceback.format_exc(), level='error', console=traceback.format_exc())
            return
        except Exception as e:
            write_syslog(traceback.format_exc(), level='error', console=traceback.format_exc())
            return

    finally:
        write_syslog('End Prepare traderRunBacktestV2', level='info', trace_debug=True)

    try:
        try:
            use_time = SimpleTimer('traderRunBacktestV2', 'sec')
            GVAR.atResetRealMode()
            GVAR.atResetBackTestMode()
            GVAR.atResetAlgoOrderSignal()
            GVAR.atResetAlgorithmTradeMode()
            GVAR.atResetDailyCloseTimeSetting()
            GVAR.atResetOrderMode()
            GVAR.atSetBackTestFinished(True)
            tb_command.at_send_ATraderStartBackTest(TargetList, KFrequency, KFreNum, BeginDate, EndDate, GVAR.g_ATraderStrategyName)
            write_syslog('Begin StraRunInitV2', level='info', trace_debug=True)
            atStraRunInitV2(AccountList, TargetList, KFrequency, KFreNum, BeginDate, EndDate, FQ)
            write_syslog('End StraRunInitV2', level='info', trace_debug=True)
            write_syslog('Begin TradeFunInit', level='info', trace_debug=True)
            TradeFun(True, False, varFunParameter)
            write_syslog('End TradeFunInit', level='info', trace_debug=True)
            GVAR.atEnterBackTestMode()
            GVAR.atEnterDataFreshMode()
            write_syslog('Begin BackTestLoopV2', level='info', trace_debug=True)
            atBackTestLoopV2(TradeFun, varFunParameter)
            write_syslog('Begin BackTestLoopV2', level='info', trace_debug=True)
        except Exception as e:
            write_syslog(traceback.format_exc(), level='error', console=traceback.format_exc())

    finally:
        print('回测完毕, 正在处理绩效报告, 请稍等...')
        write_syslog('Begin Clean', level='info', trace_debug=True)
        clear_up()
        write_syslog('End Clean', level='info', trace_debug=True)
        msg = '回测总耗时 %d 秒' % use_time.total()
        write_userlog(msg, level='info', console=None)
        print(msg)


def atBackTestLoopV2(TradeFun, varFunParameter):
    curSimDay = 0
    for timeLineNum in range(GVAR.g_ATraderDataValueFresh.shape[1]):
        GVAR.atSetATraderSimCurBarFresh(timeLineNum)
        curFreshBartime = GVAR.g_ATraderDataValueFresh[(GACV.KMatrixPos_TimeLine, GVAR.g_ATraderSimCurBarFresh)]
        cD = int(np.floor(curFreshBartime))
        if curSimDay != cD:
            Log = 'Test day:%s' % datetime.datetime.fromordinal(cD - 366).strftime('%Y-%m-%d')
            tb_command.at_send_cmd_TraderPutLog(GVAR.g_ATraderAccountHandleArray[0], GVAR.g_ATraderStrategyName, Log)
            curSimDay = cD
        if GVAR.g_ATraderStraInputInfo.KFrequencyI <= GACV.KFreq_Min:
            if timeLineNum == 0:
                bDayBegin = True
                clearUnfilledOrder = True
            else:
                preBar = int(GVAR.g_ATraderKDatas[0].CurrentBar[(timeLineNum - 1)])
                curBar = int(GVAR.g_ATraderKDatas[0].CurrentBar[timeLineNum])
                _r = np.where(GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_DayPos, preBar + 1:curBar + 1] == 1)[0]
                _t = True if _r.size > 0 else False
                bDayBegin = _t
                clearUnfilledOrder = _t
        else:
            bDayBegin = True
            clearUnfilledOrder = False
        if timeLineNum > 0 and (GVAR.atBeInDirectOrderMode() or GVAR.atBeInUnsetOrderMode()):
            if clearUnfilledOrder:
                ClearUnfilledOrder()
            else:
                DealTrade()
            TradeFun(False, bDayBegin, varFunParameter)
            if GVAR.atBeInConfigurationOrderMode():
                DealTradeConfig()


def clear_up():
    """
    退出函数：如果遇异常可以保证AT不挂死，如果正常退出则返回交易结果  
    """
    normalFinished = GVAR.atIsBackTestNormalFinished()
    if normalFinished:
        try:
            if GVAR.atBeInDirectOrderMode() or GVAR.atBeInUnsetOrderMode():
                OrderTrans2()
            elif GVAR.atBeInConfigurationOrderMode():
                ConfigTrans()
        except Exception as e:
            write_syslog(traceback.format_exc(), level='error', console=str(e))

    try:
        tb_command.at_send_cmd_ATraderStopBackTest(normalFinished)
        GVAR.atResetBackTestMode()
        GVAR.atResetAlgorithmTradeMode()
        GVAR.atResetBackTestSetting()
        GVAR.atResetAlgoOrderSignal()
        GVAR.atResetDailyCloseTimeSetting()
        GVAR.g_ATraderOrderNum = 0
        GVAR.g_ATraderStopOrderNum = 0
        GVAR.g_ATraderAlgoOrderNum = 0
        GVAR.g_ATraderStopMode = 0
        GVAR.g_ATraderSimStopOrders = np.array([])
        GVAR.g_ATraderSimStopOrdersHolding = np.array([])
        GVAR.g_ATraderCurTickInfo = np.array([])
        GVAR.g_ATraderSimTrades = np.array([])
        GVAR.g_ATraderSimKDataValue = np.array([])
        GVAR.g_ATraderSimKDataKey = np.array([])
        GVAR.g_ATraderStraInputInfo.TargetList = []
        GVAR.g_ATraderDataValueFreshUserD = np.array([])
    except Exception as e:
        write_syslog(traceback.format_exc(), level='error', console=str(e))


def atStraRunInitV2(AccountList, TargetList, KFrequency, KFreNum, BeginDate, EndDate, FQ):
    """
    回测时初始化基础数据的主入口
    """
    const_da.atDefineConst()
    GVAR.g_ATraderStraInputInfo.TargetList = TargetList
    GVAR.g_ATraderStraInputInfo.KFrequency = KFrequency
    GVAR.g_ATraderStraInputInfo.KFreNum = KFreNum
    GVAR.g_ATraderStraInputInfo.BeginDate = BeginDate
    GVAR.g_ATraderStraInputInfo.EndDate = EndDate
    GVAR.g_ATraderStraInputInfo.FQ = FQ
    GVAR.g_ATraderStraInputInfo.KFrequencyI = const_da.atStringToConst('KBaseFreq', KFrequency)
    if GVAR.atExistBackTestSetting():
        InitialCash = GVAR.g_AtraderSetInfo.InitialCash
        Costfee = GVAR.g_AtraderSetInfo.Costfee
        GVAR.g_ATraderSlidePrice = GVAR.g_AtraderSetInfo.SlidePrice
        GVAR.g_ATraderPriceLoc = GVAR.g_AtraderSetInfo.PriceLoc
        GVAR.g_ATraderLimitType = GVAR.g_AtraderSetInfo.LimitType
    else:
        InitialCash = 10000000.0
        Costfee = float('nan')
        GVAR.g_ATraderSlidePrice = 0
        GVAR.g_ATraderLimitType = 0
        GVAR.g_ATraderPriceLoc = 1
    GVAR.g_ATraderStraInputInfo.FreshMatrixIdx = 0 if KFreNum == 1 else 1
    api.traderAppendKDataScope(KFrequency, 0, True)
    base0_matrix = GVAR.g_ATraderKDatas[0].Matrix
    if KFreNum == 1:
        _t = GACV.KMatrixPos_TimeLine
        GVAR.g_ATraderDataValueFresh = append_or_assign_2d_array_axis0(GVAR.g_ATraderDataValueFresh, base0_matrix[_t], _t)
        base0_matrix = append_or_assign_2d_array_axis0(base0_matrix, np.array([[1] * len(base0_matrix[_t])]), GACV.KMatrixPos_FreshIdx)
        GVAR.g_ATraderKDatas[0].CurrentBar = CORE_ALGO.atFillKMatrixFreshBar(GVAR.atGetBaseMx(0))
        GVAR.g_ATraderKDatas[0].Matrix = base0_matrix
    else:
        idxFreshArray = CORE_ALGO.atCalculateReshIdxArray(base0_matrix, KFreNum)
        GVAR.g_ATraderDataValueFresh = append_or_assign_2d_array_axis0(GVAR.g_ATraderDataValueFresh, base0_matrix[(GACV.KMatrixPos_TimeLine, idxFreshArray)], GACV.KMatrixPos_TimeLine)
        base0_matrix = append_or_assign_2d_array_axis0(base0_matrix, idxFreshArray.astype(np.int), GACV.KMatrixPos_FreshIdx)
        GVAR.g_ATraderKDatas[0].CurrentBar = CORE_ALGO.atFillKMatrixFreshBar(GVAR.atGetBaseMx(0))
        GVAR.g_ATraderKDatas[0].Matrix = base0_matrix
        api.traderRegKData(KFrequency, KFreNum)
    api.init_set.atInitTargetInfo(Costfee)
    GVAR.g_ATraderAccountMatrix = np.zeros((len(GVAR.g_ATraderAccountHandleArray),
     len(GVAR.g_ATraderStraInputInfo.TargetList) + 1,
     GVAR.atACItemsLen()))
    GVAR.g_ATraderAccountMatrix[:, 0, GACV.ACMatrix_ValidCash] = InitialCash
    GVAR.g_ATraderAccountMatrix[:, 0, GACV.ACMatrix_OrderFrozen] = 0
    GVAR.g_ATraderAccountMatrix[:, 0, GACV.ACMatrix_MarginFrozen] = 0
    GVAR.g_ATraderAccountConfigMatrix = np.zeros((len(GVAR.g_ATraderAccountHandleArray),
     len(GVAR.g_ATraderStraInputInfo.TargetList),
     len(GVAR.g_ATraderDataValueFresh[GACV.KMatrixPos_TimeLine])))


def OrderTrans2():
    """
    将所有的下单记录，以及成交记录，止盈止损单记录，存贮在本地文件中，提供给AT进行分析
    """
    record_dir = GVAR.cls_root_sub_dir('record')

    def _MC(index):
        return (
         GVAR.g_ATraderStraInputInfo.TargetList[index]['Market'],
         GVAR.g_ATraderStraInputInfo.TargetList[index]['Code'])

    def _PATH(index, suffix):
        market, code = _MC(index)
        _t = '%s_%s_%s.mat' % (market, code, suffix)
        _path = os.path.join(record_dir, _t)
        return _path

    temp_dict = dotdict({'allmxOrderTargetIdx': np.array([]), 
     'allmxOrderID': np.array([]), 
     'allmxOrderStatus': np.array([]), 
     'allmxOrderTime': np.array([]), 
     'allmxOrderFilledTime': np.array([]), 
     'allmxOrderContract': np.array([]), 
     'allmxOrderPrice': np.array([]), 
     'allmxOrderCtg': np.array([]), 
     'allmxOrderAct': np.array([]), 
     'allmxOrderOffsetFlag': np.array([])})
    if GVAR.g_ATraderSimOrders.size > 0:
        temp_dict.allmxOrderTargetIdx = GVAR.g_ATraderSimOrders[GACV.SimOrder_TargetIdx]
        temp_dict.allmxOrderID = GVAR.g_ATraderSimOrders[GACV.SimOrder_OrderID] + 1
        temp_dict.allmxOrderStatus = GVAR.g_ATraderSimOrders[GACV.SimOrder_Status]
        temp_dict.allmxOrderTime = change_inttime_to_y_M_D_H_m_s(GVAR.g_ATraderSimOrders[GACV.SimOrder_OrderTime])
        temp_dict.allmxOrderFilledTime = change_inttime_to_y_M_D_H_m_s(GVAR.g_ATraderSimOrders[GACV.SimOrder_FilledTime])
        temp_dict.allmxOrderContract = GVAR.g_ATraderSimOrders[GACV.SimOrder_Contracts]
        temp_dict.allmxOrderPrice = GVAR.g_ATraderSimOrders[GACV.SimOrder_Price]
        temp_dict.allmxOrderCtg = GVAR.g_ATraderSimOrders[GACV.SimOrder_OrderCtg]
        temp_dict.allmxOrderAct = GVAR.g_ATraderSimOrders[GACV.SimOrder_OrderAct]
        temp_dict.allmxOrderOffsetFlag = GVAR.g_ATraderSimOrders[GACV.SimOrder_OffsetFlag]
    file_name = os.path.join(record_dir, 'orders.mat')
    sio.savemat(file_name, temp_dict)
    temp_dict = dotdict({'allmxTradeTargetIdx': np.array([]), 
     'allmxTradeID': np.array([]), 
     'allmxTradeTime': np.array([]), 
     'allmxTradeContract': np.array([]), 
     'allmxTradePrice': np.array([]), 
     'allmxTradeCtg': np.array([]), 
     'allmxTradeAct': np.array([]), 
     'allmxTradeOffsetFlag': np.array([])})
    if GVAR.g_ATraderSimTrades.size > 0:
        temp_dict.allmxTradeTargetIdx = GVAR.g_ATraderSimTrades[GACV.SimTrade_TargetIdx]
        temp_dict.allmxTradeID = GVAR.g_ATraderSimTrades[GACV.SimTrade_OrderID] + 1
        temp_dict.allmxTradeTime = change_inttime_to_y_M_D_H_m_s(GVAR.g_ATraderSimTrades[GACV.SimTrade_FilledTime])
        temp_dict.allmxTradeContract = GVAR.g_ATraderSimTrades[GACV.SimTrade_Contracts]
        temp_dict.allmxTradePrice = GVAR.g_ATraderSimTrades[GACV.SimTrade_Price]
        temp_dict.allmxTradeCtg = GVAR.g_ATraderSimTrades[GACV.SimTrade_OrderCtg]
        temp_dict.allmxTradeAct = GVAR.g_ATraderSimTrades[GACV.SimTrade_OrderAct]
        temp_dict.allmxTradeOffsetFlag = GVAR.g_ATraderSimTrades[GACV.SimTrade_OffsetFlag]
    file_name = os.path.join(record_dir, 'trades.mat')
    sio.savemat(file_name, temp_dict)
    temp_dict = dotdict({'allmxSOTargetIdx': np.array([]), 
     'allmxSOStatus': np.array([]), 
     'allmxSOStopOrderType': np.array([]), 
     'allmxSOStopType': np.array([]), 
     'allmxSOTrailingType': np.array([]), 
     'allmxSOOrderAct': np.array([]), 
     'allmxSOOrderCtg': np.array([]), 
     'allmxSOTargetID': np.array([]), 
     'allmxSOClientID': np.array([]), 
     'allmxSOTargetPrice': np.array([]), 
     'allmxSOTrailingHigh': np.array([]), 
     'allmxSOTrailingLow': np.array([]), 
     'allmxSOEntryTime': np.array([]), 
     'allmxSOFireTime': np.array([]), 
     'allmxSOStopGap': np.array([]), 
     'allmxSOTrailingGap': np.array([]), 
     'allmxSOContracts': np.array([]), 
     'allmxSOBeginTrailingPrice': np.array([]), 
     'allmxSOStopTrailingPrice': np.array([]), 
     'allmxSOMPrice': np.array([])})
    if GVAR.g_ATraderSimStopOrders.size > 0:
        temp_dict.allmxSOTargetIdx = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TargetIdx]
        temp_dict.allmxSOStatus = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_Status]
        temp_dict.allmxSOStopOrderType = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_StopOrderType]
        temp_dict.allmxSOStopType = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_StopGapType]
        temp_dict.allmxSOTrailingType = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TrailingType]
        temp_dict.allmxSOOrderAct = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_OrderAct]
        temp_dict.allmxSOOrderCtg = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_OrderCtg]
        temp_dict.allmxSOClientID = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_ClientID]
        temp_dict.allmxSOTargetID = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TargetOrderID]
        temp_dict.allmxSOTargetPrice = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TargetPrice]
        temp_dict.allmxSOTrailingHigh = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TrailingHigh]
        temp_dict.allmxSOTrailingLow = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TrailingLow]
        temp_dict.allmxSOEntryTime = change_inttime_to_y_M_D_H_m_s(GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_EntryTime])
        temp_dict.allmxSOFireTime = change_inttime_to_y_M_D_H_m_s(GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_FireTime])
        temp_dict.allmxSOStopGap = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_StopGap]
        temp_dict.allmxSOTrailingGap = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_TrailingGap]
        temp_dict.allmxSOContracts = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_Contracts]
        temp_dict.allmxSOBeginTrailingPrice = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_BeginTrailingPrice]
        temp_dict.allmxSOStopTrailingPrice = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_StopTrailingPrice]
        temp_dict.allmxSOMPrice = GVAR.g_ATraderSimStopOrders[GACV.SimStopOrder_MPrice]
    file_name = os.path.join(record_dir, 'stoporders.mat')
    sio.savemat(file_name, temp_dict)
    df = api.traderGetTargetInfoV2(0)
    temp_dict = dotdict({'Margin': np.array([]), 
     'Multiple': np.array([]), 
     'InitialCash': np.array([]), 
     'Costfee': np.array([]), 
     'Rate': np.array([]), 
     'SlidePrice': np.array([]), 
     'InitialCash': GVAR.g_AtraderSetInfo.get('InitialCash', 10000000.0) + 0.0, 
     'Costfee': GVAR.g_AtraderSetInfo.get('Costfee', df.loc[('TradingFeeOpen', 0)]), 
     'Rate': GVAR.g_AtraderSetInfo.get('Rate', 0.02), 
     'SlidePrice': GVAR.g_AtraderSetInfo.get('SlidePrice', 0), 
     'Margin': df.loc[('LongMargin', 0)], 
     'Multiple': df.loc[('Multiple', 0)]})
    file_name = os.path.join(record_dir, 'Info.mat')
    sio.savemat(file_name, temp_dict)


def ConfigTrans():
    """记录配置下单矩阵传回给at"""
    GVAR.cls_root_sub_dir('record')
    record_dir = GVAR.root_sub_dir('record')
    mxTimeLine = change_inttime_to_y_M_D_H_m_s(GVAR.g_ATraderDataValueFresh[GACV.KMatrixPos_TimeLine])
    temp_dict = {'mxTimeLine': mxTimeLine}
    file_name = os.path.join(record_dir, 'config_timeline.mat')
    sio.savemat(file_name, temp_dict)
    targetsLen = len(GVAR.g_ATraderStraInputInfo.TargetList)
    _matrix = GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx].Matrix
    temp_dict = dotdict({'mxTarget': np.empty((targetsLen,), dtype=np.object), 
     'mxConfig': np.empty((targetsLen,), dtype=np.object), 
     'mxOpen': np.empty((targetsLen,), dtype=np.object), 
     'mxHigh': np.empty((targetsLen,), dtype=np.object), 
     'mxLow': np.empty((targetsLen,), dtype=np.object), 
     'mxClose': np.empty((targetsLen,), dtype=np.object)})
    for i in range(targetsLen):
        temp_dict.mxTarget[i] = '%s_%s' % (GVAR.g_ATraderStraInputInfo.TargetList[i]['Market'],
         GVAR.g_ATraderStraInputInfo.TargetList[i]['Code'])
        temp_dict.mxConfig[i] = np.array(GVAR.g_ATraderAccountConfigMatrix[0, i, :]).reshape(1, -1)
        temp_dict.mxOpen[i] = _matrix[GVAR.atKMatixBarItemPos(GACV.KMatrix_Open, i, contain_head=True)]
        temp_dict.mxHigh[i] = _matrix[GVAR.atKMatixBarItemPos(GACV.KMatrix_High, i, contain_head=True)]
        temp_dict.mxLow[i] = _matrix[GVAR.atKMatixBarItemPos(GACV.KMatrix_Low, i, contain_head=True)]
        temp_dict.mxClose[i] = _matrix[GVAR.atKMatixBarItemPos(GACV.KMatrix_Close, i, contain_head=True)]

    file_name = os.path.join(record_dir, 'configs.mat')
    sio.savemat(file_name, temp_dict)
    if GVAR.g_AtraderSetInfo:
        InitialCash = GVAR.g_AtraderSetInfo['InitialCash']
        Rate = GVAR.g_AtraderSetInfo['Rate']
        SlidePrice = GVAR.g_AtraderSetInfo['SlidePrice']
    else:
        InitialCash = 100000000
        Rate = 0.02
        SlidePrice = 0
    file_name = os.path.join(record_dir, 'Info.mat')
    sio.savemat(file_name, {'InitialCash': InitialCash, 'Rate': Rate, 'SlidePrice': SlidePrice})


def DealTradeConfig():
    """处理配置交易的逻辑"""
    if GVAR.g_ATraderAccountConfigMatrix.size > 0 and GVAR.g_ATraderSimCurBarFresh > 0:
        GVAR.g_ATraderAccountConfigMatrix[:, :, GVAR.g_ATraderSimCurBarFresh] = GVAR.g_ATraderAccountConfigMatrix[:, :, GVAR.g_ATraderSimCurBarFresh - 1]
    if len(GVAR.g_ATraderAccountConfigBarOper) > 0:
        temp_bar_fresh = GVAR.g_ATraderSimCurBarFresh
        global_config_operation = GVAR.g_ATraderAccountConfigBarOper
        for i in range(len(GVAR.g_ATraderAccountConfigBarOper)):
            setTarget = GVAR.g_ATraderAccountConfigBarOper[i]['TargetIdx'] == 1
            if np.sum(setTarget) == 0:
                continue
            temp_handle = GVAR.g_ATraderAccountConfigBarOper[i]['HandleIdx']
            GVAR.g_ATraderAccountConfigMatrix[(temp_handle, setTarget, temp_bar_fresh)] = global_config_operation[i]['Config'][setTarget]

        GVAR.g_ATraderAccountConfigBarOper = []


def JudgeStopOrdersByBar(barHigh, barLow, Position, sameTargetStopOrdersPos):
    """
    :param barHigh: 
    :param barLow: 
    :param Position: float,持仓量
    :param sameTargetStopOrdersPos: numpy.ndarray
    :return:  
    """
    mayFirePos = np.array([], dtype=np.int)
    mustTickCheckPos = np.array([], dtype=np.int)
    cancelledStopOrderPos = []
    for stopOrderPos in sameTargetStopOrdersPos:
        stopOrderPos = int(stopOrderPos)
        if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, stopOrderPos)] == GACV.StopOrderStatus_PreHolding:
            pass
        elif Position == 0:
            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_Status, stopOrderPos)] = GACV.StopOrderStatus_Cancelled
            _t = GVAR.g_ATraderSimUnfiredStopOrders[:, stopOrderPos].reshape((-1, 1))
            GVAR.g_ATraderSimStopOrders = UTILS_UTIL.append_or_assign_2d_array_axis1(GVAR.g_ATraderSimStopOrders, _t, GVAR.g_ApendEnoughConstNum)
            cancelledStopOrderPos.append(stopOrderPos)
            continue
        orderAct = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderPos)])
        _type = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopOrderType, stopOrderPos)])
        if _type == GACV.StopOrderType_Loss:
            if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderPos)] == GACV.OrderAct_Buy:
                if barLow <= GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderPos)]:
                    mayFirePos = np.append(mayFirePos, [stopOrderPos], axis=0)
            elif GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderPos)] == GACV.OrderAct_Sell and barHigh >= GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderPos)]:
                mayFirePos = np.append(mayFirePos, [stopOrderPos], axis=0)
        else:
            if _type == GACV.StopOrderType_Profit:
                if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderPos)] == GACV.OrderAct_Buy:
                    if barHigh >= GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderPos)]:
                        mayFirePos = np.append(mayFirePos, [stopOrderPos], axis=0)
                elif GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, stopOrderPos)] == GACV.OrderAct_Sell and barLow <= GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, stopOrderPos)]:
                    mayFirePos = np.append(mayFirePos, [stopOrderPos], axis=0)
            elif _type == GACV.StopOrderType_Trailing:
                beginTrailingPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_BeginTrailingPrice, stopOrderPos)]
                stopGapType = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGapType, stopOrderPos)]
                stopGap = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGap, stopOrderPos)]
                targetPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetPrice, stopOrderPos)]
                if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_IsBeginTrailing, stopOrderPos)] == 0:
                    if orderAct == GACV.OrderAct_Buy and barHigh >= beginTrailingPrice or orderAct == GACV.OrderAct_Sell and barLow <= beginTrailingPrice:
                        if GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBarBegin, stopOrderPos)] == 0:
                            mustTickCheckPos = np.append(mustTickCheckPos, [stopOrderPos], axis=0)
                            continue
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_IsBeginTrailing, stopOrderPos)] = True
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, stopOrderPos)] = True
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)] = beginTrailingPrice
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)] = beginTrailingPrice
                            if orderAct == GACV.OrderAct_Buy:
                                basePrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)]
                                stopGapDirection = -1
                            else:
                                if orderAct == GACV.OrderAct_Sell:
                                    basePrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)]
                                    stopGapDirection = 1
                                elif not False:
                                    raise AssertionError
                            if stopGapType == GACV.StopGapType_Point:
                                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)] = basePrice + stopGapDirection * stopGap
                            else:
                                if stopGapType == GACV.StopGapType_Percent:
                                    temp_stopGap = stopGap / 100.0
                                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)] = (1 - temp_stopGap) * basePrice + temp_stopGap * targetPrice
                                elif not False:
                                    raise AssertionError
                        else:
                            continue
                        if orderAct == GACV.OrderAct_Buy:
                            if barHigh > GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)]:
                                if stopGapType == GACV.StopGapType_Point:
                                    tempStopTrailingPrice = barHigh - stopGap
                                else:
                                    if stopGapType == GACV.StopGapType_Percent:
                                        tempStopTrailingPrice = barHigh - (barHigh - targetPrice) * stopGap / 100.0
                                    elif not False:
                                        raise AssertionError
                                if barLow <= tempStopTrailingPrice:
                                    mustTickCheckPos = np.append(mustTickCheckPos, [stopOrderPos], axis=0)
                                    continue
                                else:
                                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)] = barHigh
                                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)] = tempStopTrailingPrice
                            else:
                                if barLow <= GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)]:
                                    if bool(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, stopOrderPos)]):
                                        mustTickCheckPos = np.append(mustTickCheckPos, [stopOrderPos], axis=0)
                                    else:
                                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)] = min(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)], GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)])
                                        mayFirePos = np.append(mayFirePos, [stopOrderPos], axis=0)
                                        continue
                                if barLow < GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)]:
                                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)] = barLow
                        else:
                            if orderAct == GACV.OrderAct_Sell:
                                if barLow < GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)]:
                                    if stopGapType == GACV.StopGapType_Point:
                                        tempStopTrailingPrice = barLow + stopGap
                                    else:
                                        if stopGapType == GACV.StopGapType_Percent:
                                            tempStopTrailingPrice = barLow + (targetPrice - barLow) * stopGap / 100.0
                                        elif not False:
                                            raise AssertionError
                                    if barHigh >= tempStopTrailingPrice:
                                        mustTickCheckPos = np.append(mustTickCheckPos, [stopOrderPos], axis=0)
                                        continue
                                    else:
                                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, stopOrderPos)] = barHigh
                                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)] = tempStopTrailingPrice
                                else:
                                    if barHigh >= GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)]:
                                        if bool(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, stopOrderPos)]):
                                            mustTickCheckPos = np.append(mustTickCheckPos, [stopOrderPos], axis=0)
                                        else:
                                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)] = max(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)], GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, stopOrderPos)])
                                            mayFirePos = np.append(mayFirePos, [stopOrderPos], axis=0)
                                            continue
                                    if barHigh > GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)]:
                                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, stopOrderPos)] = barHigh
                            elif not False:
                                raise AssertionError
                    else:
                        if not False:
                            raise AssertionError

    GVAR.g_ATraderSimUnfiredStopOrders = np.delete(GVAR.g_ATraderSimUnfiredStopOrders, np.asarray(cancelledStopOrderPos, dtype=np.int), axis=1)
    return (mayFirePos, mustTickCheckPos)


def JudgeStopOrdersByTick(stopOrdersPos):
    """
    :param stopOrdersPos: 包含多个止盈止损的订单索引
    :return: theFireOnePos(N,), tickBarOpen(N,), tickBarHigh(N,), tickBarLow(N,), tickBarVol(N,)
    """
    theFireOnePos = np.array([])
    tickBarOpen = np.array([])
    tickBarHigh = np.array([])
    tickBarLow = np.array([])
    tickBarVol = np.array([])
    _idx = GVAR.g_ATraderStraInputInfo.FreshMatrixIdx
    curbarfresh = GVAR.g_ATraderKDatas[_idx].CurrentBar[GVAR.g_ATraderSimCurBarFresh]
    curBarTime = GVAR.g_ATraderKDatas[_idx].Matrix[(GACV.KMatrixPos_TimeLine, curbarfresh)]
    preBarTime = GVAR.g_ATraderKDatas[_idx].Matrix[(GACV.KMatrixPos_TimeLine, curbarfresh - 1)]
    if matlab_float_time_to_datetime(curBarTime).hour >= 21:
        realBarDate = tb_command.atSendCmdTransTradeTimeToTradeDate(curBarTime)
        tickDay = int(realBarDate)
    else:
        tickDay = int(matlab_float_time_to_str_date(curBarTime))
    if GVAR.g_ATraderSimUnfiredStopOrders.size < 1 or len(GVAR.g_ATraderSimUnfiredStopOrders.shape) != 2:
        GVAR.g_ATraderSimUnfiredStopOrders = GVAR.g_ATraderSimUnfiredStopOrders.reshape((-1,
                                                                                         1))
    P = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetIdx, stopOrdersPos[0])])
    info = tb_command.atLoadTickDataFromPro(GVAR.g_ATraderStraInputInfo.TargetList[P]['Market'], GVAR.g_ATraderStraInputInfo.TargetList[P]['Code'], tickDay, 'NA')
    ticktime, tickprice, volumetick = info.Time.reshape((-1, 1)), info.Price.reshape((-1,
                                                                                      1)), info.VolumeTick.reshape((-1,
                                                                                                                    1))
    _t1 = np.where(ticktime > preBarTime)[0]
    _t2 = np.where(ticktime < curBarTime)[0]
    if len(_t1) > 0 and len(_t2) > 0:
        TickBeginNum = _t1[0]
        TickEndNum = _t2[(-1)]
        for tickNum in range(TickBeginNum, TickEndNum + 1):
            for sOrderPos in stopOrdersPos:
                sOrderPos = int(sOrderPos)
                orderAct = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_OrderAct, sOrderPos)])
                targetPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TargetPrice, sOrderPos)]
                curTickPrice = tickprice[(tickNum, 0)]
                if not bool(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBarBegin, sOrderPos)]):
                    if orderAct == GACV.OrderAct_Buy and curTickPrice <= targetPrice or orderAct == GACV.OrderAct_Sell and curTickPrice >= targetPrice:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBarBegin, sOrderPos)] = True
                    else:
                        continue
                    order_type = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopOrderType, sOrderPos)])
                    if order_type == GACV.StopOrderType_Loss:
                        mPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, sOrderPos)]
                        if orderAct == GACV.OrderAct_Buy and curTickPrice <= mPrice or orderAct == GACV.OrderAct_Sell and curTickPrice >= mPrice:
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, sOrderPos)] = curTickPrice
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_FireTime, sOrderPos)] = ticktime[tickNum]
                            tickBarOpen = np.array([curTickPrice]).ravel()
                            tickBarHigh = np.array([np.max(tickprice[tickNum:TickEndNum + 1])]).ravel()
                            tickBarLow = np.array([np.min(tickprice[tickNum:TickEndNum + 1])]).ravel()
                            tickBarVol = np.array([np.sum(volumetick[tickNum:TickEndNum + 1])]).ravel()
                            theFireOnePos = np.array([sOrderPos])
                if order_type == GACV.StopOrderType_Profit:
                    mPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, sOrderPos)]
                    if orderAct == GACV.OrderAct_Buy and curTickPrice >= mPrice or orderAct == GACV.OrderAct_Sell and curTickPrice <= mPrice:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_MPrice, sOrderPos)] = curTickPrice
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_FireTime, sOrderPos)] = ticktime[tickNum]
                        tickBarOpen = np.array([curTickPrice]).ravel()
                        tickBarHigh = np.array([np.max(tickprice[tickNum:TickEndNum + 1])]).ravel()
                        tickBarLow = np.array([np.min(tickprice[tickNum:TickEndNum + 1])]).ravel()
                        tickBarVol = np.array([np.sum(volumetick[tickNum:TickEndNum + 1])]).ravel()
                        theFireOnePos = np.array([sOrderPos])
                elif order_type == GACV.StopOrderType_Trailing:
                    stopGapType = int(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGapType, sOrderPos)])
                    stopGap = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopGap, sOrderPos)]
                    beginTrailingPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_BeginTrailingPrice, sOrderPos)]
                    if not GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_IsBeginTrailing, sOrderPos)]:
                        if orderAct == GACV.OrderAct_Buy and curTickPrice >= beginTrailingPrice or orderAct == GACV.OrderAct_Sell and curTickPrice <= beginTrailingPrice:
                            pass
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_IsBeginTrailing, sOrderPos)] = True
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, sOrderPos)] = False
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, sOrderPos)] = beginTrailingPrice
                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, sOrderPos)] = beginTrailingPrice
                if orderAct == GACV.OrderAct_Buy:
                    if stopGapType == GACV.StopGapType_Point:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = beginTrailingPrice - stopGap
                    else:
                        if stopGapType == GACV.StopGapType_Percent:
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = beginTrailingPrice - (beginTrailingPrice - targetPrice) * stopGap / 100.0
                        elif not False:
                            raise AssertionError
                        if orderAct == GACV.OrderAct_Sell:
                            if stopGapType == GACV.StopGapType_Point:
                                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = beginTrailingPrice + stopGap
                            else:
                                if stopGapType == GACV.StopGapType_Percent:
                                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = beginTrailingPrice + (targetPrice - beginTrailingPrice) * stopGap / 100.0
                                elif not False:
                                    raise AssertionError
                        else:
                            continue
                    if bool(GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, sOrderPos)]):
                        if orderAct == GACV.OrderAct_Buy and curTickPrice >= beginTrailingPrice or orderAct == GACV.OrderAct_Sell and curTickPrice <= beginTrailingPrice:
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_IsBeginTrailing, sOrderPos)] = True
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_InBeginTrailingBar, sOrderPos)] = False
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, sOrderPos)] = beginTrailingPrice
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, sOrderPos)] = beginTrailingPrice
                        else:
                            continue
                        stopTrailingPrice = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)]
                        trailingHigh = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, sOrderPos)]
                        trailingLow = GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, sOrderPos)]
                        if orderAct == GACV.OrderAct_Buy and stopTrailingPrice >= curTickPrice or orderAct == GACV.OrderAct_Sell and curTickPrice >= stopTrailingPrice:
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, sOrderPos)] = max(trailingHigh, curTickPrice)
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, sOrderPos)] = min(trailingLow, curTickPrice)
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_FireTime, sOrderPos)] = ticktime[tickNum]
                            GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = curTickPrice
                            tickBarOpen = np.array([curTickPrice]).ravel()
                            tickBarHigh = np.array([np.max(tickprice[tickNum:TickEndNum + 1])]).ravel()
                            tickBarLow = np.array([np.min(tickprice[tickNum:TickEndNum + 1])]).ravel()
                            tickBarVol = np.array([np.sum(volumetick[tickNum:TickEndNum + 1])]).ravel()
                            theFireOnePos = np.array([sOrderPos])
                else:
                    if curTickPrice > trailingHigh:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingHigh, sOrderPos)] = curTickPrice
                        if orderAct == GACV.OrderAct_Buy:
                            if stopGapType == GACV.StopGapType_Point:
                                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = curTickPrice - stopGap
                            elif stopGapType == GACV.StopGapType_Percent:
                                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = curTickPrice - (curTickPrice - targetPrice) * stopGap / 100.0
                    elif not False:
                        raise AssertionError
                    if curTickPrice < trailingLow:
                        GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_TrailingLow, sOrderPos)] = curTickPrice
                        if orderAct == GACV.OrderAct_Sell:
                            if stopGapType == GACV.StopGapType_Point:
                                GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = curTickPrice + stopGap
                            else:
                                if stopGapType == GACV.StopGapType_Percent:
                                    GVAR.g_ATraderSimUnfiredStopOrders[(GACV.SimStopOrder_StopTrailingPrice, sOrderPos)] = curTickPrice + (targetPrice - curTickPrice) * stopGap / 100.0
                                elif not False:
                                    raise AssertionError
                        else:
                            assert False, 'not support stoporder type'
                            if theFireOnePos.size > 0:
                                break

            if theFireOnePos.size > 0:
                break

    return (
     theFireOnePos, tickBarOpen, tickBarHigh, tickBarLow, tickBarVol)


def change_inttime_to_y_M_D_H_m_s(test_array):
    """将int型日期切割为由年，月，日，小时，分钟，秒组成的np.array()"""
    istick = GVAR.g_ATraderStraInputInfo['KFrequency'] == 'tick'
    return change_to_y_M_D_H_m_s(test_array, istick)