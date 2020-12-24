# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\pluginAbsoluteAll.py
# Compiled at: 2018-10-03 10:21:10
"""
author : Olivier Tache
(C) CEA 2015
"""
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import dlgAbsoluteI

class AbsoluteAll(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'SAXS'
    subMenuText = 'Absolute all'
    icon = 'expand_selection.png'

    def execute(self):
        datalist = self.ListOfDatasChecked()
        label = self.selectedData
        if self.selectedData is None:
            QtWidgets.QMessageBox.information(self.parent, 'pySAXS', 'No data are selected', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            params = self.data_dict[label].parameters
            if params is not None:
                params.printout = self.printTXT
            reference = self.parent.referencedata
            self.referenceValue = self.parent.referenceValue
            self.childSaxs = dlgAbsoluteI.dlgAbsolute(self, saxsparameters=params, datasetname=label, printout=self.printTXT, referencedata=reference, backgrounddata=self.parent.backgrounddata, datasetlist=datalist, referenceValue=self.referenceValue)
            self.childSaxs.show()
            return