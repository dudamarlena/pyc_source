# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/generalData.py
# Compiled at: 2009-05-29 13:49:11
from superData import *

class GeneralData(SuperData):
    """ data class having general data.
    """

    def __init__(self):
        SuperData.__init__(self)
        self.saved = False
        self.volFracPhase1 = 0.0
        self.volFracPhase2 = 0.0
        self.materialFile = {'Phase1': '', '2Phase1': '', '2Phase2': ''}
        self.textureFile = {'Phase1': '', '2Phase1': '', '2Phase2': ''}
        self.diffractionFile = {'Phase1': '', '2Phase1': '', '2Phase2': ''}
        self.processFiles = []
        self.numProcessFiles = 1