# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/mks.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarAnalogArduinoUnipolar, SysVarDigitalArduino
__author__ = 'yoelk'
from instrumentino import cfg

class MKSMassFlowController(SysCompArduino):

    def __init__(self, name, pinInPercent, pinOutPercent, pinOutClose=None, I2cDac=None):
        if I2cDac:
            controlVar = SysVarAnalogArduinoUnipolar('Flow', [0, 100], pinInPercent, None, name, 'Flow percentage', '%', self.PreEditPercent, I2cDac=I2cDac)
        else:
            controlVar = SysVarAnalogArduinoUnipolar('Flow', [0, 100], pinInPercent, pinOutPercent, name, 'Flow percentage', '%', self.PreEditPercent, highFreqPWM=True)
        SysCompArduino.__init__(self, name, (
         controlVar,), 'monitor/change gas flow')
        self.pinOutClose = pinOutClose
        if self.pinOutClose != None:
            self.varClose = SysVarDigitalArduino('close', pinOutClose, name)
        return

    def FirstTimeOnline(self):
        if self.pinOutClose != None:
            self.GetController().PinModeOut(self.varClose.pin)
        return super(MKSMassFlowController, self).FirstTimeOnline()

    def PreEditPercent(self, value):
        if self.pinOutClose != None:
            if value == 0:
                self.varClose.Set('off')
            else:
                self.varClose.Set('on')
        return