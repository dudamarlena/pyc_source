# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC5160_eval.py
# Compiled at: 2020-01-29 04:58:46
# Size of source mod 2**32: 5403 bytes
"""
Created on 24.10.2019

@author: JM
"""
import PyTrinamic.ic.TMC5160.TMC5160 as TMC5160

class TMC5160_eval(TMC5160):
    __doc__ = '\n    This class represents a TMC5160 Evaluation board.\n\n    Communication is done over the TMCL commands writeMC and readMC. An\n    implementation without TMCL may still use this class if these two functions\n    are provided properly. See __init__ for details on the function\n    requirements.\n    '

    def __init__(self, connection, moduleID=1):
        """
        Parameters:
            connection:
                Type: class
                A class that provides the neccessary functions for communicating
                with a TMC5160. The required functions are
                    connection.writeMC(registerAddress, value, moduleID)
                    connection.readMC(registerAddress, moduleID, signed)
                for writing/reading to registers of the TMC5160.
            moduleID:
                Type: int, optional, default value: 1
                The TMCL module ID of the TMC5160. This ID is used as a
                parameter for the writeMC and readMC functions.
        """
        TMC5160.__init__(self, moduleID)
        self._TMC5160_eval__connection = connection
        self._MODULE_ID = moduleID
        self.APs = _APs

    def writeRegister(self, registerAddress, value, moduleID=None):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC5160_eval__connection.writeMC(registerAddress, value, moduleID)

    def readRegister(self, registerAddress, moduleID=None, signed=False):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC5160_eval__connection.readMC(registerAddress, moduleID, signed)

    def getAxisParameter(self, apType, axis):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        return self._TMC5160_eval__connection.axisParameter(apType, axis)

    def setAxisParameter(self, apType, axis, value):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        self._TMC5160_eval__connection.setAxisParameter(apType, axis, value)

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self._TMC5160_eval__connection.rotate(motor, value, moduleID=(self._MODULE_ID))

    def stop(self, motor):
        self._TMC5160_eval__connection.stop(motor, moduleID=(self._MODULE_ID))

    def moveTo(self, motor, position, velocity=None):
        if velocity:
            if velocity != 0:
                self.setAxisParameter(self.APs.MaxVelocity, motor, velocity)
        self._TMC5160_eval__connection.move(0, motor, position, moduleID=(self._MODULE_ID))


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
    THIGH = 23
    VDCMIN = 24
    HighSpeedChopperMode = 27
    HighSpeedFullstepMode = 28
    MeasuredSpeed = 29
    I_scale_analog = 33
    internal_Rsense = 34
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
    smartEnergyActualCurrent = 180
    smartEnergyStallVelocity = 181
    smartEnergyThresholdSpeed = 182
    RandomTOffMode = 184
    ChopperSynchronization = 185
    PWMThresholdSpeed = 186
    PWMGrad = 187
    PWMAmplitude = 188
    PWMFrequency = 191
    PWMAutoscale = 192
    FreewheelingMode = 204
    LoadValue = 206
    EncoderPosition = 209
    EncoderResolution = 210