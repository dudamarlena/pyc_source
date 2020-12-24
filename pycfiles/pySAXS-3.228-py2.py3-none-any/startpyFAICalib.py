# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\winpython\python-2.7.10.amd64\lib\site-packages\pySAXS\guisaxs\qt\startpyFAICalib.py
# Compiled at: 2017-05-19 07:59:53
from fileinput import filename
import os, os, sys
from PyQt4 import QtGui, QtCore, uic
import fabio, pyFAI, pyFAI.calibrant, pyFAI.detectors
from pyFAI.calibration import calib
import pySAXS
from pySAXS.tools import filetools

class CalibStart(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'startpyFAICalib.ui', self)
        if parent is not None:
            self.setWindowIcon(parent.windowIcon())
        QtCore.QObject.connect(self.ui.STARTButton, QtCore.SIGNAL('clicked()'), self.OnClickStartButton)
        QtCore.QObject.connect(self.ui.fileButton, QtCore.SIGNAL('clicked()'), self.OnClickFileButton)
        QtCore.QObject.connect(self.ui.cleanButton, QtCore.SIGNAL('clicked()'), self.OnClickCleanButton)
        self.calibrants = pyFAI.calibrant.ALL_CALIBRANTS.keys()
        self.list_Calibrants = list(self.calibrants)
        self.list_Calibrants.sort()
        self.detectors = pyFAI.detectors.ALL_DETECTORS.keys()
        self.list_Detectors = list(self.detectors)
        self.list_Detectors.sort()
        self.ui.comboBoxCalibrants.addItems(self.list_Calibrants)
        self.ui.comboBoxDetectors.addItems(self.list_Detectors)
        self.ui.cleanButton.setDisabled(True)
        self.ui.show()
        return

    def OnClickFileButton(self):
        """
        Allow to select a file
        """
        fd = QtGui.QFileDialog(self)
        filename = fd.getOpenFileName()
        self.workingdirectory = filename
        self.ui.fileLineEdit.setText(filename)
        self.fname = filename
        self.ui.cleanButton.setEnabled(True)

    def OnClickStartButton(self):
        self.wavelength = float(self.ui.wavelengthLineEdit.text())
        self.polarization = str(self.ui.PolarizationLineEdit.text())
        self.distance = str(self.ui.DistanceLineEdit.text())
        self.detector = self.ui.comboBoxDetectors.currentIndex()
        self.calibrant = self.ui.comboBoxCalibrants.currentIndex()
        self.execute()

    def OnClickCleanButton(self):
        print 'Clean Button'
        name = filetools.getFilenameOnly(self.fname)
        print name
        ret = QtGui.QMessageBox.question(self, 'Clean', 'Are you sure you want to delete these items?', buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if ret != QtGui.QMessageBox.Yes:
            return
        removePoni = str(name + '.poni')
        removeNpt = str(name + '.npt')
        try:
            os.remove(removePoni)
            print name + '.poni has been removed'
        except:
            print "Poni file doesn't exist"

        try:
            os.remove(removeNpt)
            print name + '.npt has been removed'
        except:
            print "Npt file doesn't exist"

    def execute(self):
        cmd = 'pyFAI-calib.py '
        cmd += '-w ' + str(self.wavelength)
        cmd += ' -D ' + self.list_Detectors[self.detector]
        cmd += ' -c ' + self.list_Calibrants[self.calibrant]
        if self.ui.notiltCheckBox.isChecked():
            cmd += ' --no-tilt'
        if self.ui.PolarizationLineEdit.text() != '':
            cmd += ' -P ' + self.polarization
        if self.ui.DistanceLineEdit.text() != '':
            cmd += ' -l ' + self.distance
        if self.ui.fixDistanceCheckBox.isChecked():
            cmd += ' --fix-dist'
        cmd += ' "' + self.fname + '"'
        print cmd
        cmd = str(cmd)
        cd = os.path.dirname(str(self.fname))
        os.system('cd ' + cd)
        os.system(cmd)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = CalibStart()
    myapp.show()
    sys.exit(app.exec_())