# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\dashboard.py
# Compiled at: 2020-03-24 13:24:33
# Size of source mod 2**32: 4170 bytes
"""
Author: Kapil Duwadi
Version: 0.0.1
"""
from ResultDashboard.Dashboard.CIFFDashboard import CreateApp
import dash
from ResultDashboard.ReadersContainer import *
from ResultDashboard.pyProcessData import ProcessData
from ResultDashboard.ProcessForInitialAssessment import ProcessLoadProfile
from ResultDashboard.template import TomlDictForDashboard
import os, toml

class DashApp:
    __doc__ = ' A class for developing interactive dashboard. \n    \n    :param SettingsTomlFilePath: A path to .toml file containg all the settings necessary for visualization\n    :type SettingsTomlFilePath: str\n    :return: html file\n    '

    def __init__(self, SettingsTomlFilePath):
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
        """ A function to launch dashboard.Takes no parameters.

        :return: http: address to visualize results
        """
        return self.app.run_server(debug=True, port=8060)


class Template:
    __doc__ = ' A class which generates template for visualization process including .toml file\n    \n    :param FolderPath: A folder path where you want to create project\n    :type FolderPath: str\n    :param FeederName: A name of feeder for which you want to create a project\n    :type FeederName: str\n    '

    def __init__(self, FolderPath, FeederName):
        FolderName = 'DashboardTemplate'
        os.mkdir(os.path.join(FolderPath, FolderName))
        os.mkdir(os.path.join(FolderPath, FolderName, 'Projects'))
        print('{} created successfully'.format(os.path.join(FolderPath, FolderName, 'Projects')))
        os.mkdir(os.path.join(FolderPath, FolderName, 'Projects', FeederName))
        print('{} created successfully'.format(os.path.join(FolderPath, FolderName, 'Projects', FeederName)))
        Feederpath = os.path.join(FolderPath, FolderName, 'Projects', FeederName)
        FolderCategory = ['CoordinateCSVFiles', 'CSVDataFiles', 'CSVDataFilesForAdvancedPV', 'InitialAssessment', 'PVConnection']
        for folder in FolderCategory:
            os.mkdir(os.path.join(Feederpath, folder))
            print('{} created successfully'.format(os.path.join(Feederpath, folder)))

        os.mkdir(os.path.join(Feederpath, 'PVConnection', 'Base'))
        print('{} created successfully'.format(os.path.join(Feederpath, 'PVConnection', 'Base')))
        os.mkdir(os.path.join(Feederpath, 'PVConnection', 'ExtraData'))
        print('{} created successfully'.format(os.path.join(Feederpath, 'PVConnection', 'ExtraData')))
        TomlFileContent = TomlDictForDashboard().ReturnDict()
        TomlFileContent['Project Path'] = os.path.join(FolderPath, 'Projects')
        TomlFileContent['Active Project'] = FeederName
        TomlStrings = toml.dumps(TomlFileContent)
        TextFile = open(os.path.join(Feederpath, 'settings.toml'), 'w')
        TextFile.write(TomlStrings)
        TextFile.close()
        print('{} file created successfully'.format(os.path.join(Feederpath, 'settings.toml')))