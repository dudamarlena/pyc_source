# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\modules\TMCM_0010_OPC.py
# Compiled at: 2019-09-16 10:04:04
# Size of source mod 2**32: 915 bytes
"""
Created on 01.01.2019

@author: ED
"""

class TMCM_0010_OPC(object):
    __doc__ = ' brake chopper parameter '
    AP_SupplyVoltage = 0
    AP_Enable = 1
    AP_VoltageLimit = 2
    AP_Hysteresis = 3
    AP_LowerVoltageLimit = 4
    AP_Active = 5
    AP_MainLoopsPerSecond = 200
    AP_UsbLoopsPerSecond = 201

    def __init__(self, connection):
        self.connection = connection

    def showConfiguration(self):
        print('Brake chopper configuration:')
        print('\tenabled:       ' + str(self.connection.axisParameter(self.AP_Enable, 0)))
        print('\tvoltage limit: ' + str(self.connection.axisParameter(self.AP_VoltageLimit, 0) / 10) + 'V')
        print('\thysteresis:    ' + str(self.connection.axisParameter(self.AP_Hysteresis, 0) / 10) + 'V')