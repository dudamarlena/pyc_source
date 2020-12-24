# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/pid_thermostat.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarDigitalArduino, SysVarAnalogArduinoUnipolar, SysVarPidRelayArduino
__author__ = 'yoelk'
from instrumentino import cfg

class PidControlledThermostat(SysCompArduino):

    def __init__(self, name, rangeT, pinInT, pinOutRelay, sensorVoltsMin, sensorVoltsMax, pidVar, windowSizeMs, kp, ki, kd):
        self.varEnable = SysVarDigitalArduino('enable', None, name, PreSetFunc=self.PreEditEnable)
        self.pidRelayVar = SysVarPidRelayArduino('T', rangeT, pidVar, windowSizeMs, kp, ki, kd, pinInT, pinOutRelay, name, 'Temperature', 'C', pinInVoltsMin=sensorVoltsMin, pinInVoltsMax=sensorVoltsMax)
        SysCompArduino.__init__(self, name, (
         self.pidRelayVar, self.varEnable), 'control a heating element through a relay to keep the temperature set')
        return

    def FirstTimeOnline(self):
        super(PidControlledThermostat, self).FirstTimeOnline()

    def PreEditEnable(self, value):
        self.pidRelayVar.Enable(value == 'on')