# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Main.py
# Compiled at: 2020-03-12 18:42:50
# Size of source mod 2**32: 1581 bytes
"""
Author: Kapil Duwadi
Version: 0.0.1
"""
from ResultDashboard.Dashboard.CIFFDashboard import CreateApp
import dash
from ResultDashboard.ReadersContainer import *
from pyProcessData import ProcessData
from ResultDashboard.ProcessForInitialAssessment import ProcessLoadProfile

class DashApp:

    def __init__(self):
        SettingsTomlFilePath = 'C:\\Users\\KDUWADI\\Desktop\\VisualizingInDashboard\\Projects\\settings.toml'
        self.DashboardSettings = ReadFromFile(SettingsTomlFilePath)
        self.DataObject = ProcessData(self.DashboardSettings, 'Classical')
        self.DataObjectAdvancedPV = ProcessData((self.DashboardSettings), 'Advanced', DataFolderName='CSVDataFilesForAdvancedPV')
        self.DataObjectInitialAssessment = ProcessLoadProfile(self.DashboardSettings)
        self.app = dash.Dash(__name__, meta_tags=[{'name':'viewport',  'content':'width=device-width, initial-scale=1'}])
        self.app.config['suppress_callback_exceptions'] = True
        self.DashApp = CreateApp(self.app, self.DashboardSettings, self.DataObject, self.DataObjectAdvancedPV, self.DataObjectInitialAssessment)
        self.app.layout = self.DashApp.layout()
        self.DashApp.Callbacks()

    def Launch(self):
        return self.app.run_server(debug=True, port=8060)