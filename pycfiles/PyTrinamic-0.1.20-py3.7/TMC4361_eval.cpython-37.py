# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC4361_eval.py
# Compiled at: 2019-12-20 04:14:42
# Size of source mod 2**32: 4075 bytes
"""
Created on 07.11.2019

@author: JM
"""
import PyTrinamic.ic.TMC4361.TMC4361 as TMC4361

class TMC4361_eval(TMC4361):

    def __init__(self, connection, moduleID=1):
        self._TMC4361_eval__connection = connection
        self.APs = _APs
        TMC4361.__init__(self, channel=0)

    def register(self):
        return self.TMC4361.register()

    def variants(self):
        return self.TMC4361.variants()

    def maskShift(self):
        return self.TMC4361.maskShift()

    def ic(self):
        return self.TMC4361

    def writeRegister(self, registerAddress, value, channel=0):
        if channel != 0:
            raise ValueError
        return self._TMC4361_eval__connection.writeMC(registerAddress, value)

    def readRegister(self, registerAddress, channel=0, signed=False):
        if channel != 0:
            raise ValueError
        return self._TMC4361_eval__connection.readMC(registerAddress, signed=signed)

    def getAxisParameter(self, apType, axis):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        return self._TMC4361_eval__connection.axisParameter(apType, axis)

    def setAxisParameter(self, apType, axis, value):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        self._TMC4361_eval__connection.setAxisParameter(apType, axis, value)

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self._TMC4361_eval__connection.rotate(motor, value)

    def stop(self, motor):
        self._TMC4361_eval__connection.stop(motor)

    def moveTo(self, motor, position, velocity=None):
        if velocity:
            if velocity != 0:
                self.setAxisParameter(self.APs.MaxVelocity, motor, velocity)
        self._TMC4361_eval__connection.move(0, motor, position)


class _APs:
    TargetPosition = 0
    ActualPosition = 1
    TargetVelocity = 2
    ActualVelocity = 3
    MaxVelocity = 4
    MaxAcceleration = 5
    PositionReachedFlag = 8
    RampType = 14
    StartVelocity = 15
    AStart = 16
    MaxDeceleration = 17
    VBreak = 18
    DFinal = 19
    StopVelocity = 20
    DSTOP = 21
    BOW1 = 22
    BOW2 = 23
    BOW3 = 24
    BOW4 = 25
    VirtualStopLeft = 26
    VirtualStopRight = 27
    CLGammaVMin = 108
    CLGammaVMax = 109
    CLMaxGamma = 110
    CLBeta = 111
    CLOffset = 112
    CLCurrentMin = 113
    CLCurrentMax = 114
    CLCorrectionVelocityP = 115
    CLCorrectionVelocityI = 116
    CLCorrectionVelIClip = 116
    CL_CorrectionVelDVClock = 116
    CL_Correction_VelDVClip = 119
    CLUpscaleDelay = 120
    CLDownscaleDelay = 121
    CLCorrectionPositionP = 124
    CLMaxCorrectionTolerance = 125
    CLStartUp = 126
    CLFlag = 129
    MeasuredEncoderSpeed = 132
    CLInitFlag = 133
    EncoderDeviation = 134
    EncVelDelay = 136
    EncVelFilter = 137
    FilterUpdateTime = 138
    BoostCurrent = 200
    EncoderPosition = 209
    MaxEncoderDeviation = 212
    PowerDownDelay = 214