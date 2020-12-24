# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/pewatron.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarAnalogArduinoUnipolar
__author__ = 'yoelk'

class PewatronPressureSensor(SysCompArduino):

    def __init__(self, name, rangeP, pinInP):
        SysCompArduino.__init__(self, name, (
         SysVarAnalogArduinoUnipolar('P', rangeP, pinInP, None, name, 'Pressure', 'mbar', pinInVoltsMax=4.5, pinInVoltsMin=0.5),), 'monitor pressure')
        return