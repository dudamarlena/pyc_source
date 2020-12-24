# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\winpython\python-2.7.10.amd64\lib\site-packages\pySAXS\guisaxs\qt\plugin.py
# Compiled at: 2017-08-24 10:00:30


class pySAXSplugin:
    menu = 'Plugins'
    subMenu = 'sub Plugins'
    subMenuText = ''
    icon = None
    toolbar = False

    def __init__(self, parent, selectedData=None, noGUI=False):
        self.parent = parent
        self.data_dict = parent.data_dict
        self.selectedData = selectedData
        self.printTXT = parent.printTXT
        self.redrawTheList = parent.redrawTheList
        self.Replot = self.parent.Replot
        self.ListOfDatasChecked = parent.ListOfDatasChecked
        self.noGUI = noGUI
        self.workingdirectory = parent.workingdirectory
        self.referencedataSubtract = parent.referencedataSubtract

    def execute(self):
        """
        execute
        """
        pass

    def setParameters(self, parametersDict):
        """
        want to execut with no gui,
        some parameters need to be transmitted
        parametersDict : dictionnary of parameters {'wavelength':1.542, ...}
        """
        for key in parametersDict.keys():
            setattr(self, key, parametersDict[key])

    def setSelectedData(self, name):
        self.selectedData = name

    def setWorkingDirectory(self, filename):
        self.parent.setWorkingDirectory(filename)

    def getWorkingDirectory(self):
        return self.parent.workingdirectory