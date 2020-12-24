# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/thermometer.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarDigitalArduino, SysVarAnalogArduinoUnipolar
__author__ = 'yoelk'
from instrumentino import cfg

class AnalogPinThermometer(SysCompArduino):

    def __init__(self, name, rangeT, pinInT, pinInVoltsMax, pinInVoltsMin):
        SysCompArduino.__init__(self, name, (
         SysVarAnalogArduinoUnipolar('T', rangeT, pinInT, None, name, 'Temperature', 'C', pinInVoltsMax=pinInVoltsMax, pinInVoltsMin=pinInVoltsMin),), 'measure the temperature')
        return


class AnalogPinThermometer_AD22103(AnalogPinThermometer):

    def __init__(self, name, pinInT):
        AnalogPinThermometer.__init__(self, name, [0, 100], pinInT, pinInVoltsMax=3.05, pinInVoltsMin=0.25)