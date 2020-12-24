# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/emco.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarDigitalArduino, SysVarAnalogArduinoUnipolar
__author__ = 'yoelk'
from instrumentino import cfg

class EmcoHvSypplyCA_Series_Input12V(SysCompArduino):

    def __init__(self, name, rangeV, pinInV, pinOutV=None, ctlV_I2cDac=None):
        if ctlV_I2cDac:
            voltageVar = SysVarAnalogArduinoUnipolar('V', rangeV, pinInV, None, name, 'Voltage', 'V', I2cDac=ctlV_I2cDac)
        else:
            voltageVar = SysVarAnalogArduinoUnipolar('V', rangeV, pinInV, pinOutV, name, 'Voltage', 'V')
        SysCompArduino.__init__(self, name, (
         voltageVar,), 'monitor/change High Voltage variables')
        return


class EmcoCA05P(EmcoHvSypplyCA_Series_Input12V):

    def __init__(self, name, pinInV, pinOutV=None, ctlV_I2cDac=None):
        EmcoHvSypplyCA_Series_Input12V.__init__(self, name, [0, 500], pinInV, pinOutV=pinOutV, ctlV_I2cDac=ctlV_I2cDac)