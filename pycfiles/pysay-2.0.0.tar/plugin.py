# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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