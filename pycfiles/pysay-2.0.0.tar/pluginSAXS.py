# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\pluginSAXS.py
# Compiled at: 2018-08-23 04:06:23
from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import dlgAbsoluteI
from PyQt5 import QtGui, QtCore, QtWidgets
classlist = [
 'pluginSAXSAbsolute']

class pluginSAXSAbsolute(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'SAXS'
    subMenuText = 'Absolute Intensities'
    icon = 'expand_selection.png'
    toolbar = True

    def execute(self):
        label = self.selectedData
        if self.selectedData is None:
            QtWidgets.QMessageBox.information(self.parent, 'pySAXS', 'No data are selected', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            params = self.data_dict[label].parameters
            if params is not None:
                params.printout = self.printTXT
            reference = self.parent.referencedata
            self.childSaxs = dlgAbsoluteI.dlgAbsolute(self, saxsparameters=params, datasetname=label, printout=self.printTXT, referencedata=reference, backgrounddata=self.parent.backgrounddata)
            self.childSaxs.show()
            return