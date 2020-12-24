# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/gui/metadataWidget.py
# Compiled at: 2019-11-28 10:44:40
# Size of source mod 2**32: 4338 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '14/10/2019'
import numpy
from silx.gui import qt
from darfix.core.dataset import _METADATA_TYPES

class MetadataWidget(qt.QMainWindow):

    def __init__(self, parent=None):
        """
        Widget used to show the metadata in a table.
        """
        super(MetadataWidget, self).__init__(parent)
        self.setWindowTitle('Metadata')
        metadataTypeLabel = qt.QLabel('metadata type: ')
        self._metadataTypeCB = qt.QComboBox()
        for metaType in _METADATA_TYPES:
            self._metadataTypeCB.addItem(metaType)

        metadataTypeWidget = qt.QWidget(self)
        metadataTypeWidget.setLayout(qt.QHBoxLayout())
        metadataTypeWidget.layout().addWidget(metadataTypeLabel)
        metadataTypeWidget.layout().addWidget(self._metadataTypeCB)
        self._table = qt.QTableWidget()
        mainWidget = qt.QWidget(self)
        mainWidget.setLayout(qt.QVBoxLayout())
        mainWidget.layout().addWidget(metadataTypeWidget)
        mainWidget.layout().addWidget(self._table)
        self.mainWidget = mainWidget
        self.setCentralWidget(mainWidget)
        self._metadataTypeCB.currentTextChanged.connect(self._updateView)

    def setDataset(self, dataset):
        self._dataset = dataset
        self._updateView()

    def clearTable(self):
        self._table.clear()

    def _updateView(self, metadata_type=None):
        """
        Updates the view to show the correponding metadata.

        :param Union[None, int] metadata_type: Kind of metadata.
        """
        if metadata_type is None:
            metadata_type = self._metadataTypeCB.currentText()
        metadata_type = _METADATA_TYPES[metadata_type]
        self._table.clear()
        metadata = self._dataset.metadata
        self._table.setRowCount(len(metadata))
        columnCount = None
        for row, metadata_frame in enumerate(self._dataset.metadata):
            keys = metadata_frame.get_keys(kind=metadata_type)
            if not row:
                if columnCount is None:
                    self._table.setColumnCount(len(keys))
                    self._table.setHorizontalHeaderLabels(keys)
                else:
                    if columnCount != len(metadata_frame):
                        raise ValueError('Metadata keys are incoherent')
            for column, key in enumerate(keys):
                _item = qt.QTableWidgetItem()
                txt = metadata_frame.get_value(kind=metadata_type, name=key)
                if type(txt) is numpy.ndarray:
                    if txt.size == 1:
                        txt = txt[0]
                elif hasattr(txt, 'decode'):
                    txt = txt.decode('utf-8')
                else:
                    txt = str(txt)
                _item.setText(txt)
                _item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                self._table.setItem(row, column, _item)