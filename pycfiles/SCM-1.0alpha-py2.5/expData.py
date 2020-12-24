# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/expData.py
# Compiled at: 2009-05-29 13:49:10
from superData import SuperData
import config

class ExpData(SuperData):
    """ data class having file names of experimental data and list of it.
    """

    def __init__(self):
        SuperData.__init__(self)
        self.expFile = ''
        self.expPh2File = ''
        self.flags['expData'] = False
        self.macroExpX = []
        self.macroExpY = []
        self.HKLExpX = {'Phase1': [], 'Phase2': [], 'TransPhase1': [], 'LongPhase1': [], 'RollingPhase1': [], 'TransPhase2': [], 'LongPhase2': [], 'RollingPhase2': []}
        self.HKLExpX_error = {'Phase1': [], 'Phase2': [], 'TransPhase1': [], 'LongPhase1': [], 'RollingPhase1': [], 'TransPhase2': [], 'LongPhase2': [], 'RollingPhase2': []}
        self.HKLExpY = []