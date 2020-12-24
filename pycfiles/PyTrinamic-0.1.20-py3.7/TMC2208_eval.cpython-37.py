# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC2208_eval.py
# Compiled at: 2019-12-05 04:37:02
# Size of source mod 2**32: 3336 bytes
"""
Created on 17.10.2019

@author: JM
"""
import PyTrinamic.ic.TMC2208.TMC2208 as TMC2208

class TMC2208_eval(TMC2208):
    __doc__ = '\n    This class represents a TMC2208 Evaluation board.\n\n    Communication is done over the TMCL commands writeDRV and readDRV. An\n    implementation without TMCL may still use this class if these two functions\n    are provided properly. See __init__ for details on the function\n    requirements.\n    '

    def __init__(self, connection, moduleID=1):
        """
        Parameters:
            connection:
                Type: class
                A class that provides the neccessary functions for communicating
                with a TMC2208. The required functions are
                    connection.writeDRV(registerAddress, value, moduleID)
                    connection.readDRV(registerAddress, moduleID, signed)
                for writing/reading to registers of the TMC2208.
            moduleID:
                Type: int, optional, default value: 1
                The TMCL module ID of the TMC2208. This ID is used as a
                parameter for the writeDRV and readDRV functions.
        """
        TMC2208.__init__(self, moduleID)
        self._TMC2208_eval__connection = connection
        self._MODULE_ID = moduleID
        self.APs = _APs

    def writeRegister(self, registerAddress, value, moduleID=None):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC2208_eval__connection.writeDRV(registerAddress, value, moduleID)

    def readRegister(self, registerAddress, moduleID=None, signed=False):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC2208_eval__connection.readDRV(registerAddress, moduleID, signed)

    def getAxisParameter(self, apType, axis):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        return self._TMC2208_eval__connection.axisParameter(apType, axis)

    def setAxisParameter(self, apType, axis, value):
        if not 0 <= axis < self.MOTORS:
            raise ValueError('Axis index out of range')
        self._TMC2208_eval__connection.setAxisParameter(apType, axis, value)

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self._TMC2208_eval__connection.rotate(motor, value, moduleID=(self._MODULE_ID))

    def stop(self, motor):
        self._TMC2208_eval__connection.stop(motor, moduleID=(self._MODULE_ID))

    def moveTo(self, motor, position, velocity=None):
        if velocity:
            if velocity != 0:
                self.setAxisParameter(self.APs.MaxVelocity, motor, velocity)
        self._TMC2208_eval__connection.move(0, motor, position, moduleID=(self._MODULE_ID))


class _APs:
    TargetPosition = 0
    ActualPosition = 1
    TargetVelocity = 2
    ActualVelocity = 3
    MaxVelocity = 4
    MaxAcceleration = 5