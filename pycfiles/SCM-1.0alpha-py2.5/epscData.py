# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/epscData.py
# Compiled at: 2009-05-29 13:49:11
from matParameters import MatParameters
from processParameters import ProcessParameters
from optData import OptData
from expData import ExpData
from superData import SuperData
from generalData import GeneralData
import config

class EpscData(SuperData):
    """class which is the main data structure of EPSC. It has several members
    which are experimental data, material data, and model parameters.
    """

    def __init__(self):
        SuperData.__init__(self)
        self.generalData = GeneralData()
        self.matParam = {}
        self.matParam['Phase1'] = MatParameters()
        self.matParam['2Phase1'] = MatParameters()
        self.matParam['2Phase2'] = MatParameters()
        self.textureFileNum = 1
        self.processParam = ProcessParameters()
        self.processDataSaved = False
        self.expData = ExpData()
        self.optData = OptData()
        self.phaseNum = 201
        self.phaseName = ''
        self.flagRun = False
        self.isAltered = False
        self.diffractionDataSaved = False
        self.textureDataSaved = False
        self.flagFromFile = False
        self.numDiffractionData = {'Phase1_exp': 0, 'Phase2_exp': 0, 'Phase1': 0, 'Phase2': 0, 'LongPhase1_exp': 0, 'LongPhase1': 0, 
           'LongPhase2': 0, 'TransPhase1': 0, 'TransPhase1_exp': 0, 'TransPhase2': 0, 
           'RollingPhase1': 0, 'RollingPhase1_exp': 0, 'RollingPhase2': 0}
        self.listDiffractionData = {'Phase1_exp': [], 'Phase2_exp': [], 'Phase1': [], 'Phase2': [], 'LongPhase1_exp': [], 'LongPhase1': [], 'LongPhase2': [], 'TransPhase1': [], 'TransPhase1_exp': [], 'TransPhase2': [], 'RollingPhase1': [], 'RollingPhase1_exp': [], 'RollingPhase2': []}