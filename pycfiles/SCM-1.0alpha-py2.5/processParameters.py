# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/processParameters.py
# Compiled at: 2009-05-29 13:49:11
from superData import SuperData

class ProcessParameters(SuperData):
    """ data class which has material parameters for both particle phase
    and matrix phase
    """

    def __init__(self):
        SuperData.__init__(self)
        self.saved = False
        self.numSteps = 0
        self.selectedProcess = 0
        self.tempStart = 0
        self.tempFinal = 0
        self.strain = 0
        self.stress = 0