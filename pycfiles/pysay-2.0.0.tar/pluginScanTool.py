# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\pluginScanTool.py
# Compiled at: 2017-08-30 07:43:51
__doc__ = '\nauthor : Olivier Tache\n(C) CEA 2015\n'
import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import scanPlot
from pySAXS.guisaxs import dataset
import pySAXS
from time import sleep
import numpy
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
classlist = [
 'SCTool']

class SCTool(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'SPEC Tool'
    subMenuText = 'Scan Plot'
    icon = 'magnifier.png'

    def execute(self):
        self.dlg = scanPlot.scanPlot()
        self.dlg.show()