# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\data\global_variable.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 21497 bytes
from datetime import datetime
from functools import lru_cache
import numpy as np, pandas as pd
from atquant.data.const_data import Enum_FQ, Enum_KFrequency, Enum_Const
from atquant.data.const_data import atStringToConst
from atquant.socket_ctrl.base_socket import HandleSocket
from atquant.utils.internal_exception import ToolBoxErrors
from atquant.utils.user_class import dotdict, OutputFileManager
from .const_data import GACV
g_Parral = False
g_ATraderStrategyName = ''
g_isBackTestNormalfinished = True
g_ATraderAlgoTrade = False
g_BeginDate = datetime(1900, 1, 1).strftime('%Y-%m-%d')
g_EndDate = datetime.now().strftime('%Y-%m-%d')
g_ATraderSimMode = 0
g_ATraderSimCurBarFresh = None
g_ATraderSimOrders = np.array([])
g_IsATraderTrade = 0
g_ATraderOrderNum = 0
g_ATraderStopOrderNum = 0
g_ATraderAlgoOrderNum = 0
g_ATraderRealMode = 0
g_ATraderStraInputInfo = dotdict({})
g_AtraderSetInfo = dotdict({})
g_ATraderAccountHandleArray = []
g_ATraderKDatas = []
g_ATraderDataValueFresh = np.array([])
g_ATraderSID = HandleSocket(3293)
g_ATraderSIDCB = HandleSocket(3294)
g_ATraderFutureInfoMap = dotdict({})
g_ATraderFutureInfoMapV2 = pd.DataFrame([])
g_ATraderAccountMatrix = np.array([])
g_ATraderAccountConfigBarOper = []
g_ATraderMarketOrderHolding = False
g_ATraderAccountConfigMatrix = []
g_ATraderDataValueFreshUserD = np.array([])
g_ATraderSimUnfilledOrders = np.array([])
g_ATraderSimTrades = np.array([])
g_ATraderSimUnfiredStopOrders = np.array([])
g_ATraderSimStopOrders = np.array([])
g_user_input_info = dotdict({})
ClientOrderID = 0
g_ATraderTradingDays = np.array([])
g_ATraderTickMap = dotdict({})
g_ATraderCurTickInfo = dotdict({})
g_ATraderGetKData_NoReturn = False
g_ApendEnoughConstNum = 100000000000000000000000000
g_ATraderRegIndiCalc = []
g_ATraderRegKDataInfo = []
g_ATraderAccountOrderMode = 0
g_ATraderRealTradeSaveFreshPositionInAppend = float('nan')
g_ATraderSlidePrice = 0
g_ATraderLimitType = 0
g_ATraderLastLog = []
g_ATraderOldMaxKTime = np.nan
g_ATraderLatestTick = np.array([])
g_ATraderPriceLoc = 0
g_ATraderAccountInfo = dotdict({})
g_ATraderRTAccountConfig = np.array([])
g_ATraderRealHandles = np.array([])
g_ATraderTrigerBy = False
g_ATraderLastHeartBeat = 0
g_ATraderRealTradeSaveFreshPosition = 0
g_ATraderRealOrders = pd.DataFrame([], index=['dbClientID', 'dbAccHandleID', 'dbOrderPrice', 'dbFilledPrice',
 'dbVolume', 'dbVolumeTraded', 'eOrderStatus', 'strStrategyName',
 'strMarket', 'strCode', 'tmCreate', 'tmFilled',
 'eOrderAct', 'dbOrderCtg', 'dbOffsetFlag', 'dbOrderPrice',
 'dbFilledPrice', 'dbVolume', 'dbVolumeTraded', 'eOrderStatus'])
g_ATraderRegisterRealK = dotdict({})
g_ATraderLastChangeOrder = dotdict({})
g_ATraderDailyCloseTime = 0
g_ATraderRegIndiCalc = []
g_ATraderRealCurBarOperation = pd.DataFrame([], index=['HandleIdx', 'Market', 'Code', 'Contracts', 'Price', 'OrderCtg', 'OrderAct', 'OffsetFlag', 'OrderTag', 'RemainNum'])

@lru_cache(None)
def atBarItemsLen():
    """
    :return: int, 返回bar包含字段个数 
    """
    step = GACV.KMatrix_Bar_End - GACV.KMatrix_Bar_Begin + 1
    return step


@lru_cache(None)
def atACItemsLen():
    """
    :return: int, 返回 GACV.ACMatrix_Begin-GACV.ACMatrix_End 之间item个数
    """
    return GACV.ACMatrix_End - GACV.ACMatrix_Begin + 1


@lru_cache(None)
def atBarHeadLen():
    """
    :return: int, 返回包含标的矩阵常见头的长度 
    """
    head = GACV.KMatrixPos_End - GACV.KMatrixPos_Begin + 1
    return head


@lru_cache(None)
def atSimTradeItemsLen():
    """
    :return: int, 返回 GACV.SimTrade_Begin-GACV.SimTrade_End 之间item个数
    """
    return GACV.SimTrade_End - GACV.SimTrade_Begin + 1


@lru_cache(None)
def atSimOrderItemsLen():
    """
    :return: int, 返回 GACV.SimOrder_Begin-GACV.SimOrder_End 之间item个数
    """
    return GACV.SimOrder_End - GACV.SimOrder_Begin + 1


@lru_cache(None)
def atSimStopOrderItemsLen():
    """
    :return: int, 返回 GACV.SimStopOrder_Begin-GACV.SimStopOrder_End 之间item个数
    """
    return GACV.SimStopOrder_End - GACV.SimStopOrder_Begin + 1


def atKMatixBarItemPos(bar_item, target_offset=0, contain_head=True):
    """
    计算标的的 bar 中某一项，在基础矩阵中的索引位置
    
    :param bar_item: int, [GACV.KMatrix_Bar_Begin,GACV.KMatrix_Bar_End]之间的参数， 比如：GACV.KMatrix_Open。
    :param target_offset: int, 0表示第1个标的,1表示第2个标的
    :param contain_head: bool, 是否包含基础矩阵的头。即[GACV.KMatrixPos_Begin,GACV.KMatrixPos_End]
    :return: int,返回索引信息
    """
    if bar_item < GACV.KMatrix_Bar_Begin or bar_item > GACV.KMatrix_Bar_End:
        assert False, 'Bar的索引超出范围，需要在 [GACV.KMatrix_Bar_Begin,GACV.KMatrix_Bar_End] 之间'
        if contain_head:
            pass
        return atBarHeadLen() + target_offset * atBarItemsLen() + bar_item
    else:
        return target_offset * atBarItemsLen() + bar_item


def atGetBaseMx(index):
    """
    这是一个方便函数数。获取 g_ATraderKDatas 中 索引为 index 词典中的 Matrix 的 value 项.
    :param index: int, g_ATraderKDatas 索引
    :return: g_ATraderKDatas[index].Matrix
    """
    return g_ATraderKDatas[index].Matrix


def atSetBaseMx(index, matrix):
    """
    这是一个方便函数数。设置 g_ATraderKDatas 中 索引为 index 词典中的 Matrix 的 value 项.
    :param index: int, g_ATraderKDatas 索引
    :param matrix: pandas.DataFrame
    """
    g_ATraderKDatas[index].Matrix = matrix


def atSetTraderAccountMatrixValue(axis0, axis1, axis2, value):
    global g_ATraderAccountMatrix
    g_ATraderAccountMatrix[(axis0, axis1, axis2)] = value


def atAddTraderAccountMatrixValue(axis0, axis1, axis2, value):
    g_ATraderAccountMatrix[(axis0, axis1, axis2)] += value


def atGetTraderAccountMatrixValue(axis0, axis1, axis2):
    value = g_ATraderAccountMatrix[(axis0, axis1, axis2)]
    return value


def atSetATraderSimCurBarFresh(value):
    global g_ATraderSimCurBarFresh
    g_ATraderSimCurBarFresh = value


def atBeInDirectOrderMode():
    global g_ATraderAccountOrderMode
    r = True if g_ATraderAccountOrderMode == 1 else False
    return r


def atBeInUnsetOrderMode():
    r = True if g_ATraderAccountOrderMode == 0 else False
    return r


def atBeInConfigurationOrderMode():
    if g_ATraderAccountOrderMode == 2:
        return True
    return False


def atResetAlgoOrderSignal():
    global g_IsATraderTrade
    g_IsATraderTrade = False


def atExistAlgoOrderSignal():
    return g_IsATraderTrade


def atEnterBackTestMode():
    """Enter backtest mode and change the global record"""
    global g_ATraderSimMode
    g_ATraderSimMode = 1


def atResetBackTestMode():
    """Exit backtest mode and reset the global record"""
    global g_ATraderSimMode
    g_ATraderSimMode = 0


def atBeInBackTestMode():
    """查询当前系统模式是否处于回测模式"""
    if g_ATraderSimMode == 1:
        bInBackTestMode = True
    else:
        bInBackTestMode = False
    return bInBackTestMode


def atEnterRealMode():
    """进入实时交易模式"""
    global g_ATraderRealMode
    g_ATraderRealMode = True


def atResetRealMode():
    """进入实时交易模式"""
    global g_ATraderRealMode
    g_ATraderRealMode = False


def atBeInRealMode():
    """查询当前系统模式是否处于实时模式"""
    if g_ATraderRealMode == 1:
        bInRealMode = True
    else:
        bInRealMode = False
    return bInRealMode


def atEnterDataFreshMode():
    """进入数据刷新模式"""
    global g_ATraderTrigerBy
    g_ATraderTrigerBy = True


def atBeInDataFreshMode():
    """获取当前数据刷新模式的状态"""
    return ~g_ATraderTrigerBy


def atEnterDirectOrderMode():
    global g_ATraderAccountOrderMode
    if g_ATraderAccountOrderMode != 0 and g_ATraderAccountOrderMode != 1:
        raise ValueError(Enum_Const.ERROR_MIXUSE_CONFIGFUNC_TRADERFUNC.value)
    g_ATraderAccountOrderMode = 1


def atEnterDataFreshMode():
    global g_ATraderTrigerBy
    g_ATraderTrigerBy = 0


def atResetOrderMode():
    global g_ATraderAccountOrderMode
    g_ATraderAccountOrderMode = 0


def atEnterConfigurationOrderMode():
    global g_ATraderAccountOrderMode
    if g_ATraderAccountOrderMode != 0 and g_ATraderAccountOrderMode != 2:
        raise Exception(Enum_Const.ERROR_MIXUSE_CONFIGFUNC_TRADERFUNC.value)
    g_ATraderAccountOrderMode = 2


def generatingStrategyName(StrategyName):
    """
    将用户输入的StrategyName转变为与AT交互的g_StrategyName
    在StrategyName的基础上增加时间戳
    """
    global g_ATraderStrategyName
    tmp_time = datetime.now().strftime('%H%M%S')
    g_ATraderStrategyName = 'py_' + str(StrategyName) + '_' + tmp_time


def fq_type_str2enum(type_str):
    """
    根据输入的参数判断复权参数输入是否正确
    :param type_str:  str, Enum_FQ字符串
    :return: 
    """
    if type_str == 'NA':
        return Enum_FQ.NA
    if type_str == 'FWard':
        return Enum_FQ.FWARD
    if type_str == 'BWard':
        return Enum_FQ.BWARD
    ToolBoxErrors.unexpect_switch_error('fq')


def kfrequency_type_str2enum(type_str):
    """根据输入的参数判断是否为枚举的频率类型,如果是就返回枚举变量名,NotImplementedError如果没有则返回错误"""
    if type_str == 'min':
        return Enum_KFrequency.MIN
    if type_str == 'day':
        return Enum_KFrequency.DAY
    if type_str == 'sec':
        return Enum_KFrequency.SEC
    if type_str == 'tick':
        return Enum_KFrequency.TICK
    ToolBoxErrors.unexpect_switch_error('kfrequency')


def atResetAlgorithmTradeMode():
    """设置和重置算法下单"""
    global g_ATraderAlgoTrade
    g_ATraderAlgoTrade = False


def atEnterAlgorithmTradeMode():
    """Enter algorithm trade mode and change the global record"""
    global g_ATraderAlgoTrade
    g_ATraderAlgoTrade = True


def atBeInAlgorithmTradeMode():
    """Return true only if be in algorithm trade mode"""
    return g_ATraderAlgoTrade


def atGenerateAlgoOrderSignal():
    """ This happen every time algorithm trade generate order signal"""
    global g_IsATraderTrade
    g_IsATraderTrade = True


def atResetAlgoOrderSignal():
    global g_IsATraderTrade
    g_IsATraderTrade = False


def atResetDailyCloseTimeSetting():
    """将当天停止交易时间设置为0"""
    global g_ATraderDailyCloseTime
    g_ATraderDailyCloseTime = 0


def atExistDailyCloseTimeSetting():
    """判断用户是否设置当天停止交易时间"""
    if g_ATraderDailyCloseTime == 0:
        return False
    return True


def atBeInDirectOrderMode():
    if g_ATraderAccountOrderMode == 1:
        return True
    return False


def atBeInUnsetOrderMode():
    if g_ATraderAccountOrderMode == 0:
        return True
    return False


def atResetBackTestSetting():
    global g_AtraderSetInfo
    g_AtraderSetInfo = dotdict({})


def atRemoveInvalidTarget(target_list):
    return_target_list = []
    for item in target_list:
        market_ = item.get('Market', '')
        code_ = item.get('Code', '')
        if isinstance(market_, str) and market_ and isinstance(code_, str) and code_:
            return_target_list.append({'Market': market_, 'Code': code_})

    if len(return_target_list) < 1:
        raise ValueError(Enum_Const.ERROR_EMPTY_TARGETLIST.value)
    return return_target_list


def atExistBackTestSetting():
    if len(g_AtraderSetInfo) > 0:
        return True
    return False


def atIsBackTestNormalFinished():
    global g_isBackTestNormalfinished
    if g_isBackTestNormalfinished is True:
        return True
    return False


def atSetBackTestFinished(state):
    """
    :param state: bool, True 正常终止，False，异常终止 
    :return: 
    """
    global g_isBackTestNormalfinished
    g_isBackTestNormalfinished = state


def atHandleIdxCount():
    global g_ATraderAccountHandleArray
    return len(g_ATraderAccountHandleArray)


def atTargetIdxCount():
    global g_ATraderStraInputInfo
    if 'TargetList' in g_ATraderStraInputInfo:
        return len(g_ATraderStraInputInfo['TargetList'])
    return 0


def find_matrix_eq_freq_freqnum_index(matrixs, freq, freqnum):
    """
    freq = atStringToConst('KBaseFreq', KFrequency)
    KFrequency包含:'tick', 'day', 'sec', 'min' 
    :param matrixs: 
    :param freq: int 或者 str ,若为int类型，则返回值是atStringToConst('KBaseFreq', KFrequency)的返回值.若为str类型，则为KFrequency代表的值
    :param freqnum: int, 频数。比如
    :return: 目标所在矩阵链的索引,若不存在，返回None
    eg:
        matrix_pos('min',1)
        matrix_pos(2,1)
    """
    if isinstance(freq, str):
        freq = atStringToConst('KBaseFreq', freq)
    else:
        freq = int(freq)
    for i, kdata in enumerate(matrixs):
        if kdata['iFreq'] == freq and kdata['FreqNum'] == freqnum:
            return i


def generate_base_dataframe(ntarget, timelinelen):
    """
    创建一个基础pandas.DataFrame结构，可以容纳n个标的信息
    :param ntarget: int,标的数据
    :param timelinelen: int,时间线长度
    :return: pandas.DataFrame
    """
    index = [
     GACV.KMatrixPos_TimeLine, GACV.KMatrixPos_FreshIdx, GACV.KMatrixPos_DayPos]
    begin = GACV.KMatrixPos_End + GACV.KMatrix_Bar_Begin
    end = begin + ntarget * (GACV.KMatrix_Bar_End - GACV.KMatrix_Bar_Begin + 1)
    index.extend(range(begin, end, 1))
    df = pd.DataFrame(np.zeros((GACV.KMatrixPos_End + ntarget * GACV.KMatrix_Bar_End, timelinelen)), index=index)
    return df


def generate_base_ndarray(ntarget, timelinelen):
    """
    创建一个基础numpy.array结构，可以容纳n个标的信息
    :param ntarget: int,标的数据
    :param timelinelen: int,时间线长度
    :return: numpy.array
    """
    head = atBarHeadLen()
    body = atBarItemsLen() * ntarget
    arr = np.zeros((head + body, timelinelen))
    return arr


def root_sub_dir(sub=''):
    return OutputFileManager.root_sub_dir(sub)


def rm_root_sub_dir(sub):
    return OutputFileManager.rm_root_sub_dir(sub)


def mk_root_sub_dir(sub):
    return OutputFileManager.mk_root_sub_dir(sub)


def cls_root_sub_dir(sub):
    return OutputFileManager.cls_root_sub_dir(sub)