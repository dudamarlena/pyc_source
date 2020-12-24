# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/pins.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino, SysVarDigitalArduino
__author__ = 'yoelk'

class DigitalPins(SysCompArduino):

    def __init__(self, name, digiVars=()):
        SysCompArduino.__init__(self, name, digiVars, 'turn on/off Arduino digital pins')


class AnalogPins(SysCompArduino):

    def __init__(self, name, analogVars=()):
        SysCompArduino.__init__(self, name, analogVars, 'set Arduino analog pins')