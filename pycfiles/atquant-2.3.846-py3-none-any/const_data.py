# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\data\const_data.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 21223 bytes
from datetime import datetime
from enum import Enum, unique
from atquant.utils.user_class import dotdict
GACV = dotdict({})

@unique
class Enum_FQ(Enum):
    NA = 'NA'
    FWARD = 'FWard'
    BWARD = 'BWard'


@unique
class Enum_Const(Enum):
    THE_FILE_IS_EMTPY = 'the file is empty'
    NO_DATA_RIGHT = 'No_data_right'
    ERROR_FILE = 'Error_file'
    ERROR_SID = 'Error_sid'
    ERROR_DATA = 'Error_data'
    ERROR_DATE = 'Error_date'
    TRADER_END_TIME = '15:00:00'
    FAIL_CONNECT_AT = '无法连接Auto-Trader，请确保其正在运行...\n如果您还没有安装Auto-Trader, 请点击链接了解软件详情: http://www.atrader.com.cn/software.php'
    ERROR_INPUT_IVALUE = '输入值错误'
    ERROR_INPUT_CONSTTYPE = '输入类型错误'
    ERROR_INPUT_START_DATE = '输入开始日期错误'
    ERROR_INPUT_END_DATE = '输入结束日期错误'
    ERROR_INPUT_BEGIN_GT_ENDDATE = '开始日期不能大于结束日期'
    ERROR_INPUT_BEGINDATE_REPLAYDATE = '输入错误: BeginDate 必须小于 RepalyDate'
    ERROR_ACTION_STOPLESS_WHEN_ALGORITHM = '在算法下单的时候不可以使用止损单!'
    ERROR_INPUT_TARGRTORDERPRICE = '输入参数错, 不可以同时针对报单和价格止盈止损!'
    ERROR_INPUT_CONTRACTS = '交易数量输入错误!'
    ERRPR_STOPGAP_FLOAT = '价格变动点数错误!'
    ERROR_EMPTY_TARGETLIST = '标的列表为空'
    ERROR_EMPTY_HISTORY_DATA = '取到历史行情数据为空!'
    ERROR_EMPTY_TIMELINE = '时间轴空缺, 策略运行失败, 请尝试更改时间'
    ERROR_EMPTY_ACCOUNTLIST_REALMODE = '实盘请至少添加一个账户'
    ERROR_FREQ_TOO_HIGH = '注册K线基础频率不能高于回测基础频率!'
    ERROR_NOTSUPPORT_REPLAY_VERSION = '该版本不支持回放功能'
    ERROR_NOTSUPPORT_MULTI_ACCOUNT_REPLAYMODE = '回放请使用单账户操作'
    ERROR_NOTSUPPORT_MULTI_ACCOUNT_BACKTESTMODE = '回测请使用单账户操作'
    ERROR_NOTSUPPORT_WHEN_REALMODE = '系统当前模式不支持此操作! 请关闭正在进行的实时交易程序.'
    ERROR_NOTSUPPORT_ORDER_DIRECT = '不支持的订单类型'
    ERROR_NOTSUPPORT_TICK_MULTI_FREQNUM = 'Tick frequency is not supported with multi number'
    ERROR_SUPPORT_REALTRADE_REPLAY = 'Only support in version two RealTrade and Replay'
    ERROR_ORDERID = 'TargetOrderID为空或小于0请检查'
    ERROR_DOWNLOAD_DATA = '下载数据出现异常, 请再次重试!'
    ERROR_STRUCT_RECVDATA = '结构体定义错误'
    ERROR_INPUT_PARAM = '输入参数错误'
    ERROR_GET_DATA = 'Get Data Error...'
    ERROR_NOTCOMPLTE_DATA = '获取数据不完整，请检查!'
    ERROR_INVALID_HIGHDATA = '无有效的更高频数据!'
    ERROR_INPUT_FREQUENCY = '输入注册频率错误!'
    ERROR_UNKNOW_OFFSETFLAG = '未知的OffsetFlag参数'
    ERROR_NOTMATCH_CODE_MARKET = '订阅的合约与市场出现不匹配的情况, 导致启动失败, 请检查并重试'
    ERROR_ACCOUNT_INVALID = '账户不可用, 请检查账户状态'
    ERROR_ACCOUNT_BACKTEST = '回测只能使用回测回放账户, 请重新设置账号'
    ERROR_ACCOUNT_REALMODE = '回测回放账户不能用于实盘模拟, 请重新设置账号'
    ERROR_DATA_TICK_MISS = '基础 tick 数据不足, 策略运行失败'
    ERROR_DATA_NORIGHT = '数据未购买，请购买后再使用'
    ERROR_MIXUSE_CONFIGFUNC_TRADERFUNC = 'traderConfigTo配置型函数与traderBuy等交易型函数不能混用'
    ERROR_MODE_ONE = '系统当前模式不支持此操作！请关闭正在进行的回测程序'
    ERROR_MODE_TWO = '系统当前模式不支持此操作！请关闭正在进行的回放程序'
    ERROR_MODE_THREE = '系统当前模式不支持此操作！请关闭正在进行的实时交易程序'
    ERROR_MODE_NOTZERO = '未知的AutoTrader系统模式'
    DAYTIME_CLOSING = datetime.strptime('15:00:00', '%H:%M:%S').time()
    DAYTIME_OPEN = datetime.strptime('09:00:00', '%H:%M:%S').time()
    MIN_TIME = datetime(1900, 1, 1)


@unique
class Enum_KFrequency(Enum):
    MIN = 'min'
    DAY = 'day'
    SEC = 'sec'
    TICK = 'tick'


def atDefineConst():
    global GACV
    GACV.KFreq_Tick = 1
    GACV.KFreq_Sec = 2
    GACV.KFreq_Min = 3
    GACV.KFreq_Day = 4
    GACV.KFreq_Week = 5
    GACV.KFreq_Month = 6
    GACV.KFreq_Year = 7
    GACV.KMatrixPos_Begin = 0
    GACV.KMatrixPos_TimeLine = 0
    GACV.KMatrixPos_FreshIdx = 1
    GACV.KMatrixPos_DayPos = 2
    GACV.KMatrixPos_End = 2
    GACV.KMatrix_Bar_Begin = 0
    GACV.KMatrix_Open = 0
    GACV.KMatrix_High = 1
    GACV.KMatrix_Low = 2
    GACV.KMatrix_Close = 3
    GACV.KMatrix_Volume = 4
    GACV.KMatrix_TurnOver = 5
    GACV.KMatrix_OpenInterest = 6
    GACV.KMatrix_Bar_End = 6
    GACV.TickMatrix_Vol = 1
    GACV.TickMatrix_BidPrice1 = 2
    GACV.TickMatrix_BidPrice2 = 3
    GACV.TickMatrix_BidPrice3 = 4
    GACV.TickMatrix_BidPrice4 = 5
    GACV.TickMatrix_BidPrice5 = 6
    GACV.TickMatrix_BidVol1 = 7
    GACV.TickMatrix_BidVol2 = 8
    GACV.TickMatrix_BidVol3 = 9
    GACV.TickMatrix_BidVol4 = 10
    GACV.TickMatrix_BidVol5 = 11
    GACV.TickMatrix_AskPrice1 = 12
    GACV.TickMatrix_AskPrice2 = 13
    GACV.TickMatrix_AskPrice3 = 14
    GACV.TickMatrix_AskPrice4 = 15
    GACV.TickMatrix_AskPrice5 = 16
    GACV.TickMatrix_AskVol1 = 17
    GACV.TickMatrix_AskVol2 = 18
    GACV.TickMatrix_AskVol3 = 19
    GACV.TickMatrix_AskVol4 = 20
    GACV.TickMatrix_AskVol5 = 21
    GACV.ACMatrix_ValidCash = 0
    GACV.ACMatrix_OrderFrozen = 1
    GACV.ACMatrix_MarginFrozen = 2
    GACV.ACMatrix_Begin = 0
    GACV.ACMatrix_LongPos = 0
    GACV.ACMatrix_LongFrozen = 1
    GACV.ACMatrix_LongAvg = 2
    GACV.ACMatrix_ShortPos = 3
    GACV.ACMatrix_ShortFrozen = 4
    GACV.ACMatrix_ShortAvg = 5
    GACV.ACMatrix_End = 5
    GACV.OrderCtg_Limit = 0
    GACV.OrderCtg_Market = 1
    GACV.OrderAct_Sell = 0
    GACV.OrderAct_Buy = 1
    GACV.OffsetFlag_Close = 0
    GACV.OffsetFlag_Open = 1
    GACV.StopOrderType_Loss = 0
    GACV.StopOrderType_Profit = 1
    GACV.StopOrderType_Trailing = 2
    GACV.StopGapType_Point = 0
    GACV.StopGapType_Percent = 1
    GACV.OrderStatus_PreHolding = 1
    GACV.OrderStatus_Holding = 2
    GACV.OrderStatus_Cancelled = 3
    GACV.OrderStatus_Filled = 4
    GACV.OrderStatus_Denied = 5
    GACV.StopOrderStatus_Holding = 0
    GACV.StopOrderStatus_Cancelled = 2
    GACV.StopOrderStatus_Fired = 1
    GACV.StopOrderStatus_PreHolding = 3
    GACV.ConfigTrade_AccountHandleP = 1
    GACV.ConfigTrade_TargetHashP = 2
    GACV.ConfigTrade_ConfigP = 3
    GACV.FreqType_Base = 1
    GACV.FreqType_Fresh = 2
    GACV.FreqType_Other = 3
    GACV.FurInfo_Multiple = 1
    GACV.FurInfo_MinMove = 2
    GACV.FurInfo_TradingFeeOpen = 3
    GACV.FurInfo_TradingFeeClose = 4
    GACV.FurInfo_TradingFeeCloseToday = 5
    GACV.FurInfo_LongMargin = 6
    GACV.FurInfo_ShortMargin = 7
    GACV.SimOrder_Begin = 0
    GACV.SimOrder_HandleIdx = 0
    GACV.SimOrder_OrderID = 1
    GACV.SimOrder_OrderTime = 2
    GACV.SimOrder_Status = 3
    GACV.SimOrder_TargetIdx = 4
    GACV.SimOrder_Contracts = 5
    GACV.SimOrder_Price = 6
    GACV.SimOrder_OrderCtg = 7
    GACV.SimOrder_OrderAct = 8
    GACV.SimOrder_OffsetFlag = 9
    GACV.SimOrder_OrderTag = 10
    GACV.SimOrder_RemainNum = 11
    GACV.SimOrder_OpenFrozenPrice = 12
    GACV.SimOrder_FilledTime = 13
    GACV.SimOrder_End = 13
    GACV.SimTrade_Begin = 0
    GACV.SimTrade_FilledTime = 0
    GACV.SimTrade_HandleIdx = 1
    GACV.SimTrade_OrderID = 2
    GACV.SimTrade_TargetIdx = 3
    GACV.SimTrade_Contracts = 4
    GACV.SimTrade_Price = 5
    GACV.SimTrade_OrderCtg = 6
    GACV.SimTrade_OrderAct = 7
    GACV.SimTrade_OffsetFlag = 8
    GACV.SimTrade_OrderTag = 9
    GACV.SimTrade_End = 9
    GACV.SimStopOrder_Begin = 0
    GACV.SimStopOrder_ClientID = 0
    GACV.SimStopOrder_HandleIdx = 1
    GACV.SimStopOrder_Status = 2
    GACV.SimStopOrder_StopOrderType = 3
    GACV.SimStopOrder_TargetIdx = 4
    GACV.SimStopOrder_TargetOrderID = 5
    GACV.SimStopOrder_TargetPrice = 6
    GACV.SimStopOrder_EntryTime = 7
    GACV.SimStopOrder_FireTime = 8
    GACV.SimStopOrder_StopGap = 9
    GACV.SimStopOrder_StopGapType = 10
    GACV.SimStopOrder_TrailingGap = 11
    GACV.SimStopOrder_TrailingType = 12
    GACV.SimStopOrder_TrailingHigh = 13
    GACV.SimStopOrder_TrailingLow = 14
    GACV.SimStopOrder_Contracts = 15
    GACV.SimStopOrder_OrderAct = 16
    GACV.SimStopOrder_OrderCtg = 17
    GACV.SimStopOrder_OrderTag = 18
    GACV.SimStopOrder_BeginTrailingPrice = 19
    GACV.SimStopOrder_IsBeginTrailing = 20
    GACV.SimStopOrder_MPrice = 21
    GACV.SimStopOrder_StopTrailingPrice = 22
    GACV.SimStopOrder_InBarBegin = 23
    GACV.SimStopOrder_InBeginTrailingBar = 24
    GACV.SimStopOrder_End = 24
    GACV.FIS_Market_Position_Count = (0, 16, 's', 16)
    GACV.FIS_Code_Position_Count = (
     GACV.FIS_Market_Position_Count[0] + GACV.FIS_Market_Position_Count[3], 16, 's', 16)
    GACV.FIS_Name_Position_Count = (GACV.FIS_Code_Position_Count[0] + GACV.FIS_Code_Position_Count[3], 16, 'H', 32)
    GACV.FIS_Type_Position_Count = (GACV.FIS_Name_Position_Count[0] + GACV.FIS_Name_Position_Count[3], 1, 'd', 8)
    GACV.FIS_Multiple_Position_Count = (GACV.FIS_Type_Position_Count[0] + GACV.FIS_Type_Position_Count[3], 1, 'd', 8)
    GACV.FIS_MinMove_Position_Count = (GACV.FIS_Multiple_Position_Count[0] + GACV.FIS_Multiple_Position_Count[3], 1, 'd', 8)
    GACV.FIS_TradingFeeOpen_Position_Count = (GACV.FIS_MinMove_Position_Count[0] + GACV.FIS_MinMove_Position_Count[3], 1, 'd', 8)
    GACV.FIS_TradingFeeClose_Position_Count = (GACV.FIS_TradingFeeOpen_Position_Count[0] + GACV.FIS_TradingFeeOpen_Position_Count[3], 1, 'd', 8)
    GACV.FIS_TradingFeeCloseToday_Position_Count = (GACV.FIS_TradingFeeClose_Position_Count[0] + GACV.FIS_TradingFeeClose_Position_Count[3], 1, 'd', 8)
    GACV.FIS_LongMargin_Position_Count = (GACV.FIS_TradingFeeCloseToday_Position_Count[0] + GACV.FIS_TradingFeeCloseToday_Position_Count[3], 1, 'd', 8)
    GACV.FIS_ShortMargin_Position_Count = (GACV.FIS_LongMargin_Position_Count[0] + GACV.FIS_LongMargin_Position_Count[3], 1, 'd', 8)
    GACV.FIS_TargetMarket_Position_Count = (GACV.FIS_ShortMargin_Position_Count[0] + GACV.FIS_ShortMargin_Position_Count[3], 16, 's', 16)
    GACV.FIS_TargetCode_Position_Count = (GACV.FIS_TargetMarket_Position_Count[0] + GACV.FIS_TargetMarket_Position_Count[3], 16, 's', 16)
    GACV.FIS_OptionType_Position_Count = (GACV.FIS_TargetCode_Position_Count[0] + GACV.FIS_TargetCode_Position_Count[3], 1, 's', 1)
    GACV.FIS_CallOrPut_Position_Count = (GACV.FIS_OptionType_Position_Count[0] + GACV.FIS_OptionType_Position_Count[3], 1, 's', 1)
    GACV.FIS_ListDate_Position_Count = (GACV.FIS_CallOrPut_Position_Count[0] + GACV.FIS_CallOrPut_Position_Count[3], 1, 'd', 8)
    GACV.FIS_LastTradingDate_Position_Count = (GACV.FIS_ListDate_Position_Count[0] + GACV.FIS_ListDate_Position_Count[3], 1, 'd', 8)
    GACV.FIS_EndDate_Position_Count = (GACV.FIS_LastTradingDate_Position_Count[0] + GACV.FIS_LastTradingDate_Position_Count[3], 1, 'd', 8)
    GACV.FIS_ExerciseDate_Position_Count = (GACV.FIS_EndDate_Position_Count[0] + GACV.FIS_EndDate_Position_Count[3], 1, 'd', 8)
    GACV.FIS_DeliveryDate_Position_Count = (GACV.FIS_ExerciseDate_Position_Count[0] + GACV.FIS_ExerciseDate_Position_Count[3], 1, 'd', 8)
    GACV.FIS_CMUnit_Position_Count = (GACV.FIS_DeliveryDate_Position_Count[0] + GACV.FIS_DeliveryDate_Position_Count[3], 1, 'd', 8)
    GACV.FIS_ExercisePrice_Position_Count = (GACV.FIS_CMUnit_Position_Count[0] + GACV.FIS_CMUnit_Position_Count[3], 1, 'd', 8)
    GACV.FIS_MarginUnit_Position_Count = (GACV.FIS_ExercisePrice_Position_Count[0] + GACV.FIS_ExercisePrice_Position_Count[3], 1, 'd', 8)


def atStringToConst(first_type, second_type):
    """
    输入要获取常量的类型和字符串，返回已经定义好的枚举常量
    :param first_type: 类型前缀,字符串类型
    :param second_type: 类型后缀，字符串类型
    :return: 定义好的枚举常量
    """
    if first_type == 'KBaseFreq':
        first_type = 'KFreq'
    if first_type.upper() in ('STOPGAPTYPE', 'TRAILINGTYPE'):
        first_type = 'STOPGAPTYPE'
    key = '%s_%s' % (first_type.upper(), second_type.upper())
    for item in GACV.keys():
        if item.upper() == key:
            return GACV[item]

    return 0


def atConstToString(my_type, iValue):
    """输入要获取的常量类型和数字变量，返回对应的字符串常量"""
    StringValue = ''
    if my_type == 'KBaseFreq':
        if iValue == GACV.KFreq_Tick:
            StringValue = 'tick'
        else:
            if iValue == GACV.KFreq_Sec:
                StringValue = 'sec'
            else:
                if iValue == GACV.KFreq_Min:
                    StringValue = 'min'
                else:
                    if iValue == GACV.KFreq_Day:
                        StringValue = 'day'
                    else:
                        if iValue == GACV.KFreq_Week:
                            StringValue = 'week'
                        else:
                            if iValue == GACV.KFreq_Month:
                                StringValue = 'month'
                            else:
                                if iValue == GACV.KFreq_Year:
                                    StringValue = 'year'
                                else:
                                    raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
    else:
        if my_type == 'OrderCtg':
            if iValue == GACV.OrderCtg_Limit:
                StringValue = 'Limit'
            else:
                if iValue == GACV.OrderCtg_Market:
                    StringValue = 'Market'
                else:
                    raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
        else:
            if my_type == 'OrderAct':
                if iValue == GACV.OrderAct_Buy:
                    StringValue = 'Buy'
                else:
                    if iValue == GACV.OrderAct_Sell:
                        StringValue = 'Sell'
                    else:
                        raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
            else:
                if my_type == 'OffsetFlag':
                    if iValue == GACV.OffsetFlag_Open:
                        StringValue = 'Open'
                    else:
                        if iValue == GACV.OffsetFlag_Close:
                            StringValue = 'Close'
                        else:
                            raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
                else:
                    if my_type == 'StopOrderType':
                        if iValue == GACV.StopOrderType_Loss:
                            StringValue = 'Loss'
                        else:
                            if iValue == GACV.StopOrderType_Profit:
                                StringValue = 'Profit'
                            else:
                                if iValue == GACV.StopOrderType_Trailing:
                                    StringValue = 'Trailing'
                                else:
                                    raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
                    else:
                        if my_type == 'StopGapType':
                            if iValue == GACV.StopGapType_Point:
                                StringValue = 'Point'
                            else:
                                if iValue == GACV.StopGapType_Percent:
                                    StringValue = 'Percent'
                                else:
                                    raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
                        else:
                            if my_type == 'StopOrderStatus':
                                if iValue == GACV.StopOrderStatus_Holding:
                                    StringValue = 'Holding'
                                else:
                                    if iValue == GACV.StopOrderStatus_Cancelled:
                                        StringValue = 'Cancelled'
                                    else:
                                        if iValue == GACV.StopOrderStatus_Fired:
                                            StringValue = 'Fired'
                                        else:
                                            raise ValueError(Enum_Const.ERROR_INPUT_IVALUE.value)
                            else:
                                raise ValueError(Enum_Const.ERROR_INPUT_CONSTTYPE.value)
    return StringValue


def atGetAllPriceType():
    """
    设置当前pro所支持下单模式
    日后有增加其它下单模式,直接添加到此函数中
    在atTradeOperation中用到
    """
    output = [
     'Market'.upper(), 'Limit'.upper(), 'MarketIOC'.upper(), 'MarketRestTolimit'.upper(), 'MarketFOK'.upper(),
     'LimitFOK'.upper(), 'LimitIOC'.upper(), '5LevelIOC'.upper(), '5LevelFOK'.upper(), '5LevelROD'.upper()]
    return output


def raise_error_if_at_return_error(error, prefix=None, suffix=None):
    """AT 返回的错误信息"""
    prefix = 'AutoTrader Return ' if prefix is None else prefix
    suffix = '' if suffix is None else suffix
    comma_prefix = ',' if prefix else ''
    comma_suffix = ',' if suffix else ''
    if error is None:
        raise ValueError('{!r}{!r}Error none{!r}{!r}'.format(prefix, comma_prefix, comma_suffix, suffix))
    else:
        if error == Enum_Const.NO_DATA_RIGHT.value:
            raise ValueError('{!r}{!r}{}{!r}{!r}'.format(prefix, comma_prefix, Enum_Const.ERROR_DATA_NORIGHT.value, comma_suffix, suffix))
        else:
            if error == Enum_Const.ERROR_DATA.value:
                raise ValueError('{!r}{!r}Error data{!r}{!r}'.format(prefix, comma_prefix, comma_suffix, suffix))
            else:
                if error == Enum_Const.ERROR_DATE.value:
                    raise ValueError('{!r}{!r}Error date{!r}{!r}'.format(prefix, comma_prefix, comma_suffix, suffix))
                else:
                    if error == Enum_Const.ERROR_FILE.value:
                        raise ValueError('{!r}{!r}Error file{!r}{!r}'.format(prefix, comma_prefix, comma_suffix, suffix))
                    elif error == Enum_Const.ERROR_SID.value:
                        raise ValueError('{!r}{!r}Error Security sid{!r}{!r}'.format(prefix, comma_prefix, comma_suffix, suffix))


atDefineConst()