# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/CheckTable.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3361 bytes
from ..Qt import QtGui, QtCore
from . import VerticalLabel
__all__ = [
 'CheckTable']

class CheckTable(QtGui.QWidget):
    sigStateChanged = QtCore.Signal(object, object, object)

    def __init__(self, columns):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.headers = []
        self.columns = columns
        col = 1
        for c in columns:
            label = VerticalLabel.VerticalLabel(c, orientation='vertical')
            self.headers.append(label)
            self.layout.addWidget(label, 0, col)
            col += 1

        self.rowNames = []
        self.rowWidgets = []
        self.oldRows = {}

    def updateRows(self, rows):
        for r in self.rowNames[:]:
            if r not in rows:
                self.removeRow(r)

        for r in rows:
            if r not in self.rowNames:
                self.addRow(r)

    def addRow(self, name):
        label = QtGui.QLabel(name)
        row = len(self.rowNames) + 1
        self.layout.addWidget(label, row, 0)
        checks = []
        col = 1
        for c in self.columns:
            check = QtGui.QCheckBox('')
            check.col = c
            check.row = name
            self.layout.addWidget(check, row, col)
            checks.append(check)
            if name in self.oldRows:
                check.setChecked(self.oldRows[name][col])
            col += 1
            check.stateChanged.connect(self.checkChanged)

        self.rowNames.append(name)
        self.rowWidgets.append([label] + checks)

    def removeRow(self, name):
        row = self.rowNames.index(name)
        self.oldRows[name] = self.saveState()['rows'][row]
        self.rowNames.pop(row)
        for w in self.rowWidgets[row]:
            w.setParent(None)
            if isinstance(w, QtGui.QCheckBox):
                w.stateChanged.disconnect(self.checkChanged)

        self.rowWidgets.pop(row)
        for i in range(row, len(self.rowNames)):
            widgets = self.rowWidgets[i]
            for j in range(len(widgets)):
                widgets[j].setParent(None)
                self.layout.addWidget(widgets[j], i + 1, j)

    def checkChanged(self, state):
        check = QtCore.QObject.sender(self)
        self.sigStateChanged.emit(check.row, check.col, state)

    def saveState(self):
        rows = []
        for i in range(len(self.rowNames)):
            row = [self.rowNames[i]] + [c.isChecked() for c in self.rowWidgets[i][1:]]
            rows.append(row)

        return {'cols':self.columns,  'rows':rows}

    def restoreState(self, state):
        rows = [r[0] for r in state['rows']]
        self.updateRows(rows)
        for r in state['rows']:
            rowNum = self.rowNames.index(r[0])
            for i in range(1, len(r)):
                self.rowWidgets[rowNum][i].setChecked(r[i])