# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/console/CmdInput.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1988 bytes
from ..Qt import QtCore, QtGui
from ..python2_3 import asUnicode

class CmdInput(QtGui.QLineEdit):
    sigExecuteCmd = QtCore.Signal(object)

    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        self.history = ['']
        self.ptr = 0

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Up:
            if self.ptr < len(self.history) - 1:
                self.setHistory(self.ptr + 1)
                ev.accept()
                return
        if ev.key() == QtCore.Qt.Key_Down:
            if self.ptr > 0:
                self.setHistory(self.ptr - 1)
                ev.accept()
                return
        if ev.key() == QtCore.Qt.Key_Return:
            self.execCmd()
        else:
            QtGui.QLineEdit.keyPressEvent(self, ev)
            self.history[0] = asUnicode(self.text())

    def execCmd(self):
        cmd = asUnicode(self.text())
        if len(self.history) == 1 or cmd != self.history[1]:
            self.history.insert(1, cmd)
        self.history[0] = ''
        self.setHistory(0)
        self.sigExecuteCmd.emit(cmd)

    def setHistory(self, num):
        self.ptr = num
        self.setText(self.history[self.ptr])