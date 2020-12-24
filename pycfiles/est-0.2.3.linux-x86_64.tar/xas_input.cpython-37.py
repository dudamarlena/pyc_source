# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/utils/xas_input.py
# Compiled at: 2020-03-12 11:12:33
# Size of source mod 2**32: 5635 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import logging, os
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Output
from silx.gui import qt
from silx.io.url import DataUrl
import est.core.io
from est.core.types import XASObject
from est.gui.xas_object_definition import XASObjectDialog
_logger = logging.getLogger(__file__)
_DEBUG = False

class XASInputOW(OWWidget):
    __doc__ = '\n    Widget used for signal extraction\n    '
    name = 'xas input'
    id = 'orange.widgets.xas.utils.xas_input'
    description = 'Read .dat file and convert it to spectra'
    icon = 'icons/input.png'
    priority = 0
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'signal', 'input', 'file']
    want_main_area = True
    resizing_enabled = True
    _input_file_setting = Setting(str())
    _spectra_url_setting = Setting(str())
    _energy_url_setting = Setting(str())
    _configuration_url_setting = Setting(str())
    process_function = est.core.io.read_frm_file

    class Outputs:
        res_xas_obj = Output('xas_obj', XASObject)

    def __init__(self):
        super().__init__()
        self._inputWindow = qt.QWidget(parent=self)
        self._inputWindow.setLayout(qt.QGridLayout())
        self._inputDialog = XASObjectDialog(parent=self)
        self._inputWindow.layout().addWidget(self._inputDialog, 0, 0, 1, 2)
        self._startPB = qt.QPushButton('restart', parent=self)
        self._inputWindow.layout().addWidget(self._startPB, 1, 1, 1, 1)
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._inputWindow.layout().addWidget(spacer, 2, 0)
        layout = gui.vBox(self.mainArea, 'input').layout()
        layout.addWidget(self._inputWindow)
        self._manageSettings()
        self.restart = self._emitNewFile
        self._startPB.pressed.connect(self._emitNewFile)
        self._inputDialog.editingFinished.connect(self._storeSettings)
        self.setFileSelected = self._inputDialog.setDatFile

    def _emitNewFile(self, *args, **kwargs):
        try:
            xas_obj = self._inputDialog.buildXASObject()
        except ValueError as e:
            try:
                qt.QMessageBox.warning(self, '', str(e))
            finally:
                e = None
                del e

        else:
            if _DEBUG is True:
                if xas_obj.n_spectrum > 100:
                    from est.core.process.roi import ROIProcess, _ROI
                    roiProcess = ROIProcess()
                    roiProcess.setRoi(origin=(0, 0), size=(10, 10))
                    xas_obj = roiProcess.process(xas_obj)
            self.Outputs.res_xas_obj.send(xas_obj)

    def _manageSettings(self):
        input_type = est.io.InputType.hdf5_spectra
        if os.path.isfile(self._input_file_setting):
            self._inputDialog.setDatFile(self._input_file_setting)
            if self._input_file_setting.endswith('.xmu'):
                input_type = est.io.InputType.xmu_spectrum
            else:
                input_type = est.io.InputType.dat_spectrum

        def load_url(url_path, setter):
            if url_path != '':
                try:
                    url = DataUrl(url_path)
                    if url:
                        if url.is_valid():
                            setter(url.path())
                except ... as e:
                    try:
                        logging.info('fail to load ', url_path)
                    finally:
                        e = None
                        del e

        load_url(self._spectra_url_setting, self._inputDialog.setSpectraUrl)
        load_url(self._energy_url_setting, self._inputDialog.setEnergyUrl)
        load_url(self._configuration_url_setting, self._inputDialog.setConfigurationUrl)
        self._inputDialog.setCurrentType(input_type)

    def _storeSettings(self):
        self._input_file_setting = self._inputDialog.getDatFile()
        self._spectra_url_setting = self._inputDialog.getSpectraUrl()
        self._energy_url_setting = self._inputDialog.getEnergyUrl()
        self._configuration_url_setting = self._inputDialog.getConfigurationUrl()

    def sizeHint(self):
        return qt.QSize(400, 200)