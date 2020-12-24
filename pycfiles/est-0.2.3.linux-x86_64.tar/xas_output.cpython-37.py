# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/utils/xas_output.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 4858 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
from Orange.widgets import gui
from Orange.widgets.widget import OWWidget
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Input
from silx.gui import qt
from est.core.types import XASObject
import est.core.io, logging, h5py
_logger = logging.getLogger(__file__)

class XASOutputOW(OWWidget):
    __doc__ = '\n    Widget used for signal extraction\n    '
    name = 'xas output'
    id = 'orange.widgets.xas.utils.xas_output'
    description = 'Store process result (configuration)'
    icon = 'icons/output.png'
    priority = 5
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'signal', 'output', 'file']
    want_main_area = True
    resizing_enabled = True
    _output_file_setting = Setting(str())
    process_function = est.core.io.XASWriter

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)

    def __init__(self):
        super().__init__()
        self._outputWindow = qt.QWidget(parent=self)
        self._outputWindow.setLayout(qt.QGridLayout())
        self._outputWindow.layout().addWidget(qt.QLabel('file', parent=self))
        self._inputLe = qt.QLineEdit('', parent=self)
        self._outputWindow.layout().addWidget(self._inputLe, 0, 0)
        self._selectPB = qt.QPushButton('select', parent=self)
        self._outputWindow.layout().addWidget(self._selectPB, 0, 1)
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._outputWindow.layout().addWidget(spacer, 2, 0)
        layout = gui.vBox(self.mainArea, 'output').layout()
        layout.addWidget(self._outputWindow)
        self.setFileSelected(self._output_file_setting)
        self._selectPB.pressed.connect(self._selectFile)

    def _selectFile(self, *args, **kwargs):
        old = self.blockSignals(True)
        dialog = qt.QFileDialog(self)
        dialog.setAcceptMode(qt.QFileDialog.AcceptSave)
        dialog.setNameFilters(['hdf5 files (*.hdf5, *.hdf, *.h5)'])
        if not dialog.exec_():
            dialog.close()
            return False
        fileSelected = dialog.selectedFiles()
        if len(fileSelected) == 0:
            return False
        assert len(fileSelected) == 1
        file_ = fileSelected[0]
        if not h5py.is_hdf5(file_):
            file_ += '.h5'
        self.setFileSelected(file_)
        self.blockSignals(old)
        return True

    def setFileSelected(self, file_path):
        self._output_file_setting = file_path
        self._inputLe.setText(file_path)

    def _getFileSelected(self):
        return self._inputLe.text()

    @Inputs.xas_obj
    def process(self, xas_obj):
        if xas_obj is None:
            return
        else:
            if isinstance(xas_obj, dict):
                _xas_obj = XASObject.from_dict(xas_obj)
            else:
                _xas_obj = xas_obj
            has_file = self._getFileSelected() != ''
            if not has_file:
                mess = qt.QMessageBox(parent=self)
                mess.setIcon(qt.QMessageBox.Warning)
                mess.setText('No output file defined, please give a file path')
                mess.exec_()
                has_file = self._selectFile()
            if not has_file:
                _logger.error('no valid output file given, skip save')
            else:
                _xas_obj.dump(self._getFileSelected())