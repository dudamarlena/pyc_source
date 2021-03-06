# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/reconstruction/DarkRefAndCopyOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 5238 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
import logging
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Input, Output
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs, logger as DRLogger
from tomwer.core.scan.scanbase import TomoBase
from tomwer.gui.reconstruction.darkref.darkrefcopywidget import DarkRefAndCopyWidget
from tomwer.synctools.ftseries import QReconsParams
from tomwer.web.client import OWClient
logger = logging.getLogger(__name__)

class DarkRefAndCopyOW(widget.OWWidget, OWClient):
    __doc__ = '\n        A simple widget managing the copy of an incoming folder to an other one\n\n        :param parent: the parent widget\n        '
    name = 'dark and flat field construction'
    id = 'orange.widgets.tomwer.darkrefs'
    description = 'This widget will generate dark refs for a received scan '
    icon = 'icons/darkref.svg'
    priority = 25
    category = 'esrfWidgets'
    keywords = ['tomography', 'dark', 'darks', 'ref', 'refs']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    settingsHandler = CallbackSettingsHandler()
    _rpSetting = Setting(dict())
    assert len(DarkRefs.inputs) == 1

    class Inputs:
        data_in = Input(name=(DarkRefs.inputs[0].name), type=(DarkRefs.inputs[0].type),
          doc=(DarkRefs.inputs[0].doc))

    assert len(DarkRefs.outputs) == 1

    class Outputs:
        data_out = Output(name=(DarkRefs.outputs[0].name), type=(DarkRefs.outputs[0].type),
          doc=(DarkRefs.outputs[0].doc))

    def __init__(self, parent=None, _connect_handler=True, reconsparams=None):
        """

        :param bool _connect_handler: True if we want to store the modifications
                                      on the setting. Need for unit test since
                                      keep alive qt widgets.
        :param QReconsParams reconsparams: reconstruction parameters
        """
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, (logger, DRLogger))
        reconsparams = reconsparams or QReconsParams()
        if self._rpSetting != dict():
            try:
                reconsparams.dkrf.load_from_dict(self._rpSetting)
            except:
                logger.warning('fail to load reconstruction settings')

        self.widget = DarkRefAndCopyWidget(parent=self, reconsparams=reconsparams)
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.addWidget(self.widget)
        self.setForceSync = self.widget.setForceSync
        self.hasRefStored = self.widget.hasRefStored
        self.setModeAuto = self.widget.setModeAuto
        self.setRefsFromScan = self.widget.setRefsFromScan
        self.widget.sigScanReady.connect(self.signalReady)
        if _connect_handler:
            self.settingsHandler.addCallback(self._updateSettingsVals)

    @Inputs.data_in
    def process(self, scanID):
        assert isinstance(scanID, TomoBase)
        return self.widget.process(scanID)

    def signalReady(self, scanID):
        assert isinstance(scanID, TomoBase)
        self.Outputs.data_out.send(scanID)

    def _updateSettingsVals(self):
        self._rpSetting = self.widget.recons_params.to_dict()

    @property
    def recons_params(self):
        return self.widget.recons_params

    def close(self):
        logger.info('close Dark refs')
        self.widget.close()
        super(DarkRefAndCopyOW, self).close()