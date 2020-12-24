# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/reconsparamseditor/beamgeowidget.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 6368 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructEditor
from tomwer.synctools.ftseries import QReconsParams, _QBeamGeoRP
logger = TomwerLogger(__name__)

class BeamGeoWidget(H5StructEditor, qt.QWidget):
    __doc__ = '\n    Definition of the PyHST tab to edit the Geometry parameters\n    \n    :param reconsparams: reconstruction parameters edited by the widget\n    '

    def __init__(self, parent=None, reconsparams=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='BEAMGEO')
        self._recons_params = None
        self.setReconsParams(recons_params=reconsparams)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._BeamGeoWidget__buildType())
        self.layout().addWidget(self._BeamGeoWidget__buildSXSYDist())
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self._makeConnection()

    def setReconsParams(self, recons_params):
        if isinstance(recons_params, QReconsParams):
            _recons_params = recons_params.beam_geo
        else:
            if isinstance(recons_params, _QBeamGeoRP):
                _recons_params = recons_params
            else:
                raise ValueError('recons_params should be an instance of QReconsParam or _QBeamGeoRP')
        if self._recons_params:
            self._recons_params.sigChanged.disconnect(self._update_params)
        self._recons_params = _recons_params
        self.load(self._recons_params)
        self._recons_params.sigChanged.connect(self._update_params)

    def _update_params(self):
        """Update all parameter"""
        self.load(self._recons_params)

    def _makeConnection(self):
        self._qcbType.currentIndexChanged.connect(self._typeChanged)
        self._qleSX.editingFinished.connect(self._SXChanged)
        self._qleSY.editingFinished.connect(self._SYChanged)
        self._qleDIST.editingFinished.connect(self._distChanged)

    def __buildType(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('Reconstruction geometry :', widget))
        self._qcbType = qt.QComboBox(widget)
        self.dic = {'parallel':'p', 
         'conical':'c', 
         'fan beam':'f'}
        for key in self.dic.keys():
            self._qcbType.addItem(key)

        self.linkComboboxWithH5Variable((self._qcbType), 'TYPE', dic=(self.dic))
        widget.layout().addWidget(self._qcbType)
        return widget

    def _typeChanged(self):
        if self._isLoading is False:
            value = self.dic[self._qcbType.currentText()]
            self._recons_params._set_parameter_value(parameter='TYPE', value=value)

    def __buildSXSYDist(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QGridLayout())
        self._qleSX = qt.QLineEdit('', parent=widget)
        self.LinkLineEditWithH5Variable(self._qleSX, 'SX', float)
        validator = qt.QDoubleValidator(parent=(self._qleSX))
        self._qleSX.setValidator(validator)
        widget.layout().addWidget(self._qleSX, 0, 1)
        widget.layout().addWidget(qt.QLabel('Source position on vertical axis X (mm)', parent=widget), 0, 0)
        self._qleSY = qt.QLineEdit('', parent=widget)
        self.LinkLineEditWithH5Variable(self._qleSY, 'SY', float)
        validator = qt.QDoubleValidator(parent=(self._qleSY))
        self._qleSY.setValidator(validator)
        widget.layout().addWidget(self._qleSY, 1, 1)
        widget.layout().addWidget(qt.QLabel('Source position on vertical axis Y (mm)', parent=widget), 1, 0)
        self._qleDIST = qt.QLineEdit('', parent=widget)
        self.LinkLineEditWithH5Variable(self._qleDIST, 'DIST', float)
        validator = qt.QDoubleValidator(parent=(self._qleDIST))
        self._qleDIST.setValidator(validator)
        widget.layout().addWidget(self._qleDIST, 2, 1)
        widget.layout().addWidget(qt.QLabel('Source distance (m)', parent=widget), 2, 0)
        return widget

    def _SXChanged(self):
        if self._isLoading is False:
            value = float(self._qleSX.text())
            self._recons_params._set_parameter_value(parameter='SX', value=value)

    def _SYChanged(self):
        if self._isLoading is False:
            value = float(self._qleSY.text())
            self._recons_params._set_parameter_value(parameter='SY', value=value)

    def _distChanged(self):
        if self._isLoading is False:
            value = float(self._qleDIST.text())
            self._recons_params._set_parameter_value(parameter='DIST', value=value)