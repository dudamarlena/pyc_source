# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/recpyhstwidget.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 5113 bytes
"""GUI to call RecPyHST
"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/01/2017'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.core.utils import pyhstutils
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructsEditor
from tomwer.synctools.ftseries import QReconsParams, _QPyhstRP
logger = TomwerLogger(__name__)

class RecPyHSTWidget(H5StructsEditor, qt.QWidget):
    __doc__ = '\n    Widget to interface the `makeRecPyHST` function\n    '

    def __init__(self, recons_params, parent=None):
        qt.QWidget.__init__(self, parent)
        self.recons_params = None
        H5StructsEditor.__init__(self, structsManaged=('PYHSTEXE', ))
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._buildPyHSTEXE())
        self.layout().addWidget(self._buildMakeOARFile())
        self.setReconsParams(recons_params)

    def setReconsParams(self, recons_params):
        if isinstance(recons_params, _QPyhstRP):
            _recons_params = recons_params
        else:
            if isinstance(QReconsParams):
                _recons_params = recons_params.pyhst
            else:
                raise TypeError('recons_params should be an instance ot PyhstRP or ReconsParams')
        if self.recons_params:
            self.recons_params.sigChanged.disconnect(self._update)
        self.recons_params = _recons_params
        self.load(self.recons_params)
        self.recons_params.sigChanged.connect(self._update)

    def _buildPyHSTEXE(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QVBoxLayout())
        exe_widget = qt.QWidget()
        widget.layout().addWidget(exe_widget)
        exe_widget.setLayout(qt.QHBoxLayout())
        exe_widget.layout().addWidget(qt.QLabel('PyHST version : ', parent=exe_widget))
        self._qcbPyHSTVersion = qt.QComboBox(parent=self)
        self.linkComboboxWithH5Variable((self._qcbPyHSTVersion), structID='PYHSTEXE',
          h5ParamName='EXE')
        exe_widget.layout().addWidget(self._qcbPyHSTVersion)
        d = pyhstutils._getPyHSTDir()
        if d is None:
            logger.warning("Can't find the directory containing the PyHST\n                directory. Please set the environment variable\n                PYHST_DIR and run again")
            d = 'not found'
        else:
            availablePyHSTVersion = pyhstutils._findPyHSTVersions(d)
            if len(availablePyHSTVersion) == 0:
                logger.warning('No valid PyHST version found.')
            else:
                [self._qcbPyHSTVersion.addItem(exe) for exe in availablePyHSTVersion]
        pyhst_dir_widget = qt.QWidget(parent=widget)
        widget.layout().addWidget(pyhst_dir_widget)
        pyhst_dir_widget.setLayout(qt.QHBoxLayout())
        pyhst_dir_widget.layout().addWidget(qt.QLabel('PyHST directory:'))
        pyhst_dir_widget.layout().addWidget(qt.QLabel(d))
        self._qcbPyHSTVersion.currentIndexChanged.connect(self._pyHSTVersionChanged)
        return widget

    def _pyHSTVersionChanged(self):
        value = self._qcbPyHSTVersion.currentText()
        self.recons_params['EXE'] = value

    def _buildMakeOARFile(self):
        self._makeOARFileCB = qt.QCheckBox('make OAR file', parent=self)
        self.linkCheckboxWithH5Variable((self._makeOARFileCB), 'PYHSTEXE', 'MAKE_OAR_FILE',
          invert=False)
        self._makeOARFileCB.toggled.connect(self._makeOARChanged)
        return self._makeOARFileCB

    def _makeOARChanged(self, b):
        self.recons_params['MAKE_OAR_FILE'] = b

    def _update(self):
        self.load(self.recons_params)