# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/parker.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarAnalogArduinoUnipolar
__author__ = 'yoelk'

class ParkerPressureController(SysCompArduino):

    def __init__(self, name, rangeP, pinInP, pinOutP=None, highFreqPWM=False, units='psi', I2cDac=None):
        SysCompArduino.__init__(self, name, (
         SysVarAnalogArduinoUnipolar('P', rangeP, pinInP, pinOutP, name, 'Pressure', units, highFreqPWM=highFreqPWM, I2cDac=I2cDac),), 'monitor/change pressure')