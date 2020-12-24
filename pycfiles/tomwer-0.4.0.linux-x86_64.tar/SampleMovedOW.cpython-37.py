# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/visualization/SampleMovedOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3888 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '19/03/2018'
from silx.gui import qt
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from tomwer.web.client import OWClient
from tomwer.gui.samplemoved import SampleMovedWidget
from tomwer.core.scan.scanbase import TomoBase
import os, logging
logger = logging.getLogger(__name__)

class SampleMovedOW(widget.OWWidget, OWClient):
    __doc__ = '\n    Simple widget exposing two images side by side to see if a sample moved\n    during the acquisition.\n\n    :param parent: the parent widget\n    '
    name = 'sample moved'
    id = 'orange.widgets.tomwer.samplemoved'
    description = 'This widget is used to display two scan side by side to know if a sample moved during the acquisition by simple observation.'
    icon = 'icons/sampleMoved.svg'
    priority = 85
    category = 'esrfWidgets'
    keywords = ['tomography', 'sample', 'moved', 'visualization']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name='data', type=TomoBase)

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, logger)
        layout = gui.vBox(self.mainArea, self.name).layout()
        self._widgetScanPath = qt.QWidget(parent=self)
        self._widgetScanPath.setLayout(qt.QHBoxLayout())
        self._widgetScanPath.layout().addWidget(qt.QLabel('scan: ', parent=(self._widgetScanPath)))
        self._scanNameQLabel = qt.QLabel('', parent=(self._widgetScanPath))
        self._widgetScanPath.layout().addWidget(self._scanNameQLabel)
        spacer = qt.QWidget(parent=(self._widgetScanPath))
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._widgetScanPath.layout().addWidget(spacer)
        layout.addWidget(self._widgetScanPath)
        self._mainWidget = SampleMovedWidget(parent=self)
        layout.addWidget(self._mainWidget)

    def sizeHint(self):
        return qt.QSize(400, 200)

    @Inputs.data_in
    def updateScan(self, scan):
        if scan is None:
            return
        assert isinstance(scan, TomoBase)
        if os.path.isdir(scan.path):
            self._scanNameQLabel.setText(os.path.basename(scan.path))
            rawSlices = scan.getProjectionsUrl()
            self._mainWidget.clearOnLoadActions()
            self._mainWidget.setImages(rawSlices)
            self._mainWidget.setOnLoadAction(scan.flatFieldCorrection)