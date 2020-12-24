# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/table/qtable.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides base table widget"""
__all__ = [
 'QBaseTableWidget']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus.qt.qtgui.model import QBaseModelWidget

class QBaseTableWidget(QBaseModelWidget):

    def tableView(self):
        return self.viewWidget()

    def createViewWidget(self, klass=None):
        if klass is None:
            klass = Qt.QTableView
        table = klass()
        table.setSortingEnabled(True)
        table.sortByColumn(0, Qt.Qt.AscendingOrder)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
        table.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        return table