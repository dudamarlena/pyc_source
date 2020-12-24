# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/reconsparamseditor/pyhstwidget.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 8864 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.core.utils import pyhstutils
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructEditor
from tomwer.synctools.ftseries import QReconsParams, _QPyhstRP
from tomwer.gui.reconstruction.deviceselector import CudaPlatfornGroup
logger = TomwerLogger(__name__)

class PyHSTWidget(H5StructEditor, qt.QWidget):
    __doc__ = '\n    Definition of the PyHST tab to edit the PyHST parameters\n\n    :param reconsparams: reconstruction parameters edited by the widget\n    '

    def __init__(self, reconsparams, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='PYHSTEXE')
        self._recons_params = None
        self.setReconsParams(recons_params=reconsparams)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._PyHSTWidget__buildPYHSTVersion())
        self.layout().addWidget(self._PyHSTWidget__buildPYHSTOfficialVersion())
        self._qcbverbose = qt.QCheckBox('verbose', parent=self)
        self.layout().addWidget(self._qcbverbose)
        self.linkCheckboxWithH5Variable((self._qcbverbose), 'VERBOSE', invert=False)
        self.layout().addWidget(self._PyHSTWidget__buildVerboseFile())
        self.layout().addWidget(self._PyHSTWidget__buildMakeOAR())
        self.layout().addWidget(self._PyHSTWidget__buildCudaOptions())
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self._qcbverbose.setChecked(False)
        self._versoseFileWidget.setVisible(True)
        self._qcbverbose.toggled.connect(self._versoseFileWidget.setDisabled)
        self._makeConnection()
        self.getCudaDevices = self._cudaSelector.getExistingDevices()

    def setReconsParams(self, recons_params):
        if isinstance(recons_params, QReconsParams):
            _recons_params = recons_params.pyhst
        else:
            if isinstance(recons_params, _QPyhstRP):
                _recons_params = recons_params
            else:
                raise ValueError('recons_params should be an instance of QReconsParam or _QPyhstRP')
        if self._recons_params:
            self._recons_params.sigChanged.disconnect(self._update_params)
        self._recons_params = _recons_params
        self.load(self._recons_params)
        self._recons_params.sigChanged.connect(self._update_params)

    def _update_params(self):
        """Update all parameter"""
        self.load(self._recons_params)

    def _makeConnection(self):
        self._qcbverbose.toggled.connect(self._verboseChanged)
        self._qcbPyHSTVersion.currentIndexChanged.connect(self._pyHSTVersionChanged)
        self._qleVerboseFile.editingFinished.connect(self._verboseFileChanged)
        self._makeOARFileCB.toggled.connect(self._makeOARChanged)
        self._cudaSelector.selectionChanged.connect(self._cudaDevicesChanged)

    def _verboseChanged(self, b):
        self._recons_params['VERBOSE'] = b

    def __buildPYHSTVersion(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('PyHST version : ', parent=widget))
        self._qcbPyHSTVersion = qt.QComboBox(parent=self)
        widget.layout().addWidget(self._qcbPyHSTVersion)
        self.linkComboboxWithH5Variable((self._qcbPyHSTVersion), 'EXE',
          fitwithindex=False,
          setDefault=False)
        d = pyhstutils._getPyHSTDir()
        if d is None:
            raise logger.warning("Can't find the directory containing the PyHST\n                directory. Please set the environment variable\n                PYHST_DIR and run again")
        else:
            availablePyHSTVersion = pyhstutils._findPyHSTVersions(d)
            if len(availablePyHSTVersion) == 0:
                self._PyHSTWidget__warmNoPyHSTFound(d)
            else:
                [self._qcbPyHSTVersion.addItem(exe) for exe in availablePyHSTVersion]
        return widget

    def __buildMakeOAR(self):
        self._makeOARFileCB = qt.QCheckBox('make OAR file', parent=self)
        self.linkCheckboxWithH5Variable(qcheckbox=(self._makeOARFileCB), h5ParamName='MAKE_OAR_FILE')
        self._makeOARFileCB.toggled.connect(self._makeOARChanged)
        return self._makeOARFileCB

    def __buildCudaOptions(self):
        self._cudaSelector = CudaPlatfornGroup(parent=self)
        self._cudaSelector.activate_all()
        self.linkGroupWithH5Variable(group=(self._cudaSelector), h5ParamName='CUDA_DEVICES',
          setter=(self._cudaSelector.setDevices),
          getter=(self._cudaSelector.getSelectedDevices))
        old = self._recons_params.blockSignals(True)
        self._recons_params['CUDA_DEVICES'] = self._cudaSelector.getSelectedDevices()
        self._recons_params.blockSignals(old)
        return self._cudaSelector

    def _pyHSTVersionChanged(self):
        value = self._qcbPyHSTVersion.currentText()
        self._recons_params['EXE'] = value

    def _makeOARChanged(self, b):
        self._recons_params['MAKE_OAR_FILE'] = b

    def _cudaDevicesChanged(self, devices):
        self._recons_params.cuda_devices = devices

    def __buildPYHSTOfficialVersion(self):
        """build the official version QLine edit and update the _qcbPyHSTVersion
        combobox so should always be called after.
        """
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('PyHST official version', parent=widget))
        self._qlOfficalVersion = qt.QLabel('', parent=widget)
        widget.layout().addWidget(self._qlOfficalVersion)
        self.linkGroupWithH5Variable((self._qlOfficalVersion), 'OFFV',
          getter=(self._qlOfficalVersion.text),
          setter=(self._qlOfficalVersion.setText))
        return widget

    def __warmNoPyHSTFound(self, directory):
        """Simple function displaying a MessageBox that PyHST haven't been found
        """
        text = 'No executable of PyHST have been found in %s.' % directory
        text += ' You might set the environment variable PYHST_DIR '
        text += ' or install PyHST.'
        logger.info(text)

    def __buildVerboseFile(self):
        self._versoseFileWidget = qt.QWidget(self)
        self._versoseFileWidget.setLayout(qt.QHBoxLayout())
        self._versoseFileWidget.layout().addWidget(qt.QLabel('name of the PyHST information output file', parent=self))
        self._qleVerboseFile = qt.QLineEdit('', parent=None)
        self._versoseFileWidget.layout().addWidget(self._qleVerboseFile)
        self.LinkLineEditWithH5Variable(self._qleVerboseFile, 'VERBOSE_FILE')
        return self._versoseFileWidget

    def _verboseFileChanged(self):
        value = self._qleVerboseFile.text()
        self._recons_params._set_parameter_value(parameter='VERBOSE_FILE', value=value)