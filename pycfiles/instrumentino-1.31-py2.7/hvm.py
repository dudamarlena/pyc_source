# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/hvm.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarDigitalArduino, SysVarAnalogArduinoUnipolar
__author__ = 'yoelk'
from instrumentino import cfg

class HvmSubMiniHighVoltage(SysCompArduino):

    def __init__(self, name, rangeV, rangeI, pinEnable, activeHigh, pinInV, pinInI, pinOutV, highFreqPWM=False):
        self.activeHigh = activeHigh
        self.varEnable = SysVarDigitalArduino('enable', pinEnable, name)
        SysCompArduino.__init__(self, name, (
         SysVarAnalogArduinoUnipolar('V', rangeV, pinInV, pinOutV, name, 'Voltage', 'kV', self.PreEditV, highFreqPWM=highFreqPWM, pinInVoltsMax=1),
         SysVarAnalogArduinoUnipolar('I', rangeI, pinInI, None, name, 'Current', 'uA', highFreqPWM=highFreqPWM, pinInVoltsMax=1)), 'monitor/change High Voltage variables')
        return

    def FirstTimeOnline(self):
        self.GetController().PinModeOut(self.varEnable.pin)
        super(HvmSubMiniHighVoltage, self).FirstTimeOnline()

    def PreEditV(self, value):
        if value != 0:
            self.varEnable.Set('on' if self.activeHigh else 'off')
        else:
            self.varEnable.Set('off' if self.activeHigh else 'on')


class HvmSMHV05100(HvmSubMiniHighVoltage):

    def __init__(self, name, pinEnable, activeHigh, pinInV, pinInI, pinOutV, highFreqPWM=False):
        HvmSubMiniHighVoltage.__init__(self, name, [0, 10], [0, 100], pinEnable, activeHigh, pinInV, pinInI, pinOutV, highFreqPWM=highFreqPWM)


class HvmSMHV05100N(HvmSubMiniHighVoltage):

    def __init__(self, name, pinEnable, activeHigh, pinInV, pinInI, pinOutV, highFreqPWM=False):
        HvmSubMiniHighVoltage.__init__(self, name, [-10, 0], [0, 100], pinEnable, activeHigh, pinInV, pinInI, pinOutV, highFreqPWM=highFreqPWM)