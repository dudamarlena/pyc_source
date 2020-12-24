# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\utils\internal_exception.py
# Compiled at: 2018-08-27 20:45:27
# Size of source mod 2**32: 2725 bytes
import atquant.data.const_data as const_da

class ToolBoxErrors:

    class NotSupportError(Exception):
        pass

    class AtModeNotSupportError(Exception):
        pass

    class DataDownloadError(Exception):
        pass

    @classmethod
    def unexpect_switch_error(cls, type):
        """
        :param type: 'orderact', 'stopgap', 'stoporder', 'runmode', 'fq', 'kfrequency'
        :return: raise NotImplementedError()
        """
        if type == 'orderact':
            cls.not_support_error('not support orderact type ,expect (OrderAct_Buy,OrderAct_Sell)')
        else:
            if type == 'stopgap':
                cls.not_support_error('not support stopgap type ,expect (StopGapType_Point,StopGapType_Percent)')
            else:
                if type == 'stoporder':
                    cls.not_support_error('not support stoporder type ,expect (StopOrderType_Loss, StopOrderType_Profit,StopOrderType_Trailing)')
                else:
                    if type == 'runmode':
                        cls.not_support_error('not support run mode expect (BackTest, RealTrade and Replay)')
                    else:
                        if type == 'fq':
                            cls.not_support_error('not support FQ type, expect(NA,FWard,BWard),NA:不复权,FWard:前复权,BWard:后复权')
                        elif type == 'kfrequency':
                            cls.not_support_error('not support KFrequency type, expect(min,day,sec,tick)')

    @classmethod
    def at_mode_error(cls, mode, modetype):
        """
        对指定mode抛出异常
        :param mode: int型
        :param modetype: 支持 'backtest', 'backreplay','realtrade'
        :return: 
        """
        if modetype in ('backtest', 'backreplay'):
            if mode == 1:
                cls.atmode_notsupport_error(const_da.Enum_Const.ERROR_MODE_ONE.value)
            else:
                if mode == 2:
                    cls.atmode_notsupport_error(const_da.Enum_Const.ERROR_MODE_TWO.value)
                elif mode == 3:
                    cls.atmode_notsupport_error(const_da.Enum_Const.ERROR_MODE_THREE.value)
        else:
            if modetype == 'realtrade':
                if mode == 1:
                    cls.atmode_notsupport_error(const_da.Enum_Const.ERROR_MODE_ONE.value)
            elif mode == 2:
                cls.atmode_notsupport_error(const_da.Enum_Const.ERROR_MODE_TWO.value)

    @classmethod
    def not_support_error(cls, msg):
        raise cls.NotSupportError(msg)

    @classmethod
    def data_download_error(cls, msg):
        raise cls.DataDownloadError(msg)

    @classmethod
    def atmode_notsupport_error(cls, msg):
        raise cls.AtModeNotSupportError(msg)