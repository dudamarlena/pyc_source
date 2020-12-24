# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/datawatcher/observations.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 7254 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '31/05/2018'
from silx.gui import qt
from collections import OrderedDict
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.edfscan import EDFTomoScan
import weakref, os

class _ScanObservation(qt.QWidget):
    __doc__ = 'Widget used for the scans observation'
    HEADER = ('acquisition', 'status', 'N projections', 'type')

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self._onGoingObservations = None
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(qt.QLabel(''))
        self.observationTable = qt.QTableView(parent=parent)
        self.observationTable.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.observationTable.setModel(_ObservedScanModel(parent=(self.observationTable), header=(self.HEADER)))
        self.observationTable.resizeColumnsToContents()
        self.observationTable.setSortingEnabled(True)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self.observationTable)
        header = self.observationTable.horizontalHeader()
        if qt.qVersion() < '5.0':
            setResizeMode = header.setResizeMode
        else:
            setResizeMode = header.setSectionResizeMode
        setResizeMode(0, qt.QHeaderView.Fixed)
        setResizeMode(1, qt.QHeaderView.Stretch)
        setResizeMode(2, qt.QHeaderView.Stretch)
        header.setSectionResizeMode(0, qt.QHeaderView.Interactive)
        header.setStretchLastSection(True)

    @property
    def onGoingObservations(self):
        if self._onGoingObservations:
            return self._onGoingObservations()
        return

    def setOnGoingObservations(self, onGoingObservations):
        """
        will update the table to display the observations contained in
        onGoingObservations

        :param onGoingObservations: the obsevations observed to display
        """
        if self.onGoingObservations:
            self.onGoingObservations.sigObsAdded.disconnect(self.addObservation)
            self.onGoingObservations.sigObsRemoved.disconnect(self.removeObservation)
            self.onGoingObservations.sigObsStatusReceived.disconnect(self.update)
        self._onGoingObservations = weakref.ref(onGoingObservations)
        self.onGoingObservations.sigObsAdded.connect(self.addObservation)
        self.onGoingObservations.sigObsRemoved.connect(self.removeObservation)
        self.onGoingObservations.sigObsStatusReceived.connect(self.update)

    def update(self, scan, status):
        """

        :param str scan: the updated scan
        :param str status: the status of the updated scan
        """
        self.observationTable.model().update(scan, status)

    def addObservation(self, scan):
        """

        :param scan: the scan observed
        """
        self.observationTable.model().add(scan, 'starting')

    def removeObservation(self, scan):
        """

        :param scan: the scan removed
        """
        self.observationTable.model().remove(scan)

    def clear(self):
        self.observationTable.model().clear()


class _ObservedScanModel(qt.QAbstractTableModel):

    def __init__(self, parent, header, *args):
        (qt.QAbstractTableModel.__init__)(self, parent, *args)
        self.header = header
        self.observations = OrderedDict()

    def add(self, scan, status):
        self.observations[scan] = status
        if qt.qVersion() > '4.6':
            self.endResetModel()

    def remove(self, scan):
        if scan in self.observations:
            del self.observations[scan]
        if qt.qVersion() > '4.6':
            self.endResetModel()

    def update(self, scan, status):
        self.observations[scan] = status
        if qt.qVersion() > '4.6':
            self.endResetModel()

    def clear(self):
        self.observations = OrderedDict()
        if qt.qVersion() > '4.6':
            self.endResetModel()

    def rowCount(self, parent):
        return len(self.observations)

    def columnCount(self, parent):
        return len(self.header)

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        if self.observations is None:
            return
        ordering = sorted(list(self.observations.keys()))
        if order == qt.Qt.DescendingOrder:
            ordering = reversed(ordering)
        _observations = OrderedDict()
        for key in ordering:
            _observations[key] = self.observations[key]

        self.observations = _observations
        self.layoutChanged.emit()

    def data(self, index, role):
        if index.isValid() is False:
            return
            if role not in (qt.Qt.DisplayRole, qt.Qt.ToolTipRole):
                return
            obs = list(self.observations.keys())[index.row()]
            if index.column() is 0:
                if role == qt.Qt.ToolTipRole:
                    return obs
                    return os.path.basename(obs)
                else:
                    pass
            if index.column() is 1:
                return self.observations[obs]
        elif index.column() is 2:
            if HDF5TomoScan.directory_contains_scan(directory=obs):
                scan = HDF5TomoScan(scan=obs)
                return str(len(scan.projections))
            if os.path.exists(obs):
                if os.path.isdir(obs):
                    return str(len(os.listdir(obs)))
            return
        else:
            if index.column() is 3:
                if HDF5TomoScan.directory_contains_scan(directory=obs):
                    return 'hdf5'
                return 'edf'
            else:
                return

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal:
            if role == qt.Qt.DisplayRole:
                return self.header[col]