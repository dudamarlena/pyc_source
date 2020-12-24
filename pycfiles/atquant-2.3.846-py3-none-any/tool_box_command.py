# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\socket_ctrl\tool_box_command.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 48331 bytes
import os, re, struct, sys, time, traceback, xml.dom.minidom
from datetime import datetime
import numpy as np, pandas as pd, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR, atquant.utils.datetime_func as UTILS_DT, atquant.utils.internal_util as UTILS_UTIL
from atquant.data.const_data import GACV
from atquant.data.const_data import raise_error_if_at_return_error
from atquant.utils.internal_util import trace_cmd
from atquant.utils.logger import write_syslog
from atquant.utils.user_class import dotdict

def xml_tag_key_value(xmlstr, tag, attr):
    """
    获取xml第一个节点的属性的值
    """
    try:
        root = xml.parseString(xmlstr)
        allSchemeListItems = root.getElementsByTagName(tag)
        for item in allSchemeListItems:
            if item.hasAttribute(attr):
                return item.getAttribute(attr)

    except Exception:
        write_syslog(traceback.format_exc(), level='error')


def from_data_get_file_name(data):
    """从接收到的数据，解析文件路径"""
    if data is None:
        return
    byte_array = bytearray(data)
    for j in range(len(byte_array)):
        if byte_array[j] == 0 and byte_array[(j + 1)] == 0:
            if j < 15:
                pass
            else:
                info = ''
                for i in range(0, j, 2):
                    temp_data = byte_array[i:i + 2]
                    temp = temp_data[0]
                    temp_data[0] = temp_data[1]
                    temp_data[1] = temp
                    info = info + temp_data.decode('utf-16', errors='ignore').replace('\x00', '')

                try:
                    if info == '':
                        return ''
                    else:
                        return os.path.abspath(os.path.normpath(info))
                except Exception:
                    return info


def get_info_from_binary_array(data, element):
    """从接收的二进制中剥离出结构体数据"""
    gcv_key = 'FIS_%s_Position_Count' % element
    if gcv_key not in GACV:
        raise ValueError('The key input error')
    byte_array = bytearray(data[GACV[gcv_key][0]:GACV[gcv_key][0] + GACV[gcv_key][3]])
    if GACV[gcv_key][2] == 'd':
        format_s = '!%dd' % GACV[gcv_key][1]
        info, = struct.unpack(format_s, byte_array)
        return info
    for j in range(len(byte_array)):
        if byte_array[j] == 0:
            if GACV[gcv_key][2] == 's':
                format_s = '!%ds' % j
                info, = struct.unpack(format_s, byte_array[0:j])
                return info
            if GACV[gcv_key][2] == 'H':
                info = ''
                for i in range(0, j, 2):
                    temp_data = byte_array[i:i + 2]
                    temp = temp_data[0]
                    temp_data[0] = temp_data[1]
                    temp_data[1] = temp
                    info = info + temp_data.decode('utf-16', errors='ignore').replace('\x00', '')

                return info
            raise ValueError(const_da.Enum_Const.ERROR_STRUCT_RECVDATA.value)


def get_real_data_from_byte_array(byte_array, data_len, data_type):
    """
    从接受的数据中提取各种类型的数据
    """
    byte_array = bytearray(byte_array)
    if data_type == 'd':
        format_s = '!%dd' % data_len
        info, = struct.unpack(format_s, byte_array)
        return info
    for j in range(len(byte_array)):
        if byte_array[j] == 0:
            if data_type == 's':
                format_s = '!%ds' % j
                info, = struct.unpack(format_s, byte_array[0:j])
                return info
            if data_type == 'H':
                s0 = slice(0, j, 2)
                s1 = slice(1, j, 2)
                info = bytearray(byte_array[:j])
                if j >= 2 and j % 2 == 0:
                    info[s0], info[s1] = info[s1], info[s0]
                else:
                    info = b''
                return info.decode(encoding='utf-16', errors='ignore').replace('\x00', '')
            raise ValueError(const_da.Enum_Const.ERROR_INPUT_PARAM.value)


@trace_cmd
def atSendCmdGetLoginUserRight():
    """
    向AT pro请求：获取用户名的权限信息,当前只用于检测回放
    0 表示不能进行回放
    1 表示能进行回放
    """
    cmd = 'ATraderGetUserRight'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=4)
    data, = struct.unpack('i', data[0:4])
    return data


@trace_cmd
def atSendCmdStartReplay(StrategyName, BeginDateTime, EndDateTime, IDList, KFrequency, KFreNum, Speed):
    cmd = 'ATraderStartReplay'
    head_tail = 'cmd="%s" KFrequency="%s" KFreNum="%d" begin="%s" end="%s" StraName="%s" Speed="%d"' % (
     cmd, KFrequency, KFreNum, BeginDateTime, EndDateTime, StrategyName, Speed)
    middle = ''.join(['<item Market="%s" Code="%s"/>\n' % (item['Market'], item['Code']) for item in IDList])
    GVAR.g_ATraderSID.send_xml_cmd(head_tail, middle)
    time.sleep(0.1)
    result = GVAR.g_ATraderSID.recv_data()
    value = xml_tag_key_value(result, 'return', 'result')
    if value != 'true':
        raise Exception(xml_tag_key_value(result, 'return', 'errInfo'))


@trace_cmd
def atSendCmdStopReplay():
    cmd = 'ATraderStopReplay'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.1)
    result = GVAR.g_ATraderSID.recv_data()


def atLoadTickDataFromPro(Market, Code, Date, FQ):
    """
    
    :param Market: str, 市场名称
    :param Code: str, 标的代号
    :param Date: int, 日期，形如：20170501
    :param FQ: str，复权类型，包括："NA","FWard","BWard"
    :return: dict, 获取的信息
    """

    def dealMatContent(mat_content, info):
        info.Time = mat_content.Time
        info.Price = mat_content.Price
        info.Volume = mat_content.Volume
        info.VolumeTick = mat_content.VolumeTick
        info.TurnOver = mat_content.TurnOver
        info.OpenInterest = mat_content.OpenInterest
        for i in range(1, 6):
            BidPrice_key = 'BidPrice%d' % i
            BidVolume_key = 'BidVolume%d' % i
            AskPrice_key = 'AskPrice%d' % i
            AskVolume_key = 'AskVolume%d' % i
            info.BidPrice = UTILS_UTIL.append_or_assign_2d_array_axis1(info.BidPrice, mat_content[BidPrice_key][:, 0], 1000)
            info.BidVolume = UTILS_UTIL.append_or_assign_2d_array_axis1(info.BidVolume, mat_content[BidVolume_key][:, 0], 1000)
            info.AskPrice = UTILS_UTIL.append_or_assign_2d_array_axis1(info.AskPrice, mat_content[AskPrice_key][:, 0], 1000)
            info.AskVolume = UTILS_UTIL.append_or_assign_2d_array_axis1(info.AskVolume, mat_content[AskVolume_key][:, 0], 1000)

        return info

    info = dotdict({'Time': np.array([]), 
     'Price': np.array([]), 
     'Volume': np.array([]), 
     'VolumeTick': np.array([]), 
     'TurnOver': np.array([]), 
     'OpenInterest': np.array([]), 
     'BidPrice': np.array([]), 
     'BidVolume': np.array([]), 
     'AskPrice': np.array([]), 
     'AskVolume': np.array([])})
    id = '%s_%s_%d_%s' % (Market, Code, Date, FQ)
    if id in GVAR.g_ATraderTickMap and Date != UTILS_DT.to_int_now_date():
        return GVAR.g_ATraderTickMap.get(id, info)
    matFile = at_send_ATraderGetTDPData(Market, Code, Date, FQ)
    try:
        mat_content = dotdict(UTILS_UTIL.load_mat(matFile, error='raise'))
    except Exception as e:
        UTILS_UTIL.run_ignore_exception(os.remove, matFile)
        raise Exception(const_da.Enum_Const.ERROR_DOWNLOAD_DATA.value) from e

    if 'Time' not in mat_content or mat_content.Time.size < 1:
        UTILS_UTIL.run_ignore_exception(os.remove, matFile)
        return info
    atClearMatFileIncludeCurTradeDate(matFile, Date)
    info = dealMatContent(mat_content, info)
    GVAR.g_ATraderTickMap[id] = info
    return info


@trace_cmd
def at_send_ATraderGetKDataMulti(TargetList, BeginDate, EndDate, KFrequency, KFreNum, FilledUp, FQ):
    cmd = 'ATraderGetKDataMulti'
    head_tail = 'cmd="%s" KFrequency="%s" KFreNum="%d" BeginDate="%d" EndDate="%d" FilledUp="%d" FQ="%s"' % (
     cmd, KFrequency, KFreNum, BeginDate, EndDate, FilledUp, FQ)
    middle = ''.join(['<item Market="%s" Code="%s"/>' % (item['Market'], item['Code']) for item in TargetList])
    GVAR.g_ATraderSID.send_xml_cmd(head_tail, middle)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=2048)
    matFile = from_data_get_file_name(data)
    raise_error_if_at_return_error(matFile)
    return matFile


@trace_cmd
def at_send_AtraderGetKData(BeginDate, EndDate, Market, Code, KFrequency, FilledUp, FQ, NoReturn):
    """
    发送AtraderGetKData通知AT准备行情数据，通过参数NoReturn判断是否需要返回文件名也就是
    AT是准备数据还是直接将数据写入本地文件
    如果是直接写入本地文件，则直接返回文件名
    这里的频数固定为1
    """
    cmd = 'AtraderGetKData'
    head = 'cmd="%s" Market="%s" Code="%s" KFrequency="%s" KFreNum="%d" BeginDate="%d" EndDate="%d" FilledUp="%d" FQ="%s" NoReturn="%d"' % (
     cmd, Market, Code, KFrequency, 1, BeginDate, EndDate, FilledUp, FQ, NoReturn)
    GVAR.g_ATraderSID.send_xml_cmd(head)
    if NoReturn is False:
        data = GVAR.g_ATraderSID.recv_data(recv_bytes=2048)
        matFile = from_data_get_file_name(data)
        raise_error_if_at_return_error(matFile)
        return matFile
    else:
        return ''


@trace_cmd
def at_send_ATraderGetTDPData(Market, Code, Date, FQ):
    """发送ATraderGetTDPData命令获取制定日期内的交易时间"""
    cmd = 'ATraderGetTDPData'
    head_tail = 'cmd="%s" Market="%s" Code="%s" Date="%d" FQ="%s"' % (cmd, Market, Code, Date, FQ)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=2048)
    matFile = from_data_get_file_name(data)
    raise_error_if_at_return_error(matFile)
    return matFile


@trace_cmd
def at_send_ATraderGetTradingTime(TargetList, askFreq, BeginDay, EndDay):
    """发送ATraderGetTradingTime命令获取制定日期内的交易时间"""
    cmd = 'ATraderGetTradingTime'
    head_tail = 'cmd="%s" freq="%s" beginD="%d" endD="%d"' % (cmd, askFreq, BeginDay, EndDay)
    middle = '\n'.join(['<item Market="%s" Code="%s"/>' % (t['Market'], t['Code']) for t in TargetList])
    GVAR.g_ATraderSID.send_xml_cmd(head_tail, middle)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=2048)
    matFile = from_data_get_file_name(data)
    raise_error_if_at_return_error(matFile)
    return matFile


@trace_cmd
def at_send_cmd_TraderGetFutureInfo(Market, Code):
    """获取除了标的除了行情数据信息外的其他基本信息的具体执行函数"""
    cmd = 'ATraderGetFutureInfo'
    info = dotdict()
    head_tail = 'cmd="%s" Market="%s" Code="%s"' % (cmd, Market, Code)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.1)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=226)
    info.Market = get_info_from_binary_array(data, 'Market')
    info.Code = get_info_from_binary_array(data, 'Code')
    info.Name = get_info_from_binary_array(data, 'Name')
    info.Type = get_info_from_binary_array(data, 'Type')
    info.Multiple = get_info_from_binary_array(data, 'Multiple')
    info.MinMove = get_info_from_binary_array(data, 'MinMove')
    info.TradingFeeOpen = get_info_from_binary_array(data, 'TradingFeeOpen')
    info.TradingFeeClose = get_info_from_binary_array(data, 'TradingFeeClose')
    info.TradingFeeCloseToday = get_info_from_binary_array(data, 'TradingFeeCloseToday')
    info.LongMargin = get_info_from_binary_array(data, 'LongMargin')
    info.ShortMargin = get_info_from_binary_array(data, 'ShortMargin')
    info.TargetMarket = get_info_from_binary_array(data, 'TargetMarket')
    info.TargetCode = get_info_from_binary_array(data, 'TargetCode')
    info.OptionType = get_info_from_binary_array(data, 'OptionType')
    info.CallOrPut = get_info_from_binary_array(data, 'CallOrPut')
    info.ListDate = get_info_from_binary_array(data, 'ListDate')
    info.LastTradingDate = get_info_from_binary_array(data, 'LastTradingDate')
    info.EndDate = get_info_from_binary_array(data, 'EndDate')
    info.ExerciseDate = get_info_from_binary_array(data, 'ExerciseDate')
    info.DeliveryDate = get_info_from_binary_array(data, 'DeliveryDate')
    info.CMUnit = get_info_from_binary_array(data, 'CMUnit')
    info.ExercisePrice = get_info_from_binary_array(data, 'ExercisePrice')
    info.MarginUnit = get_info_from_binary_array(data, 'MarginUnit')
    return info


@trace_cmd
def at_send_cmd_TraderPutLog(Handle, StrategyName, Log):
    """显示提示信息，函数调用后，理财牛主程序会在工具栏弹出内容为strNotice的提示框"""
    cmd = 'ATraderPutLog'
    head_tail = 'cmd="%s" Handle="%d" StrategyName="%s" Log="%s"' % (cmd, Handle, StrategyName, Log)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)


@trace_cmd
def at_send_cmd_ATraderStopBackTest(normalFinished):
    """向AT发送ATraderStopBackTest命令，标志回测结束，AT自动去读取记录文件"""
    cmd = 'ATraderStopBackTest'
    market0 = GVAR.g_ATraderStraInputInfo['TargetList'][0]['Market']
    code0 = GVAR.g_ATraderStraInputInfo['TargetList'][0]['Code']
    begin_date = GVAR.g_ATraderStraInputInfo['BeginDate']
    end_date = GVAR.g_ATraderStraInputInfo['EndDate']
    KFrequency = GVAR.g_ATraderStraInputInfo['KFrequency']
    KFreNum = GVAR.g_ATraderStraInputInfo['KFreNum']
    FQ = GVAR.g_ATraderStraInputInfo['FQ']
    match_obj = re.match('.* \\((.*)\\).*\\[(.*)\\]', sys.version)
    computer_info = match_obj.group(2)
    python_version = match_obj.group(1)
    middle = ''
    if normalFinished:
        try:
            if GVAR.atExistBackTestSetting():
                InitialCash = GVAR.g_AtraderSetInfo['InitialCash']
            else:
                InitialCash = 10000000.0
            validcash = GVAR.atGetTraderAccountMatrixValue(0, 0, GACV.ACMatrix_ValidCash) + GVAR.atGetTraderAccountMatrixValue(0, 0, GACV.ACMatrix_OrderFrozen)
            head_tail = 'cmd="%s" name="%s" initcash="%f" validcash="%f" market="%s" code="%s" begin="%d" end="%d" KFrequency="%s" kfrenum="%d" FQ="%s" OrderMode="%d" computer="%s" version="%s"' % (
             cmd, GVAR.g_ATraderStrategyName, InitialCash, validcash, market0, code0, begin_date, end_date,
             KFrequency, KFreNum, FQ, GVAR.g_ATraderAccountOrderMode, computer_info, python_version)
            middle = ''.join(['<targetIdx market="%s" code="%s" idx="%d"/>' % (target['Market'], target['Code'], idx) for idx, target in enumerate(GVAR.g_ATraderStraInputInfo.TargetList)])
        except Exception as e:
            head_tail = 'cmd="%s" name="%s" initcash="%f" validcash="%f" market="%s" code="%s" begin="%d" end="%d" kfrenum="%d" OrderMode="%d" computer="%s" version="%s"' % (
             cmd, GVAR.g_ATraderStrategyName, 0, 0, '', '', begin_date, end_date, 1, GVAR.g_ATraderAccountOrderMode,
             computer_info, python_version)

    else:
        head_tail = 'cmd="%s" name="%s" initcash="%f" validcash="%f" market="%s" code="%s" begin="%d" end="%d" kfrenum="%d" computer="%s" version="%s"' % (
         cmd, GVAR.g_ATraderStrategyName, 0, 0, '', '', 0, 0, normalFinished, computer_info, python_version)
        print('主动终止回测或者回测异常!!!\n')
    GVAR.g_ATraderSID.test_channel_available()
    GVAR.g_ATraderSID.send_xml_cmd(head_tail, middle)
    time.sleep(0.1)
    result = GVAR.g_ATraderSID.recv_data()


@trace_cmd
def at_send_cmd_ATraderGetTradingDays():
    """向AT发送ATraderGetTradingDays命令，沪深两市从开始设立到当前年份为止所有的交易日期【包含当前一整年的交易日期】"""
    cmd = 'ATraderGetTradingDays'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.2)
    data = GVAR.g_ATraderSID.recv_data_by_size()
    if len(data) < 1:
        raise ValueError(const_da.Enum_Const.ERROR_GET_DATA.value)
    date_count = int(get_real_data_from_byte_array(data[0:8], 1, 'd'))
    all_date = np.arange(date_count)
    for i in range(date_count):
        all_date[i] = int(get_real_data_from_byte_array(data[8 + i * 8:8 + i * 8 + 8], 1, 'd'))

    return all_date


@trace_cmd
def at_send_cmd_ATraderGetCodeList(block, **kwargs):
    """
    向AT发送ATraderGetCodeList命令，AT发回含有[Market 16 char],[Code 16 char],[Name 32 uint16],[BlockName 32 char],[Weight 1 double]
    """
    one_target_size = 136
    cmd = 'ATraderGetCodeList'
    date = kwargs.get('date', 0)
    head_tail = 'cmd="%s" block="%s" date ="%d"' % (cmd, block, date)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.2)
    data = GVAR.g_ATraderSID.recv_data()
    if len(data) < one_target_size:
        raise ValueError(const_da.Enum_Const.ERROR_GET_DATA.value)
    LoopTimes = int(np.floor(len(data) / one_target_size))
    result = {'IDPWeightArray': np.zeros((LoopTimes,), dtype=[('Market', '<U32'),
                        ('Code', '<U32'),
                        ('Name', '<U32'),
                        ('BlockName', '<U32'),
                        (
                         'Weight', np.float)])}
    for i, item in enumerate(result['IDPWeightArray']):
        forward_step = one_target_size * i
        item['Market'] = get_real_data_from_byte_array(data[0 + forward_step:16 + forward_step], 16, 's')
        item['Code'] = get_real_data_from_byte_array(data[16 + forward_step:32 + forward_step], 16, 's')
        item['Name'] = get_real_data_from_byte_array(data[32 + forward_step:96 + forward_step], 32, 'H')
        item['BlockName'] = get_real_data_from_byte_array(data[96 + forward_step:128 + forward_step], 32, 's')
        item['Weight'] = get_real_data_from_byte_array(data[128 + forward_step:136 + forward_step], 1, 'd')

    return result


@trace_cmd
def atSendCmdGetTradeAccountHandle(name):
    """发送ATraderSTTradeGetAccountHandle至ATcore，AT返回账户名对应的句柄"""
    cmd = 'ATraderSTTradeGetAccountHandle'
    head_tail = 'cmd="%s" name="%s"' % (cmd, name)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=8)
    Handle, = struct.unpack('!d', data[0:8])
    return np.fix(Handle)


@trace_cmd
def atSendCmdATraderSTTradeStopOrder(params):
    """
    发送 ATraderSTTradeStopOrder 指令
    :param params: dict
    """
    params = dotdict(params)
    cmd = 'ATraderSTTradeStopOrder'
    head_tail = ' cmd="{cmd}" StrategyName="{StrategyName}" Handle="{Handle}" Market="{Market}" Code="{Code}" Contracts="{Contracts}" StopGap="{StopGap}" OrderAct="{OrderAct}" OrderCtg="{OrderCtg}" targetPrice="{targetPrice}" targetOrder="{targetOrder}" StopBy="{StopBy}" StopType="{StopType}" TrailingStopGap="{TrailingStopGap}"  TrailingStopBy="{TrailingStopBy}" OrderTag="{OrderTag}"'.format(cmd=cmd, StrategyName=params.StrategyName, Handle=params.Handle, Market=params.Market, Code=params.Code, Contracts=params.Contracts, StopGap=params.StopGap, OrderAct=params.OrderAct, OrderCtg=params.OrderCtg, targetPrice=params.targetPrice, targetOrder=params.targetOrder, StopBy=params.StopBy, StopType=params.StopType, TrailingStopGap=params.TrailingStopGap, TrailingStopBy=params.TrailingStopBy, OrderTag=params.OrderTag)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    try:
        code = np.nan
        data = GVAR.g_ATraderSID.recv_data(recv_bytes=8)
        code = np.fix(get_real_data_from_byte_array(data[0:8], 1, 'd'))
    except Exception as e:
        write_syslog(traceback.format_exc(), level='error')

    return code


@trace_cmd
def atSendCmdGetCurMode():
    """发送ATraderGetCurMode命令获取AT当前运行状态，当前状态应该为0，如果不为空则报错"""
    cmd = 'ATraderGetCurMode'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=8)
    mode = get_real_data_from_byte_array(data[0:8], 1, 'd')
    return int(mode)


@trace_cmd
def atSendCmdIsAccountValid(handle):
    """Send command for checking account status"""
    cmd = 'ATraderIsAccountValid'
    head_tail = 'cmd="%s" Handle="%d"' % (cmd, handle)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=8)
    valid, = struct.unpack('!d', data[0:8])
    return np.fix(valid)


@trace_cmd
def atSendCmdCheckSubscribeNum(subscribeNum):
    """Send command for checking subscribe number"""
    cmd = 'ATraderCheckSubscribeNum'
    head_tail = 'cmd="%s" num="%d"' % (cmd, subscribeNum)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.1)
    result = GVAR.g_ATraderSID.recv_data()
    value = xml_tag_key_value(result, 'return', 'result')
    if value != 'true':
        raise Exception(xml_tag_key_value(result, 'return', 'errInfo'))


@trace_cmd
def atSendCmdGetCurTradeDate():
    """向AT发送ATraderGetCurTradeDate命令，返回距离当前日期最近的交易日期 格式为20170901"""
    cmd = 'ATraderGetCurTradeDate'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(1)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=8, ignore_error=False)
    CurTradeDate = np.fix(get_real_data_from_byte_array(data, 1, 'd'))
    return CurTradeDate


@trace_cmd
def atSendCmdTransTradeTimeToTradeDate(checkTime):
    cmd = 'ATraderTransTradeTimeToTradeDate'
    dt = UTILS_DT.matlab_float_time_to_datetime(checkTime)
    head_tail = 'cmd="%s" checkTime="%s"' % (cmd, dt.strftime('%Y%m%dT%H%M%S'))
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    data = GVAR.g_ATraderSID.recv_data(recv_bytes=8, ignore_error=False)
    tradeDate = np.fix(get_real_data_from_byte_array(data, 1, 'd'))
    return tradeDate


@trace_cmd
def atSendATraderSTTradeOperation(params):
    """
    :param params: dotdict类型，params.Handle 等价于 params['Handle'] ,包含了命令所需要的所有参数
    :return: float, orderID
    """
    cmd = 'ATraderSTTradeOperation'
    head_tail = 'cmd="%s" StrategyName="%s" Handle="%d" Market="%s" Code="%s" Price="%d" Contracts="%d" OrderAct="%s" OrderCtg="%s" OffsetFlag="%s" OrderTag="%s">\n' % (
     cmd,
     params.StrategyName,
     params.Handle,
     params.Market,
     params.Code,
     params.Price,
     params.Contracts,
     params.OrderAct,
     params.OrderCtg,
     params.OffsetFlag,
     params.OrderTag)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    recv = GVAR.g_ATraderSID.recv_data(recv_bytes=8)
    orderID = np.fix(get_real_data_from_byte_array(recv[0:8], 1, 'd'))
    return orderID


def IsTickDataExist(Market, Code, KFrequency, Date, FQ):
    """
    :return: 检查mat文件是否存在,存在返回文件路径，否则返回None  
    """
    fileLoc = os.path.join(GVAR.root_sub_dir('mat'), '%s_%s_%s_%d_%s.mat' % (KFrequency, Market, Code, Date, FQ))
    if os.path.exists(fileLoc):
        return fileLoc


def atClearMatFileIncludeCurTradeDate(matFile, Date):
    if matFile and os.path.exists(matFile):
        curTradeDate = atSendCmdGetCurTradeDate()
        if not Date or Date == curTradeDate:
            UTILS_UTIL.run_ignore_exception(os.remove, matFile)


def atClearMatFileIncludeZeroDate(matFile, Date):
    if matFile and os.path.exists(matFile) and np.logical_not(Date):
        UTILS_UTIL.run_ignore_exception(os.remove, matFile)


@trace_cmd
def at_send_ATraderStartBackTest(TargetList, KFrequency, KFreNum, BeginDate, EndDate, StrategyName):
    """发送ATraderStartBackTest命令,并处理返回结果"""
    cmd = 'ATraderStartBackTest'
    head_tail = 'cmd="%s" KFrequency="%s" KFreNum="%d" begin="%d" end="%d" StraName="%s"' % (
     cmd, KFrequency, KFreNum, BeginDate, EndDate, StrategyName)
    middle = '\n'.join(['<item Market="%s" Code="%s"/>' % (t['Market'], t['Code']) for t in TargetList])
    GVAR.g_ATraderSID.send_xml_cmd(head_tail, middle)
    time.sleep(1)
    result = GVAR.g_ATraderSID.recv_data()
    value = xml_tag_key_value(result, 'return', 'result')
    if value.lower() != 'true':
        raise Exception(xml_tag_key_value(result, 'return', 'errInfo'))


@trace_cmd
def atSendCmdStartRealTrade(params):
    cmd = 'ATraderStartRealTrade'
    head_tail = 'cmd="%s" KFrequency="%s" KFreNum="%d" begin="%d" StraName="%s"' % (cmd,
     params.KFrequency,
     params.KFreNum,
     params.BeginDate,
     params.StraName)
    itemMarket = '\n'.join(['<item Market="%s" Code="%s"/>' % (t['Market'], t['Code']) for t in params.TargetList])
    itemHandle = '\n'.join(['<item handle="%d"/>' % handle for handle in params.Handles])
    GVAR.g_ATraderSID.send_xml_cmd(head_tail, itemMarket + itemHandle)
    time.sleep(1)
    result = GVAR.g_ATraderSID.recv_data()
    value = xml_tag_key_value(result, 'return', 'result')
    if value.lower() != 'true':
        raise Exception(xml_tag_key_value(result, 'return', 'errInfo'))


@trace_cmd
def atSendCmdATraderGetTargetIns(Market, Code, BeginDate, EndDate):
    cmd = 'ATraderGetTargetIns'
    head_tail = 'cmd="%s" Market="%s" Code="%s" Begin="%d" End="%d"' % (cmd, Market, Code, BeginDate, EndDate)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.1)
    data = GVAR.g_ATraderSID.recv_data()
    codelist, pos, looptimes = [], 0, int(len(data) / 16)
    for i in range(looptimes):
        _code = get_real_data_from_byte_array(data[pos:pos + 8], 8, 's')
        _date = int(get_real_data_from_byte_array(data[pos + 8:pos + 16], 1, 'd'))
        codelist.append((_code, _date))
        pos += 16

    df = pd.DataFrame(codelist, columns=['Market', 'Date'])
    df['Market'] = df['Market'].str.decode('utf-8', errors='ignore')
    return df


@trace_cmd
def atSendCmdStopRealTrade():
    cmd = 'ATraderStopRealTrade'
    head_tail = 'cmd="%s" handle="%d" StraName="%s"' % (
     cmd, GVAR.g_ATraderAccountHandleArray[0], GVAR.g_ATraderStrategyName)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(1)
    GVAR.g_ATraderSID.recv_data()


@trace_cmd
def atSendCmdSubscribeAcc(IDList):
    cmd = 'ATraderSubscribeAccount'
    head_tail = 'cmd="%s"' % cmd
    middle = ''.join(['<item AccountID="%d"/>' % account for account in IDList])
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail, middle)
    time.sleep(0.1)


@trace_cmd
def atSendCmdUnsubscribeAcc(IDList):
    cmd = 'ATraderUnsubscribeAccount'
    head_tail = 'cmd="%s"' % cmd
    middle = ''.join(['<item AccountID="%d"/>' % account for account in IDList])
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail, middle)
    time.sleep(0.1)


@trace_cmd
def atSendCmdSubscribeIns(TargetList, KFrequency):
    atSendCmdCheckSubscribeNum(len(TargetList))
    cmd = 'ATraderSubscribeIns'
    head_tail = 'cmd="%s" freq="%s"' % (cmd, KFrequency)
    middle = ''.join(['<item Market="%s" Code="%s" Index="%d"/>\n' % (target['Market'], target['Code'], i) for i, target in enumerate(TargetList)])
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail, middle)
    time.sleep(0.1)


@trace_cmd
def atSendCmdUnsubscribeIns(IDList):
    cmd = 'ATraderUnsubscribeIns'
    head_tail = 'cmd="%s"' % cmd
    middle = '\n'.join(['<item Market="%s" Code="%s"/>' % (t['Market'], t['Code']) for t in IDList])
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail, middle)
    time.sleep(0.1)


def atSendCmdATraderKeepActive():
    cmd = 'ATraderKeepActive'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail)
    time.sleep(0.1)


@trace_cmd
def atSendCmdATraderRtNotifyReceived():
    """实时数据收到之后，发送确认命令"""
    cmd = 'ATraderRtNotifyReceived'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail)


@trace_cmd
def atSendCmdATraderAccountNotifyReceived():
    """实时账户数据收到之后，发送确认命令"""
    cmd = 'ATraderAccountNotifyReceived'
    head_tail = 'cmd="%s"' % cmd
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail)


@trace_cmd
def atSendCmdATraderSTGetAccountPosition(Handle, Market, Code, LongShort=''):
    """实盘运行时，发送ATraderSTGetAccountPosition命令获取指定账户中指定标的的持仓信息"""
    cmd = 'ATraderSTGetAccountPosition'
    if LongShort:
        head_tail = 'cmd="%s" Handle="%d" Market="%s" Code="%s" LongShort="%s"' % (cmd, Handle, Market, Code, LongShort)
    else:
        head_tail = 'cmd="%s" Handle="%d" Market="%s" Code="%s"' % (cmd, Handle, Market, Code)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    target_num = GVAR.g_ATraderSID.recv_data(recv_bytes=8)
    target_num = np.fix(get_real_data_from_byte_array(target_num[0:8], 1, 'd'))
    Position, Frozen, AvgPrice = (0, 0, 0)
    if target_num < 1:
        write_syslog('%s, Auto-Trade return bad data' % cmd, level='warn')
    else:
        all_data = GVAR.g_ATraderSID.recv_data(recv_bytes=72)
        Market = get_real_data_from_byte_array(all_data[0:16], 16, 's')
        Code = get_real_data_from_byte_array(all_data[16:32], 16, 's')
        Direction = get_real_data_from_byte_array(all_data[32:40], 8, 's')
        start_position = 40
        step_len = 8
        slices = [slice(step_len * i + start_position, step_len * (i + 1) + start_position) for i in range(4)]
        Position = get_real_data_from_byte_array(all_data[slices[0]], 1, 'd')
        Frozen = get_real_data_from_byte_array(all_data[slices[1]], 1, 'd')
        OpenPrice = get_real_data_from_byte_array(all_data[slices[2]], 1, 'd')
        HoldPrice = get_real_data_from_byte_array(all_data[slices[3]], 1, 'd')
        AvgPrice = HoldPrice
    return (Position, Frozen, AvgPrice)


@trace_cmd
def atSendCmdATraderAccountConfigTo(TargetList, Config, StrategyName, Handle):
    """cmd: ATraderAccountConfigTo """
    cmd = 'ATraderAccountConfigTo'
    head_tail = 'cmd="%s" StrategyName="%s" Handle="%d"' % (cmd, StrategyName, Handle)
    Middle = ''.join(['<item Market="%s" Code="%s" Config="%d" />\n' % (t['Market'], t['Code'], c) for c, t in zip(Config, TargetList)])
    GVAR.g_ATraderSIDCB.send_xml_cmd(head_tail, Middle)


@trace_cmd
def atSendCmdATraderCloseOperation(HandleIdx):
    """发送ATraderCloseOperation命令，平掉对应账户的所有持仓"""
    cmd = 'ATraderCloseOperation'
    head_tail = 'cmd="%s" Handle="%d"' % (cmd, GVAR.g_ATraderRealHandles[HandleIdx])
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    time.sleep(0.1)
    result = GVAR.g_ATraderSID.recv_data()


@trace_cmd
def atSendCmdGetAccountInfo(Handles):
    """获取账号信息"""
    cmd = 'ATraderSTGetAccountInfo'
    for Handle in Handles:
        head_tail = 'cmd="%s" Handle="%d"' % (cmd, Handle)
        GVAR.g_ATraderSID.send_xml_cmd(head_tail)
        data = GVAR.g_ATraderSID.recv_data(recv_bytes=40)
        if len(data) <= 40:
            GVAR.g_ATraderAccountInfo[Handle] = dotdict({'HandListCap': get_real_data_from_byte_array(data[0:8], 1, 'd'), 
             'ValidCash': get_real_data_from_byte_array(data[8:16], 1, 'd'), 
             'OrderFrozen': get_real_data_from_byte_array(data[16:24], 1, 'd'), 
             'MarginFrozen': get_real_data_from_byte_array(data[24:32], 1, 'd'), 
             'PositionProfit': get_real_data_from_byte_array(data[32:40], 1, 'd')})
        else:
            GVAR.g_ATraderAccountInfo[Handle] = dotdict({'HandListCap': 0, 
             'ValidCash': 0, 
             'OrderFrozen': 0, 
             'MarginFrozen': 0, 
             'PositionProfit': 0})
            write_syslog('ATraderSTGetAccountInfo get bad info', level='warn', trace_debug=False)


@trace_cmd
def atSendCmdCancelOrder(StrategyName, Handle, OrderID):
    """cmd ATraderCancelOrder"""
    cmd = 'ATraderCancelOrder'
    head_tail = 'cmd="%s" StrategyName="%s" Handle="%d" orderID="%d"' % (cmd, StrategyName, Handle, OrderID)
    GVAR.g_ATraderSID.send_xml_cmd(head_tail)
    result = GVAR.g_ATraderSID.recv_data()
    value = xml_tag_key_value(result, 'return', 'result')
    if value.lower() != 'true':
        raise Exception(xml_tag_key_value(result, 'return', 'errInfo'))


def atUpdateAccountInfo(Handle, m_AccInfo):
    """根据传入的字典更新账户信息，只在实时模式时使用"""
    if Handle in GVAR.g_ATraderAccountInfo:
        GVAR.g_ATraderAccountInfo[Handle] = m_AccInfo


def atGetAllSocketData():
    """实盘运行时，收取所有socket里的数据"""
    RtDataSize = 248
    sizeofOrderInfoMatlab_s = 160
    sizeofAccountDataTransMatlab_s = 48
    FreshList = []
    KFreshArray = np.array([])
    StopRun = False
    MTYPE_RT = 0
    MTYPE_ORDERINFO = 1
    MTYPE_REPLAYSTOP = 2
    MTYPE_KEEPACTIVE = 3
    MTYPE_ACCOUNTINFO = 4
    MTYPE_RT_MAT = 5
    MTYPE_KDATA = 6
    MTYPE_KDATA_MAT = 7
    KDataSize = 72
    all_data = GVAR.g_ATraderSIDCB.recv_data_by_size2()
    residue_len = len(all_data)
    residue_data = all_data
    while residue_len > 0:
        command_type = get_real_data_from_byte_array(residue_data[0:8], 1, 'd')
        current_data_len = int(get_real_data_from_byte_array(residue_data[8:16], 1, 'd'))
        residue_len = residue_len - 16
        residue_data = residue_data[16:]
        if command_type == MTYPE_RT:
            pass
        if np.mod(current_data_len, KDataSize) != 0:
            write_syslog('MTYPE_RT get wrong data length: %d' % current_data_len, level='warn')
            continue
            LoopTimes = current_data_len / RtDataSize
            for k in range(int(LoopTimes)):
                forward_step = RtDataSize * k
                temp_dict = dotdict()
                temp_dict.Market = get_real_data_from_byte_array(residue_data[0 + forward_step:16 + forward_step], 16, 's')
                temp_dict.Code = get_real_data_from_byte_array(residue_data[16 + forward_step:32 + forward_step], 16, 's')
                step_len = 8
                start_position = forward_step + 32
                slices = [slice(step_len * i + start_position, step_len * (i + 1) + start_position) for i in range(27)]
                temp_datas = [get_real_data_from_byte_array(residue_data[s], 1, 'd') for s in slices]
                temp_dict.rtIsbegin = temp_datas[0]
                temp_dict.rtTime = temp_datas[1]
                temp_dict.rtLastPrice = temp_datas[2]
                temp_dict.rtVolumeTick = temp_datas[3]
                temp_dict.rtVolume = temp_datas[4]
                temp_dict.rtTurnOver = temp_datas[5]
                temp_dict.rtOpenInt = temp_datas[6]
                temp_dict.rtBidPrice = np.array(temp_datas[7:12])
                temp_dict.rtBidVolume = np.array(temp_datas[12:17])
                temp_dict.rtAskPrice = np.array(temp_datas[17:22])
                temp_dict.rtAskVolume = np.array(temp_datas[22:27])
                FreshList.append(temp_dict)

            residue_len = residue_len - current_data_len
            residue_data = residue_data[current_data_len:]
            atSendCmdATraderRtNotifyReceived()
        else:
            if command_type == MTYPE_ORDERINFO:
                LoopTimes = current_data_len // sizeofOrderInfoMatlab_s
                flag_exist_pos = False
                pos = np.nan
                for k in range(LoopTimes):
                    forward_step = sizeofOrderInfoMatlab_s * k
                    temp_dict = dotdict()
                    temp_dict.dbAccHandleID = get_real_data_from_byte_array(residue_data[0 + forward_step:8 + forward_step], 1, 'd')
                    temp_dict.dbClientID = get_real_data_from_byte_array(residue_data[8 + forward_step:16 + forward_step], 1, 'd')
                    temp_dict.strStrategyName = get_real_data_from_byte_array(residue_data[16 + forward_step:48 + forward_step], 32, 's')
                    temp_dict.strMarket = get_real_data_from_byte_array(residue_data[48 + forward_step:64 + forward_step], 16, 's')
                    temp_dict.strCode = get_real_data_from_byte_array(residue_data[64 + forward_step:80 + forward_step], 16, 's')
                    step_len = 8
                    start_position = forward_step + 80
                    slices = [slice(step_len * i + start_position, step_len * (i + 1) + start_position) for i in range(10)]
                    temp_dict.tmCreate = get_real_data_from_byte_array(residue_data[slices[0]], 1, 'd')
                    temp_dict.tmFilled = get_real_data_from_byte_array(residue_data[slices[1]], 1, 'd')
                    temp_dict.eOrderAct = get_real_data_from_byte_array(residue_data[slices[2]], 1, 'd')
                    temp_dict.dbOrderCtg = get_real_data_from_byte_array(residue_data[slices[3]], 1, 'd')
                    temp_dict.dbOffsetFlag = get_real_data_from_byte_array(residue_data[slices[4]], 1, 'd')
                    temp_dict.dbOrderPrice = get_real_data_from_byte_array(residue_data[slices[5]], 1, 'd')
                    temp_dict.dbFilledPrice = get_real_data_from_byte_array(residue_data[slices[6]], 1, 'd')
                    temp_dict.dbVolume = get_real_data_from_byte_array(residue_data[slices[7]], 1, 'd')
                    temp_dict.dbVolumeTraded = get_real_data_from_byte_array(residue_data[slices[8]], 1, 'd')
                    temp_dict.eOrderStatus = get_real_data_from_byte_array(residue_data[slices[9]], 1, 'd')
                    pos = np.nan
                    flag_exist_pos = True
                    if GVAR.g_ATraderRealOrders.size > 0:
                        pos_1 = np.array(GVAR.g_ATraderRealOrders.loc['dbClientID'] == temp_dict.dbClientID)
                        pos_2 = np.array(GVAR.g_ATraderRealOrders.loc['dbAccHandleID'] == temp_dict.dbAccHandleID)
                        pos = pos_1 & pos_2
                        if ~np.any(pos):
                            pos = np.nan
                        if np.sum(pos) > 0:
                            GVAR.g_ATraderRealOrders.loc[('dbOrderPrice', pos)] = temp_dict.dbOrderPrice
                            GVAR.g_ATraderRealOrders.loc[('dbFilledPrice', pos)] = temp_dict.dbFilledPrice
                            GVAR.g_ATraderRealOrders.loc[('dbVolume', pos)] = temp_dict.dbVolume
                            GVAR.g_ATraderRealOrders.loc[('dbVolumeTraded', pos)] = temp_dict.dbVolumeTraded
                            GVAR.g_ATraderRealOrders.loc[('eOrderStatus', pos)] = temp_dict.eOrderStatus
                        else:
                            ls = list(GVAR.g_ATraderRealOrders.columns)
                            ls.append(-1)
                            pos = np.max(ls) + 1
                            shape0 = GVAR.g_ATraderRealOrders.shape[0]
                            GVAR.g_ATraderRealOrders[pos] = pd.Series(np.array([np.nan] * shape0), index=list(GVAR.g_ATraderRealOrders.index))
                            GVAR.g_ATraderRealOrders.loc[('dbAccHandleID', pos)] = temp_dict.dbAccHandleID
                            GVAR.g_ATraderRealOrders.loc[('dbClientID', pos)] = temp_dict.dbClientID
                            GVAR.g_ATraderRealOrders.loc[('strStrategyName', pos)] = temp_dict.strStrategyName
                            GVAR.g_ATraderRealOrders.loc[('strMarket', pos)] = temp_dict.strMarket
                            GVAR.g_ATraderRealOrders.loc[('strCode', pos)] = temp_dict.strCode
                            GVAR.g_ATraderRealOrders.loc[('tmCreate', pos)] = temp_dict.tmCreate
                            GVAR.g_ATraderRealOrders.loc[('tmFilled', pos)] = temp_dict.tmFilled
                            GVAR.g_ATraderRealOrders.loc[('eOrderAct', pos)] = temp_dict.eOrderAct
                            GVAR.g_ATraderRealOrders.loc[('dbOrderCtg', pos)] = temp_dict.dbOrderCtg
                            GVAR.g_ATraderRealOrders.loc[('dbOffsetFlag', pos)] = temp_dict.dbOffsetFlag
                            GVAR.g_ATraderRealOrders.loc[('dbOrderPrice', pos)] = temp_dict.dbOrderPrice
                            GVAR.g_ATraderRealOrders.loc[('dbFilledPrice', pos)] = temp_dict.dbFilledPrice
                            GVAR.g_ATraderRealOrders.loc[('dbVolume', pos)] = temp_dict.dbVolume
                            GVAR.g_ATraderRealOrders.loc[('dbVolumeTraded', pos)] = temp_dict.dbVolumeTraded
                            GVAR.g_ATraderRealOrders.loc[('eOrderStatus', pos)] = temp_dict.eOrderStatus

                if flag_exist_pos is True and np.isnan(pos) is False:
                    GVAR.g_ATraderLastChangeOrder = GVAR.g_ATraderRealOrders[pos].copy()
                atSendCmdATraderAccountNotifyReceived()
                residue_len = residue_len - current_data_len
                residue_data = residue_data[current_data_len:]
            else:
                if command_type == MTYPE_REPLAYSTOP:
                    StopRun = True
                    residue_len = residue_len - current_data_len
                    residue_data = residue_data[current_data_len:]
                else:
                    if command_type == MTYPE_KEEPACTIVE:
                        GVAR.g_ATraderLastHeartBeat = datetime.now()
                        residue_len = residue_len - current_data_len
                        residue_data = residue_data[current_data_len:]
                    else:
                        if command_type == MTYPE_ACCOUNTINFO:
                            start_position = 0
                            step_len = 8
                            temp_dict = dotdict({})
                            slices = [slice(step_len * i + start_position, step_len * (i + 1) + start_position) for i in range(6)]
                            Handle = get_real_data_from_byte_array(residue_data[slices[0]], 1, 'd')
                            temp_dict.HandListCap = get_real_data_from_byte_array(residue_data[slices[1]], 1, 'd')
                            temp_dict.ValidCash = get_real_data_from_byte_array(residue_data[slices[2]], 1, 'd')
                            temp_dict.OrderFrozen = get_real_data_from_byte_array(residue_data[slices[3]], 1, 'd')
                            temp_dict.MarginFrozen = get_real_data_from_byte_array(residue_data[slices[4]], 1, 'd')
                            temp_dict.PositionProfit = get_real_data_from_byte_array(residue_data[slices[5]], 1, 'd')
                            residue_len = residue_len - current_data_len
                            residue_data = residue_data[current_data_len:]
                            atUpdateAccountInfo(Handle, temp_dict)
                            atSendCmdATraderAccountNotifyReceived()
                        elif command_type == MTYPE_RT_MAT:
                            continue
        if command_type == MTYPE_KDATA:
            if np.mod(current_data_len, KDataSize) != 0:
                write_syslog('MTYPE_KDATA get wrong data length: %d' % current_data_len, level='warn')
                continue
                KROW = 9
                loopTimes = current_data_len // KDataSize
                arr = []
                for i in range(loopTimes * KROW):
                    _r = residue_data[i * 8:(i + 1) * 8]
                    if _r:
                        arr.append(get_real_data_from_byte_array(_r, 1, 'd'))
                    else:
                        break

                arr = np.asarray(arr).reshape(-1, KROW).T
                if KFreshArray.size < 1:
                    KFreshArray = arr
                else:
                    KFreshArray = np.append(KFreshArray, arr, axis=1)
                residue_len -= loopTimes * KROW * 8
                residue_data = residue_data[current_data_len:]
                if residue_len < 1:
                    return (
                     KFreshArray, StopRun)
            else:
                if command_type == MTYPE_KDATA_MAT:
                    pass
                else:
                    residue_len = 0
                    GVAR.g_ATraderSIDCB.recv_garbage_data(ignore_timeout=True)
                    write_syslog('not support command type={!r}, data={!r}'.format(command_type, all_data), level='warn')

    return (
     FreshList, StopRun)