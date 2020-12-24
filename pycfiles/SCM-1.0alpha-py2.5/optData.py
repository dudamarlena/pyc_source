# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/optData.py
# Compiled at: 2009-05-29 13:49:11
from superData import *

class OptData(SuperData):
    """ data class for the optimization
    """

    def __init__(self):
        SuperData.__init__(self)
        self.nameAlgorithm = 'leastsq'
        self.data['func'] = 'default'
        self.data['xtol'] = 1.49e-08
        self.data['ftol'] = 1.49e-08
        self.data['maxFunc'] = 100
        self.data['fullOutput'] = 1
        self.data['expData'] = 'macro'
        self.voceFlag = [
         [
          0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.lowVoce = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.highVoce = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
        self.flags['range'] = False
        self.flags['optData'] = False
        self.flags['optAlgorithm'] = False