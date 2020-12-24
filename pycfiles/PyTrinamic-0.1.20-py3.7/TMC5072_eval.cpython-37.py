# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC5072_eval.py
# Compiled at: 2019-12-05 04:43:16
# Size of source mod 2**32: 3772 bytes
"""
Created on 20.09.2019

@author: JM
"""
import PyTrinamic.ic.TMC5072.TMC5072 as TMC5072

class TMC5072_eval(TMC5072):
    __doc__ = '\n    This class represents a TMC5072 Evaluation board\n    '

    def __init__(self, connection):
        TMC5072.__init__(self, channel=0)
        self._TMC5072_eval__connection = connection
        self.APs = _APs

    def writeRegister(self, registerAddress, value, channel=0):
        if channel != 0:
            raise ValueError
        return self._TMC5072_eval__connection.writeMC(registerAddress, value)

    def readRegister(self, registerAddress, channel=0, signed=False):
        if channel != 0:
            raise ValueError
        return self._TMC5072_eval__connection.readMC(registerAddress, signed=signed)

    def getAxisParameter(self, apType, axis):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        return self._TMC5072_eval__connection.axisParameter(apType, axis)

    def setAxisParameter(self, apType, axis, value):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        self._TMC5072_eval__connection.setAxisParameter(apType, axis, value)

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self._TMC5072_eval__connection.rotate(motor, value)

    def stop(self, motor):
        self._TMC5072_eval__connection.stop(motor)

    def moveTo(self, motor, position, velocity=None):
        if velocity:
            if velocity != 0:
                self.setAxisParameter(self.APs.MaxVelocity, motor, velocity)
        self._TMC5072_eval__connection.move(0, motor, position)


class _APs:
    TargetPosition = 0
    ActualPosition = 1
    TargetVelocity = 2
    ActualVelocity = 3
    MaxVelocity = 4
    MaxAcceleration = 5
    MaxCurrent = 6
    StandbyCurrent = 7
    PositionReachedFlag = 8
    RightEndstop = 10
    LeftEndstop = 11
    AutomaticRightStop = 12
    AutomaticLeftStop = 13
    SW_MODE = 14
    A1 = 15
    V1 = 16
    MaxDeceleration = 17
    D1 = 18
    StartVelocity = 19
    StopVelocity = 20
    RampWaitTime = 21
    smartEnergyThresholdSpeed = 22
    THIGH = 23
    VDCMIN = 24
    HighSpeedFullstepMode = 28
    MicrostepResolution = 140
    ChopperBlankTime = 162
    ConstantTOffMode = 163
    DisableFastDecayComparator = 164
    ChopperHysteresisEnd = 165
    ChopperHysteresisStart = 166
    TOff = 167
    SEIMIN = 168
    SECDS = 169
    smartEnergyHysteresis = 170
    SECUS = 171
    smartEnergyHysteresisStart = 172
    SG2FilterEnable = 173
    SG2Threshold = 174
    VSense = 179
    smartEnergyActualCurrent = 180
    smartEnergyStallVelocity = 181
    RandomTOffMode = 184
    ChopperSynchronization = 185
    LoadValue = 206
    EncoderPosition = 209
    EncoderResolution = 210