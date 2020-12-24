# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/matParameters.py
# Compiled at: 2009-05-29 13:49:18
from superData import SuperData

class MatParameters(SuperData):
    """ data class which has material parameters
    """

    def __init__(self):
        SuperData.__init__(self)
        self.saved = False
        self.nameMaterial = ''
        self.typeCrystal = 0
        self.elastic = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.thermal = [1.2e-05, 1.2e-05, 1.2e-05, 0.0, 0.0, 0.0]
        self.voce = [[0.3, 0.3, 1, 0.01], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
         [
          0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.selectedSystems = []
        self.numSystems = 0