# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgInvariant.py
# Compiled at: 2019-10-29 07:05:01
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import pySAXS.LS.SAXSparametersXML as SAXSparameters, sys, pySAXS
from pySAXS.tools import isNumeric
from pySAXS.tools import filetools
from pySAXS.guisaxs.dataset import *
from pySAXS.LS import invariant
import os

class dlgInvariant(QtWidgets.QDialog):

    def __init__(self, parent, datasetname='', printout=None):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgInvariant.ui', self)
        self.datasetname = datasetname
        self.parentwindow = parent
        self.workingdirectory = self.parentwindow.getWorkingDirectory()
        self.parent = parent
        self.data_dict = self.parent.data_dict
        self.printout = parent.printTXT
        self.DPQ = self.datasetname + ' invariant low q'
        self.data_dict[self.DPQ] = dataset(self.DPQ, self.data_dict[self.datasetname].q, self.data_dict[self.datasetname].i, comment='invariant low q', type='calculated', parent=[
         self.datasetname])
        self.DGQ = self.datasetname + ' invariant high q'
        self.data_dict[self.DGQ] = dataset(self.DGQ, self.data_dict[self.datasetname].q, self.data_dict[self.datasetname].i, comment='invariant high q', type='calculated', parent=[
         self.datasetname])
        self.q = self.data_dict[self.datasetname].q
        self.i = self.data_dict[self.datasetname].i
        self.qmini = self.q[0]
        self.qmaxi = self.q[(-1)]
        self.radius = 300.0
        self.invariant = invariant.invariant(self.q, self.i, radius=self.radius, printout=self.printTXT)
        self.B = self.invariant.B
        self.data_dict[self.DPQ].q = self.invariant.LowQq
        self.data_dict[self.DPQ].i = self.invariant.LowQi
        self.data_dict[self.DGQ].q = self.invariant.HighQq
        self.data_dict[self.DGQ].i = self.invariant.HighQi
        self.parent.redrawTheList()
        self.parent.Replot()
        self.ConstructUI()
        self.calculateAll()
        self.ui.buttonBox.clicked.connect(self.click)

    def ConstructUI(self):
        self.ui.labelDataset.setText(self.datasetname)
        self.UpdateResults()
        self.ui.edtQmin.setText(str(self.qmini))
        self.ui.edtQmin.textChanged.connect(self.onTextEdited)
        self.ui.edtQmax.setText(str(self.qmaxi))
        self.ui.edtQmax.textChanged.connect(self.onTextEdited)
        self.ui.edtRadius.setText(str(self.radius))
        self.ui.edtRadius.textChanged.connect(self.onTextEdited)
        self.ui.edtB.setText(str(self.B))
        self.ui.edtB.textChanged.connect(self.onTextEdited)
        self.ui.edtP1.setReadOnly(True)
        self.ui.edtP1.setStyleSheet('color: blue')
        self.ui.edtP2.setReadOnly(True)
        self.ui.edtP2.setStyleSheet('color: blue')
        self.ui.edtP3.setReadOnly(True)
        self.ui.edtP3.setStyleSheet('color: blue')
        self.ui.edtInvariant.setReadOnly(True)
        self.ui.edtInvariant.setStyleSheet('color:red')
        self.ui.edtVolume.setReadOnly(True)
        self.ui.edtVolume.setStyleSheet('color:red')
        self.ui.edtDiameter.setReadOnly(True)
        self.ui.edtDiameter.setStyleSheet('color:red')

    def UpdateResults(self):
        self.ui.edtP1.setText(str(self.invariant.P1))
        self.ui.edtP2.setText(str(self.invariant.P2))
        self.ui.edtP3.setText(str(self.invariant.P3))
        self.ui.edtInvariant.setText(str(self.invariant.invariant))
        self.ui.edtVolume.setText(str(self.invariant.volume))
        self.ui.edtDiameter.setText(str(self.invariant.diameter))

    def calculateAll(self):
        self.invariant.calculate(self.radius, self.qmini, self.qmaxi, self.B)
        self.data_dict[self.DPQ].q = self.invariant.LowQq
        self.data_dict[self.DPQ].i = self.invariant.LowQi
        self.data_dict[self.DGQ].q = self.invariant.HighQq
        self.data_dict[self.DGQ].i = self.invariant.HighQi
        self.parent.redrawTheList()
        self.parent.Replot()
        self.UpdateResults()

    def onTextEdited(self):
        if isNumeric.isNumeric(self.ui.edtQmin.text()):
            self.qmini = float(self.ui.edtQmin.text())
        else:
            return
        if isNumeric.isNumeric(self.ui.edtQmax.text()):
            self.qmaxi = float(self.ui.edtQmax.text())
        else:
            return
        if isNumeric.isNumeric(self.ui.edtB.text()):
            self.B = float(self.ui.edtB.text())
        else:
            return
        if isNumeric.isNumeric(self.ui.edtRadius.text()):
            self.radius = float(self.ui.edtRadius.text())
        else:
            return
        self.calculateAll()

    def accepted(self):
        """
        user click on an accepted button (ok, open,...)
        do nothing
        """
        pass

    def click(self, obj=None):
        name = obj.text()
        if name == 'OK':
            self.close()
        elif name == 'Close':
            self.close()
        elif name == 'Apply':
            self.onTextEdited()

    def printTXT(self, txt='', par=''):
        """
        for printing messages
        """
        if self.printout == None:
            print str(txt) + str(par)
        else:
            self.printout(txt, par)
        return