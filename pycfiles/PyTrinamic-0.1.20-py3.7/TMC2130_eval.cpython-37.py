# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC2130_eval.py
# Compiled at: 2019-12-05 04:35:23
# Size of source mod 2**32: 4918 bytes
"""
Created on 14.10.2019

@author: JM
"""
import PyTrinamic.ic.TMC2130.TMC2130 as TMC2130

class TMC2130_eval(TMC2130):
    __doc__ = '\n    This class represents a TMC2130 Evaluation board.\n\n    Communication is done over the TMCL commands writeDRV and readDRV. An\n    implementation without TMCL may still use this class if these two functions\n    are provided properly. See __init__ for details on the function\n    requirements.\n    '

    def __init__(self, connection, moduleID=1):
        """
        Parameters:
            connection:
                Type: class
                A class that provides the neccessary functions for communicating
                with a TMC2130. The required functions are
                    connection.writeDRV(registerAddress, value, moduleID)
                    connection.readDRV(registerAddress, moduleID, signed)
                for writing/reading to registers of the TMC2130.
            moduleID:
                Type: int, optional, default value: 1
                The TMCL module ID of the TMC2130. This ID is used as a
                parameter for the writeDRV and readDRV functions.
        """
        TMC2130.__init__(self, moduleID)
        self._TMC2130_eval__connection = connection
        self._MODULE_ID = moduleID
        self.APs = _APs

    def writeRegister(self, registerAddress, value, moduleID=None):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC2130_eval__connection.writeDRV(registerAddress, value, moduleID)

    def readRegister(self, registerAddress, moduleID=None, signed=False):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC2130_eval__connection.readDRV(registerAddress, moduleID, signed)

    def getAxisParameter(self, apType, axis):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        return self._TMC2130_eval__connection.axisParameter(apType, axis)

    def setAxisParameter(self, apType, axis, value):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        self._TMC2130_eval__connection.setAxisParameter(apType, axis, value)

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self._TMC2130_eval__connection.rotate(motor, value, moduleID=(self._MODULE_ID))

    def stop(self, motor):
        self._TMC2130_eval__connection.stop(motor, moduleID=(self._MODULE_ID))

    def moveTo(self, motor, position, velocity=None):
        if velocity:
            if velocity != 0:
                self.setAxisParameter(self.APs.MaxVelocity, motor, velocity)
        self._TMC2130_eval__connection.move(0, motor, position, moduleID=(self._MODULE_ID))


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
    THIGH = 23
    VDCMIN = 24
    HighSpeedFullstepMode = 26
    HighSpeedChopperMode = 27
    internal_Rsense = 28
    MeasuredSpeed = 29
    StepDirSource = 50
    StepDirFrequency = 51
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