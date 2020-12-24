# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTOC_GUI\styleMultiPlotGUI.py
# Compiled at: 2019-05-13 19:01:12
# Size of source mod 2**32: 1807 bytes
from PyQt5 import uic
from PyQt5 import QtWidgets
import os, sys
from .stylePlotGUI import plotStyler
import logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

class plotMultiStyler(QtWidgets.QDialog):

    def __init__(self, signalnames, plots=[], logger=None):
        super(plotMultiStyler, self).__init__()
        if getattr(sys, 'frozen', False):
            packagedir = os.path.dirname(sys.executable) + '/RTOC/RTOC_GUI'
        else:
            packagedir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(packagedir + '/ui/stylePlotDialog.ui', self)
        self.setCallbacks()
        self.logger = logger
        self.plots = plots
        self.lineColor = None
        self.fillLevel = None
        self.symbolColor = None
        self.listWidget.clear()
        self.styler = plotStyler(plots[0])
        self.stylerLayout.addWidget(self.styler)
        for signal in signalnames:
            text = '.'.join(signal)
            self.listWidget.addItem(text)

    def setCallbacks(self):
        self.cancelButton.clicked.connect(self.close)
        self.styleSelectedButton.clicked.connect(self.styleSelected)
        self.styleAllButton.clicked.connect(self.styleAll)

    def styleAll(self):
        for plot in self.plots:
            self.styler.setStyleAction(plot)

        self.close()

    def styleSelected(self):
        for selectedSignal in self.listWidget.selectedItems():
            signalname = selectedSignal.text()
            idx = self.logger.database.getSignalID(signalname.split('.')[0], signalname.split('.')[1])
            if idx != -1:
                self.styler.setStyleAction(self.plots[idx])