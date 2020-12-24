# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\template.py
# Compiled at: 2020-03-24 13:23:41
# Size of source mod 2**32: 534 bytes


class TomlDictForDashboard:

    def __init__(self):
        self.toml_dict = {'Project Path':'C:\\Users\\KDUWADI\\Desktop\\VisualizingInDashboard\\Projects', 
         'Active Project':'GWC', 
         'Time Step (min)':15, 
         'ClassicalPVTotalSimulationMinute':525600, 
         'AdvancedPVTotalSimulationMinute':44640, 
         'ClassicalPVMWh':7008, 
         'AdvancedPVMWh':595.2}

    def ReturnDict(self):
        return self.toml_dict