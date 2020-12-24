# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\run_mode\trader_run_real_trade.py
# Compiled at: 2018-08-27 20:45:24
# Size of source mod 2**32: 5923 bytes
import traceback, types, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR, atquant.socket_ctrl.base_socket as base_socket, atquant.socket_ctrl.tool_box_command as tb_command
from atquant.account.account_checker import AccountChecker
from atquant.utils.arg_checker import ArgumnetChecker
from atquant.utils.arg_checker import verify_that, apply_rule, ATInvalidArgument
from atquant.utils.internal_exception import ToolBoxErrors
from atquant.utils.internal_util import SimpleTimer, trace_time
from atquant.utils.logger import write_syslog, write_userlog
from atquant.utils.user_class import dotdict
from .run_mode_common import atRealTradeInitV2, atTradeLoopV2

@apply_rule(verify_that('StrategyName').is_instance_of(str), verify_that('TradeFun').is_instance_of(types.FunctionType), verify_that('varFunParameter').is_instance_of(tuple), verify_that('AccountList').is_instance_of(list).is_empty_or_not(empty=False), verify_that('TargetList').is_instance_of(list).is_empty_or_not(empty=False), verify_that('KFrequency').is_valid_frequency(), verify_that('KFreNum').is_instance_of(int).is_greater_or_equal_than(1), verify_that('BeginDate').is_valid_date().is_future_date(), verify_that('FQ').is_valid_fq())
def traderRunRealTradeV2(StrategyName, TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, FQ, *args):
    try:
        try:
            write_syslog('Begin Prepare traderRunRealTradeV2', level='info', trace_debug=True)
            TradeFun = trace_time(TradeFun)
            if KFrequency.lower() == 'tick':
                raise NotImplementedError('tick data not support now!')
            if GVAR.g_ATraderRegisterRealK:
                ToolBoxErrors.atmode_notsupport_error(const_da.Enum_Const.ERROR_NOTSUPPORT_WHEN_REALMODE.value)
            if len(AccountList) < 1:
                raise ValueError(const_da.Enum_Const.ERROR_EMPTY_ACCOUNTLIST_REALMODE.value)
            ArgumnetChecker.is_algorithm_func_and_args(traderRunRealTradeV2.__name__, *args)
            AccountChecker.check_run_real_trade_account(AccountList)
            base_socket.atClearAllTCPIP()
            AlgoTradeFunction = []
            TargetList = GVAR.atRemoveInvalidTarget(TargetList)
            tb_command.atSendCmdCheckSubscribeNum(len(TargetList))
            mode = tb_command.atSendCmdGetCurMode()
            ToolBoxErrors.at_mode_error(mode, 'realtrade')
            GVAR.atResetRealMode()
            GVAR.atResetBackTestMode()
            GVAR.atResetAlgoOrderSignal()
            GVAR.atResetDailyCloseTimeSetting()
            GVAR.atResetOrderMode()
            GVAR.g_ATraderRegIndiCalc = []
            GVAR.g_ATraderRegKDataInfo = []
            GVAR.generatingStrategyName(StrategyName)
        except Exception as e:
            write_syslog(traceback.format_exc(), level='error', console=traceback.format_exc())
            return

    finally:
        write_syslog('End Prepare traderRunRealTradeV2', level='info', trace_debug=True)

    try:
        try:
            use_time = SimpleTimer('traderRunRealTradeV2', 'sec')
            write_syslog('Begin RealTradeInitV2', level='info', trace_debug=True)
            atRealTradeInitV2(TargetList, KFrequency, KFreNum, BeginDate, 0, FQ)
            write_syslog('End RealTradeInitV2', level='info', trace_debug=True)
            write_syslog('Begin TradeFunInit', level='info', trace_debug=True)
            TradeFun(True, False, varFunParameter)
            write_syslog('End TradeFunInit', level='info', trace_debug=True)
            GVAR.atEnterRealMode()
            GVAR.atEnterDataFreshMode()
            tb_command.atSendCmdSubscribeAcc(GVAR.g_ATraderAccountHandleArray)
            bLowSec = True if KFrequency.lower() in ('tick', 'sec') else False
            tb_command.atSendCmdStartRealTrade(dotdict({'KFrequency': 'min' if bLowSec else KFrequency, 
             'KFreNum': 1 if bLowSec else KFreNum, 
             'BeginDate': BeginDate, 
             'Handles': GVAR.g_ATraderAccountHandleArray, 
             'TargetList': TargetList, 
             'StraName': GVAR.g_ATraderStrategyName}))
            tb_command.atSendCmdSubscribeIns(TargetList, KFrequency)
            write_syslog('Begin TradeLoopV2', level='info', trace_debug=True)
            atTradeLoopV2(TradeFun, varFunParameter, TargetList, KFrequency, KFreNum, AlgoTradeFunction)
            write_syslog('End TradeLoopV2', level='info', trace_debug=True)
        except ATInvalidArgument as e:
            write_userlog(traceback.format_exc(), level='error', console=traceback.format_exc())
            return
        except Exception as e:
            write_syslog(traceback.format_exc(), level='error', console=traceback.format_exc())
            return

    finally:
        msg = '实盘总耗时 %d 秒' % use_time.total()
        write_userlog(msg, level='info', console=None)
        print(msg)
        write_syslog('Begin Clean', level='info', trace_debug=True)
        clear_up()
        write_syslog('End Clean', level='info', trace_debug=True)


def clear_up():
    try:
        tb_command.atSendCmdUnsubscribeIns(GVAR.g_ATraderStraInputInfo.TargetList)
        tb_command.atSendCmdUnsubscribeAcc(GVAR.g_ATraderAccountHandleArray)
        tb_command.atSendCmdStopRealTrade()
        GVAR.g_ATraderCurTickInfo = dotdict({})
        GVAR.g_ATraderAccountInfo = dotdict({})
    except Exception as e:
        write_syslog(traceback.format_exc(), level='error', console=str(e))