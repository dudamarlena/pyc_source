# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/MyStatusBar.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1026 bytes
from dicom_tools.pyqtgraph.Qt import QtCore, QtGui

class MyStatusBar(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QHBoxLayout(self)
        self.lights = []

    def setSize(self, size):
        for i in xrange(0, size):
            thisLight = QtGui.QPushButton()
            thisLight.setStyleSheet('background-color: red')
            thisLight.setFixedSize(3, 3)
            self.lights.append(thisLight)
            self.layout.addWidget(thisLight)

    def setOn(self, i):
        self.lights[i].setOn()

    def setOff(self, i):
        self.lights[i].setOff()