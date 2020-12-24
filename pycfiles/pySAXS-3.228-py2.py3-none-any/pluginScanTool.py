# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\pluginScanTool.py
# Compiled at: 2017-08-30 07:43:51
"""
author : Olivier Tache
(C) CEA 2015
"""
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