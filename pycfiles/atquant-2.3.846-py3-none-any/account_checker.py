# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\account\account_checker.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 3624 bytes
import sys, numpy as np, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR, atquant.socket_ctrl.tool_box_command as tb_command
from atquant.utils.internal_exception import ToolBoxErrors

class AccountChecker:

    @classmethod
    def check_run_back_test_account(cls, accounts):
        """
        检查回测账户是否合法
        :param accounts: list
        :return: 返回 GVAR.g_ATraderAccountHandleArray 
        """
        function_name = sys._getframe().f_code.co_name
        GVAR.g_ATraderAccountHandleArray = [-1] * len(accounts)
        for i, account in enumerate(accounts):
            _acc = tb_command.atSendCmdGetTradeAccountHandle(account)
            if _acc < 1:
                raise ValueError(function_name + ' 账户信息 ' + account + ' 不存在')
            else:
                valid = tb_command.atSendCmdIsAccountValid(_acc)
                if valid == 0:
                    raise ToolBoxErrors.not_support_error(function_name + const_da.Enum_Const.ERROR_ACCOUNT_INVALID.value)
                if 888888 != _acc and 666666 != _acc:
                    raise ToolBoxErrors.not_support_error(function_name + const_da.Enum_Const.ERROR_ACCOUNT_BACKTEST.value)
            GVAR.g_ATraderAccountHandleArray[i] = _acc

        return GVAR.g_ATraderAccountHandleArray

    @classmethod
    def check_run_real_trade_account(cls, accounts):
        """
        检查回测账户是否合法
        :param accounts: list
        :return: 返回 GVAR.g_ATraderAccountHandleArray 
        """
        function_name = sys._getframe().f_code.co_name
        GVAR.g_ATraderAccountHandleArray = [
         -1] * len(accounts)
        GVAR.g_ATraderRealHandles = np.zeros((len(accounts),))
        for i, account in enumerate(accounts):
            _acc = tb_command.atSendCmdGetTradeAccountHandle(account)
            if _acc < 1:
                raise ValueError(function_name + ' 账户信息 ' + account + ' 不存在')
            else:
                valid = tb_command.atSendCmdIsAccountValid(_acc)
                if valid == 0:
                    raise ToolBoxErrors.not_support_error(function_name + const_da.Enum_Const.ERROR_ACCOUNT_INVALID.value)
                if 888888 == _acc or 666666 == _acc:
                    raise ToolBoxErrors.not_support_error(function_name + const_da.Enum_Const.ERROR_ACCOUNT_REALMODE.value)
            GVAR.g_ATraderRealHandles[i] = _acc
            GVAR.g_ATraderAccountHandleArray[i] = _acc

        return GVAR.g_ATraderAccountHandleArray

    @classmethod
    def check_run_replay_account(cls, accounts):
        """
        检查回测账户是否合法
        :param accounts: list
        :return: 返回 GVAR.g_ATraderAccountHandleArray 
        """
        function_name = sys._getframe().f_code.co_name
        GVAR.g_ATraderAccountHandleArray = [-1] * len(accounts)
        GVAR.g_ATraderRealHandles = np.zeros((len(accounts),))
        for i, account in enumerate(accounts):
            _acc = tb_command.atSendCmdGetTradeAccountHandle(account)
            if _acc < 1:
                raise ValueError(function_name + ' 账户信息 ' + account + ' 不存在')
            if 888888 != _acc and 666666 != _acc:
                raise ToolBoxErrors.not_support_error(function_name + const_da.Enum_Const.ERROR_ACCOUNT_BACKTEST.value)
            GVAR.g_ATraderAccountHandleArray[i] = _acc
            GVAR.g_ATraderRealHandles[i] = _acc

        return GVAR.g_ATraderAccountHandleArray