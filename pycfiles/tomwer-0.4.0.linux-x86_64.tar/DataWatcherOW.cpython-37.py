# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/DataWatcherOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 5601 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '25/10/2016'
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Output
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.process.datawatcher.datawatcher import _DataWatcher, logger as TDLogger
from tomwer.gui.datawatcher import DataWatcherWidget
from tomwer.web.client import OWClient
import functools, logging
logger = logging.getLogger(__name__)

class DataWatcherOW(widget.OWWidget, OWClient):
    __doc__ = '\n    This widget is used to observe a selected folder and his sub-folders to\n    detect if they are containing valid-finished acquisitions.\n    '
    name = 'data watcher'
    id = 'orangecontrib.widgets.tomwer.datawatcherwidget.DataWatcherOW'
    description = 'The widget will observe folder and sub folders of a given path and waiting for acquisition to be ended. The widget will infinitely wait until an acquisition is ended. If an acquisition is ended then a signal containing the folder path is emitted.'
    icon = 'icons/datawatcher.svg'
    priority = 12
    category = 'tomwer'
    keywords = ['tomography', 'file', 'tomwer', 'observer', 'datawatcher']
    allows_cycle = True
    compress_signal = False
    want_main_area = True
    resizing_enabled = True
    folderObserved = Setting(str())
    DEFAULT_DIRECTORY = '/lbsram/data/visitor'
    assert len(_DataWatcher.inputs) == 0
    assert len(_DataWatcher.outputs) == 1

    class Outputs:
        data_out = Output(name=(_DataWatcher.outputs[0].name), type=(_DataWatcher.outputs[0].type),
          doc=(_DataWatcher.outputs[0].doc))

    def __init__(self, parent=None, displayAdvancement=True):
        """Simple class which will check advancement state of the acquisition
        for a specific folder

        :param parent: the parent widget
        """
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (logger, TDLogger))
        self._widget = DataWatcherWidget(parent=self)
        self._widget.setFolderObserved(self.folderObserved)
        self._box = gui.vBox(self.mainArea, self.name)
        layout = self._box.layout()
        layout.addWidget(self._widget)
        self._widget.sigFolderObservedChanged.connect(self._updateSettings)
        self._widget.sigScanReady.connect(self._sendSignal)
        callback_start = functools.partial(self.processing_state, True)
        self._widget.sigObservationStart.connect(callback_start)
        callback_end = functools.partial(self.processing_state, False)
        self._widget.sigObservationEnd.connect(callback_end)

    def _updateSettings(self):
        self.folderObserved = self._widget.getFolderObserved()

    @property
    def currentStatus(self):
        return self._widget.currentStatus

    @property
    def sigTMStatusChanged(self):
        return self._widget.sigTMStatusChanged

    def resetStatus(self):
        self._widget.resetStatus()

    def _sendSignal(self, scan):
        assert isinstance(scan, TomoBase)
        self.Outputs.data_out.send(scan)

    def setFolderObserved(self, path):
        self._widget.setFolderObserved(path)

    def setObservation(self, b):
        self._widget.setObservation(b)

    def setTimeBreak(self, val):
        """
        Set the time break between two loop observation
        :param val: time (in sec)
        """
        self._widget.setWaitTimeBtwLoop(val)

    def startObservation(self):
        try:
            self.processing_info('processing')
        except Exception:
            pass

        self._widget.start()

    def stopObservation(self, succes=False):
        self._widget.stop(succes)
        try:
            self.Processing.clear()
        except Exception:
            pass

    def processing_state(self, working: bool) -> None:
        try:
            if working:
                self.processing_info('watching')
            else:
                self.Processing.clear()
        except Exception:
            pass