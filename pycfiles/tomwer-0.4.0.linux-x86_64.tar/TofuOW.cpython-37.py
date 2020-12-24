# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/reconstruction/TofuOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 7454 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
import functools, logging, os
from silx.gui import qt
from Orange.widgets import settings
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input, Output
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from tomwer.core.process.reconstruction.lamino import LaminoReconstruction
from tomwer.gui.reconstruction.lamino.tofu import TofuWindow
from tomwer.synctools.stacks.reconstruction.lamino import LaminoReconstructionStack
from tomwer.web.client import OWClient
from tomwer.core.scan.scanbase import TomoBase
_logger = logging.getLogger(__name__)

class TofuOW(widget.OWWidget, OWClient):
    __doc__ = '\n        A simple widget managing the copy of an incoming folder to an other one\n\n        :param parent: the parent widget\n        '
    name = 'tofu reconstruction'
    id = 'orange.widgets.tomwer.reconstruction.TofuOW.TofuOW'
    description = 'This widget will call tofu for running a reconstruction '
    icon = 'icons/XY_lamino.svg'
    priority = 25
    category = 'esrfWidgets'
    keywords = ['tomography', 'tofu', 'reconstruction', 'lamino', 'laminography']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    settingsHandler = CallbackSettingsHandler()
    _reconsParams = settings.Setting(dict())
    _additionalOpts = settings.Setting(dict())
    _delete_existing = settings.Setting(bool())
    assert len(LaminoReconstruction.inputs) == 1

    class Inputs:
        data_in = Input(name=(LaminoReconstruction.inputs[0].name), type=(LaminoReconstruction.inputs[0].type),
          doc=(LaminoReconstruction.inputs[0].doc))

    assert len(LaminoReconstruction.outputs) == 1

    class Outputs:
        data_out = Output(name=(LaminoReconstruction.outputs[0].name), type=(LaminoReconstruction.outputs[0].type),
          doc=(LaminoReconstruction.outputs[0].doc))

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (_logger,))
        widget.OWWidget.__init__(self, parent)
        self._lastScan = None
        self._box = gui.vBox(self.mainArea, self.name)
        self._mainWidget = TofuWindow(parent=self)
        self._box.layout().addWidget(self._mainWidget)
        self._widgetControl = qt.QWidget(self)
        self._widgetControl.setLayout(qt.QHBoxLayout())
        self._executeButton = qt.QPushButton('reprocess', self._widgetControl)
        self._executeButton.clicked.connect(self._reprocess)
        self._executeButton.setEnabled(False)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._widgetControl.layout().addWidget(spacer)
        self._widgetControl.layout().addWidget(self._executeButton)
        self._box.layout().addWidget(self._mainWidget)
        self._box.layout().addWidget(self._widgetControl)
        self._mainWidget.setParameters(self._reconsParams)
        if len(self._additionalOpts) > 0:
            self._mainWidget.setAdditionalRecoOptions(self._additionalOpts)
        self._mainWidget.setRemoveOutputDir(self._delete_existing)
        self.settingsHandler.addCallback(self._updateSettingsVals)
        self._reconsStack = LaminoReconstructionStack()
        self._reconsStack.sigReconsStarted.connect(self._TofuOW__processing_start)
        self._reconsStack.sigReconsFinished.connect(self._TofuOW__processing_end)
        self._reconsStack.sigReconsFailed.connect(self._TofuOW__processing_end)
        self._reconsStack.sigReconsMissParams.connect(self._TofuOW__processing_end)

    @Inputs.data_in
    def process(self, scan):
        if scan is not None:
            self._executeButton.setEnabled(True)
            self._lastScan = scan
            self._mainWidget.loadFromScan(scan.path)
            recons_param = self._mainWidget.getParameters()
            add_options = self._mainWidget.getAdditionalRecoOptions()
            remove_existing = self._mainWidget.removeOutputDir()
            assert isinstance(scan, TomoBase)
            callback = functools.partial(self.Outputs.data_out.send, scan)
            self._reconsStack.add(recons_obj=(LaminoReconstruction()), scan_id=scan,
              recons_params=recons_param,
              additional_opts=add_options,
              remove_existing=remove_existing,
              callback=callback)

    def _reprocess(self):
        if self._lastScan is None:
            _logger.warning('No scan has been process yet')
        else:
            if os.path.isdir(self._lastScan) is False:
                _logger.warning('Last scan %s, does not exist anymore' % self._lastScan)
                self._executeButton.setEnabled(False)
            else:
                self.process(self._lastScan)

    def _updateSettingsVals(self):
        """function used to update the settings values"""
        self._reconsParams = self._mainWidget.getParameters()
        self._additionalOpts = self._mainWidget.getAdditionalRecoOptions()
        self._delete_existing = self._mainWidget.removeOutputDir()

    def __processing_start(self, scan):
        self.processing_state(scan=scan, working=True)

    def __processing_end(self, scan):
        self.processing_state(scan=scan, working=False)

    def processing_state(self, scan, working: bool) -> None:
        try:
            if working:
                self.processing_info('processing %s' % scan.path)
            else:
                self.Processing.clear()
        except Exception:
            pass