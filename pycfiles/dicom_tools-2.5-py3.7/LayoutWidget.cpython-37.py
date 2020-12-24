# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/LayoutWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3425 bytes
from ..Qt import QtGui, QtCore
__all__ = ['LayoutWidget']

class LayoutWidget(QtGui.QWidget):
    __doc__ = "\n    Convenience class used for laying out QWidgets in a grid.\n    (It's just a little less effort to use than QGridLayout)\n    "

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.items = {}
        self.rows = {}
        self.currentRow = 0
        self.currentCol = 0

    def nextRow(self):
        """Advance to next row for automatic widget placement"""
        self.currentRow += 1
        self.currentCol = 0

    def nextColumn(self, colspan=1):
        """Advance to next column, while returning the current column number 
        (generally only for internal use--called by addWidget)"""
        self.currentCol += colspan
        return self.currentCol - colspan

    def nextCol(self, *args, **kargs):
        """Alias of nextColumn"""
        return (self.nextColumn)(*args, **kargs)

    def addLabel(self, text=' ', row=None, col=None, rowspan=1, colspan=1, **kargs):
        """
        Create a QLabel with *text* and place it in the next available cell (or in the cell specified)
        All extra keyword arguments are passed to QLabel().
        Returns the created widget.
        """
        text = (QtGui.QLabel)(text, **kargs)
        self.addItem(text, row, col, rowspan, colspan)
        return text

    def addLayout(self, row=None, col=None, rowspan=1, colspan=1, **kargs):
        """
        Create an empty LayoutWidget and place it in the next available cell (or in the cell specified)
        All extra keyword arguments are passed to :func:`LayoutWidget.__init__ <pyqtgraph.LayoutWidget.__init__>`
        Returns the created widget.
        """
        layout = LayoutWidget(**kargs)
        self.addItem(layout, row, col, rowspan, colspan)
        return layout

    def addWidget(self, item, row=None, col=None, rowspan=1, colspan=1):
        """
        Add a widget to the layout and place it in the next available cell (or in the cell specified).
        """
        if row == 'next':
            self.nextRow()
            row = self.currentRow
        else:
            if row is None:
                row = self.currentRow
        if col is None:
            col = self.nextCol(colspan)
        if row not in self.rows:
            self.rows[row] = {}
        self.rows[row][col] = item
        self.items[item] = (row, col)
        self.layout.addWidget(item, row, col, rowspan, colspan)

    def getWidget(self, row, col):
        """Return the widget in (*row*, *col*)"""
        return self.row[row][col]