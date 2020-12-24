# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/DataTransfertOW.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 5147 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '07/12/2016'
import logging
from Orange.widgets import widget, gui
from Orange.widgets import settings
from Orange.widgets.widget import Output, Input
from silx.gui import qt
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from tomwer.core.process.datatransfert import FolderTransfert, logger as FTLogger
from tomwer.web.client import OWClient
from tomwer.gui.datatransfert import DataTransfertSelector
from tomwer.core.scan.scanfactory import ScanFactory
logger = logging.getLogger(__name__)

class DataTransfertOW(widget.OWWidget, FolderTransfert, OWClient):
    __doc__ = '\n    A simple widget managing the copy of an incoming folder to an other one\n\n    :param parent: the parent widget\n    '
    name = 'data transfert'
    id = 'orange.widgets.tomwer.foldertransfert'
    description = 'This widget insure data transfert of the received data '
    description += 'to the given directory'
    icon = 'icons/folder-transfert.svg'
    priority = 30
    category = 'esrfWidgets'
    keywords = ['tomography', 'transfert', 'cp', 'copy', 'move', 'file',
     'tomwer', 'folder']
    settingsHandler = CallbackSettingsHandler()
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    dest_dir = settings.Setting(str())
    scanready = qt.Signal(str)
    assert len(FolderTransfert.inputs) == 1

    class Inputs:
        data_in = Input(name=(FolderTransfert.inputs[0].name), type=(FolderTransfert.inputs[0].type),
          doc=(FolderTransfert.inputs[0].doc))

    assert len(FolderTransfert.outputs) == 1

    class Outputs:
        data_out = Output(name=(FolderTransfert.outputs[0].name), type=(FolderTransfert.outputs[0].type),
          doc=(FolderTransfert.outputs[0].doc))

    def __init__(self, parent=None):
        FolderTransfert.__init__(self)
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (logger, FTLogger))
        self._widget = DataTransfertSelector(parent=self, rnice_option=True,
          default_root_folder=(self._getDefaultOutputDir()))
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self._widget)
        self._widget.sigSelectionChanged.connect(self.setDestDir)
        self.settingsHandler.addCallback(self._updateSettingsVals)
        if self.dest_dir != '':
            self._widget.setFolder(self.dest_dir)

    def _requestFolder(self):
        """Launch a QFileDialog to ask the user the output directory"""
        dialog = qt.QFileDialog(self)
        dialog.setWindowTitle('Destination folder')
        dialog.setModal(1)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)
        if not dialog.exec_():
            dialog.close()
            return
        return dialog.selectedFiles()[0]

    def signalTransfertOk(self, scanID):
        if scanID is None:
            return
        assert isinstance(scanID, str)
        scan = ScanFactory.create_scan_object(scan_path=scanID)
        self.Outputs.data_out.send(scan)
        self.scanready.emit(scan.path)

    def _updateSettingsVals(self):
        """function used to update the settings values"""
        self.dest_dir = self._destDir

    @Inputs.data_in
    def process(self, scan, move=False, force=True, noRsync=False):
        FolderTransfert.process(self, scan=scan, move=move, force=force, noRsync=noRsync)