# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/scanselectorwidget.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 5145 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '25/05/2018'
from silx.gui import qt
from tomwer.gui.qfolderdialog import QScanDialog
from tomwer.core.scan.scanbase import TomoBase
from tomwer.gui.datalist import DataList
from collections import OrderedDict
import os
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class ScanSelectorWidget(qt.QWidget):
    __doc__ = 'Widget used to select a scan on a list'
    sigSelectionChanged = qt.Signal(list)

    def __init__(self, parent=None):

        def getAddAndRmButtons():
            lLayout = qt.QHBoxLayout()
            w = qt.QWidget(self)
            w.setLayout(lLayout)
            self._addButton = qt.QPushButton('Add')
            self._addButton.clicked.connect(self._callbackAddFolder)
            self._rmButton = qt.QPushButton('Remove')
            self._rmButton.clicked.connect(self._callbackRemoveFolder)
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
            lLayout.addWidget(spacer)
            lLayout.addWidget(self._addButton)
            lLayout.addWidget(self._rmButton)
            return w

        def getSendButton():
            lLayout = qt.QHBoxLayout()
            widget = qt.QWidget(self)
            widget.setLayout(lLayout)
            self._sendButton = qt.QPushButton('Select')
            self._sendButton.clicked.connect(self._selectActiveScan)
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
            lLayout.addWidget(spacer)
            lLayout.addWidget(self._sendButton)
            return widget

        qt.QWidget.__init__(self, parent)
        self.items = OrderedDict()
        self.setLayout(qt.QVBoxLayout())
        self.dataList = DataList(parent=self)
        self.dataList.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.layout().addWidget(self.dataList)
        self.layout().addWidget(getAddAndRmButtons())
        self.layout().addWidget(getSendButton())
        self.setAcceptDrops(True)
        self.add = self.dataList.add
        self.remove = self.dataList.remove

    def _callbackAddFolder(self):
        """"""
        dialog = QScanDialog(self, multiSelection=True)
        if not dialog.exec_():
            dialog.close()
            return
        for folder in dialog.filesSelected():
            assert os.path.isdir(folder)
            self.add(folder)

    def _selectActiveScan(self):
        sItem = self.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [_item.text() for _item in sItem]
            self.sigSelectionChanged.emit(list(selection))
        else:
            logger.warning('No active scan detected')

    def _callbackRemoveFolder(self):
        """"""
        selectedItems = self.dataList.selectedItems()
        if selectedItems is not None:
            for item in selectedItems:
                self.dataList.remove_item(item)

    def setActiveScan(self, scan):
        """
        set the given scan as the active one

        :param scan: the scan to set active
        :type scan: Union[str, TomoBase]
        """
        scanID = scan
        if isinstance(scan, TomoBase):
            scanID = scan.path
        self.dataList.setCurrentItem(self.dataList.items[scanID])


if __name__ == '__main__':
    qapp = qt.QApplication([])
    widget = ScanSelectorWidget()
    widget.show()
    widget.add('/nobackup')
    widget.add('/nobackup/linazimov/payno/datasets/id19')
    widget.add('/nobackup/linazimov/payno/datasets/id16b')
    widget.remove('/nobackup')
    qapp.exec_()