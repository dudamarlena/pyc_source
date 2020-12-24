# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC5130_eval.py
# Compiled at: 2019-09-16 10:04:04
# Size of source mod 2**32: 2241 bytes
"""
Created on 09.01.2019

@author: LK, ED, LH
"""
import PyTrinamic.ic.TMC5130.TMC5130 as TMC5130

class TMC5130_eval(TMC5130):
    __doc__ = '\n    This class represents a TMC5130 Evaluation board.\n\n    Communication is done over the TMCL commands writeMC and readMC. An\n    implementation without TMCL may still use this class if these two functions\n    are provided properly. See __init__ for details on the function\n    requirements.\n    '
    _TMC5130_eval__PIN_MAP = [
     (2, 15),
     (3, 22),
     (4, 23),
     (5, 24),
     (7, 25),
     (8, 9),
     (9, 10),
     (23, 4),
     (24, 6),
     (25, 5),
     (26, 30),
     (27, 29),
     (28, 28)]

    def __init__(self, connection, moduleID=1):
        """
        Parameters:
            connection:
                Type: class
                A class that provides the neccessary functions for communicating
                with a TMC5130. The required functions are
                    connection.writeMC(registerAddress, value, moduleID)
                    connection.readMC(registerAddress, moduleID, signed)
                for writing/reading to registers of the TMC5130.
            moduleID:
                Type: int, optional, default value: 1
                The TMCL module ID of the TMC5130. This ID is used as a
                parameter for the writeMC and readMC functions.
        """
        TMC5130.__init__(self, moduleID)
        self._TMC5130_eval__connection = connection
        self._MODULE_ID = moduleID

    def writeRegister(self, registerAddress, value, moduleID=None):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC5130_eval__connection.writeMC(registerAddress, value, moduleID)

    def readRegister(self, registerAddress, moduleID=None, signed=False):
        if not moduleID:
            moduleID = self._MODULE_ID
        return self._TMC5130_eval__connection.readMC(registerAddress, moduleID, signed)