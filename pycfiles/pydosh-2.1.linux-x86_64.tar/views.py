# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/views.py
# Compiled at: 2013-12-19 02:01:18
from PySide import QtCore, QtGui

class TagTableView(QtGui.QTableView):

    def __init__(self, parent=None):
        super(TagTableView, self).__init__(parent=parent)

    def sizeHint(self):
        width = 0
        for column in xrange(self.model().columnCount()):
            width += self.columnWidth(column)

        width += self.verticalHeader().width() + self.autoScrollMargin() * 1.5 + 2
        height = 0
        for row in xrange(self.model().rowCount()):
            height += self.rowHeight(row)

        height += self.horizontalHeader().height() + self.autoScrollMargin() * 1.5 + 2
        return QtCore.QSize(width, height)