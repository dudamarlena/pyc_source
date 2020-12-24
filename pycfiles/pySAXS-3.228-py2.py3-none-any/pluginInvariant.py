# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\pluginInvariant.py
# Compiled at: 2017-08-30 07:40:25
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy
from pySAXS.LS import LSusaxs
from pySAXS.guisaxs.dataset import *
from pySAXS.guisaxs.qt import plugin
from pySAXS.LS import invariant
from pySAXS.guisaxs.qt import dlgInvariant
classlist = [
 'pluginInvariant']

class pluginInvariant(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'Calculate Invariant'
    subMenuText = 'invariant'
    icon = 'arrow-step-over.png'

    def execute(self):
        label = self.selectedData
        if self.selectedData is None:
            QtWidgets.QMessageBox.information(self.parent, 'pySAXS', 'No data are selected', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            self.childSaxs = dlgInvariant.dlgInvariant(self.parent, datasetname=label, printout=self.printTXT)
            self.childSaxs.show()
            return