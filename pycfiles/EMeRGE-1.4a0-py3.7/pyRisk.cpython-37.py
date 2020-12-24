# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DSSRiskAnalyzer\pyRisk.py
# Compiled at: 2020-03-15 13:07:28
# Size of source mod 2**32: 2955 bytes
from ResultDashboard.Dashboard.DSSRiskAnalyzer.SubModulesContainer.ReadersContainer import *
from ResultDashboard.Dashboard.DSSRiskAnalyzer.pyRunTimeSeriesPowerFlow import OpenDSS
import os

class RunRiskAnalysis:

    def __init__(self, SettingsTomlFilePath):
        SimulationSettings = ReadFromFile(SettingsTomlFilePath)
        print('<-------------Running Risk Analaysis on "{}" feeder------------>'.format(SimulationSettings['Active_Feeder']))
        ExtraDataFilesDirectory = os.path.join(SimulationSettings['Project path'], SimulationSettings['Active_Feeder'], 'ExtraData')
        ExtraDataFilesDataStoredByIndicator = {}
        for fileindicator, filename in SimulationSettings['FileNames'].items():
            ExtraDataFilesDataStoredByIndicator[fileindicator] = ReadFromFile(os.path.join(ExtraDataFilesDirectory, filename))

        DSSFilePathDirectory = os.path.join(SimulationSettings['Project path'], SimulationSettings['Active_Feeder'], 'DSSScenarios')
        ExportFolderPath = os.path.join(SimulationSettings['Project path'], SimulationSettings['Active_Feeder'], 'Exports')
        if not os.path.exists(ExportFolderPath):
            os.mkdir(ExportFolderPath)
        CategoryFolderPath = os.path.join(ExportFolderPath, SimulationSettings['Active_Scenario'])
        if not os.path.exists(CategoryFolderPath):
            os.mkdir(CategoryFolderPath)
        for DSSScenario in os.listdir(DSSFilePathDirectory):
            print('Running Simulation for {} scenario'.format(DSSScenario))
            ExportPath = os.path.join(CategoryFolderPath, DSSScenario)
            DSSpath = os.path.join(DSSFilePathDirectory, DSSScenario, SimulationSettings['DSSfilename'])
            a = OpenDSS(DSSpath, SimulationSettings, ExtraDataFilesDataStoredByIndicator, ExportPath)
            del a

        print('Analysis complete !!!')


if __name__ == '__main__':
    CategoryPath = 'C:\\Users\\KDUWADI\\Desktop\\NREL_Projects\\CIFF-TANGEDCO\\TANGEDCO\\SoftwareTools\\Distribution_Metric_Computing_Tool\\Projects\\GWC\\AnalysisScenarios'
    for category in os.listdir(CategoryPath):
        SimulationSettingsTomlFilePath = os.path.join(CategoryPath, category, 'settings.toml')
        RunRiskAnalysis(SimulationSettingsTomlFilePath)