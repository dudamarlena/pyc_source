# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/datawatcher/history.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 4731 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '18/02/2018'
from silx.gui import qt
from operator import itemgetter
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.edfscan import EDFTomoScan

class _ScanHistory(qt.QWidget):
    __doc__ = 'Widget used to display the lastest discovered scans'

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(qt.QLabel(''))
        self.scanHistory = qt.QTableView(parent=parent)
        self.scanHistory.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.scanHistory.setModel(_FoundScanModel(parent=(self.scanHistory), header=('time',
                                                                                     'type',
                                                                                     'scan ID'),
          mlist=[]))
        self.scanHistory.resizeColumnsToContents()
        self.scanHistory.setSortingEnabled(True)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self.scanHistory)
        self.scanHistory = self.scanHistory
        header = self.scanHistory.horizontalHeader()
        if qt.qVersion() < '5.0':
            setResizeMode = header.setResizeMode
        else:
            setResizeMode = header.setSectionResizeMode
        setResizeMode(0, qt.QHeaderView.Fixed)
        setResizeMode(1, qt.QHeaderView.Fixed)
        setResizeMode(2, qt.QHeaderView.Stretch)
        header.setStretchLastSection(True)

    def update(self, scans):
        self.scanHistory.setModel(_FoundScanModel(parent=self, header=('time', 'type',
                                                                       'scan ID'),
          mlist=scans))
        self.scanHistory.resizeColumnsToContents()


class _FoundScanModel(qt.QAbstractTableModel):
    __doc__ = '\n    Model for :class:_ScanHistory\n    '

    def __init__(self, parent, header, mlist, *args):
        (qt.QAbstractTableModel.__init__)(self, parent, *args)
        self.header = header
        self.myList = list(mlist.items()) if mlist else []

    def rowCount(self, parent):
        if self.myList is None:
            return 0
        return len(self.myList)

    def columnCount(self, parent):
        return 3

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        if self.myList is None:
            return
        self.myList = sorted((list(self.myList)), key=(itemgetter(col)))
        if order == qt.Qt.DescendingOrder:
            self.myList = list(reversed(sorted((list(self.myList)), key=(itemgetter(col)))))
        self.layoutChanged.emit()

    def data(self, index, role):
        if not index.isValid():
            return
            if role != qt.Qt.DisplayRole:
                return
            if index.column() == 0:
                return self.myList[index.row()][1].strftime('%a %m - %d - %Y   - %H:%M:%S')
            if index.column() == 1:
                path = self.myList[index.row()][0]
                if HDF5TomoScan.directory_contains_scan(path):
                    return 'hdf5'
                return 'edf'
        elif index.column() == 2:
            return self.myList[index.row()][0]

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal:
            if role == qt.Qt.DisplayRole:
                return self.header[col]