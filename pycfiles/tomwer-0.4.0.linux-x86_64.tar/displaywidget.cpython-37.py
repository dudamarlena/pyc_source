# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/reconsparamseditor/displaywidget.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 6670 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructEditor
from tomwer.synctools.ftseries import QReconsParams, _QFTRP
logger = TomwerLogger(__name__)

class DisplayWidget(H5StructEditor, qt.QWidget):
    __doc__ = '\n     Create the widget inside the of the Display tab\n\n     :param _ReconsParam reconsparams: reconstruction parameters edited by the\n                                       widget\n     '

    def __init__(self, reconsparams, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='FT')
        self._recons_params = None
        self.setReconsParams(reconsparams)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._DisplayWidget__buildShowProj())
        self.layout().addWidget(self._DisplayWidget__buildShowSlice())
        self.layout().addWidget(self._DisplayWidget__buildAngleOffset())
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self._makeConnection()

    def setReconsParams(self, recons_params):
        if isinstance(recons_params, QReconsParams):
            _recons_params = recons_params.ft
        else:
            if isinstance(recons_params, _QFTRP):
                _recons_params = recons_params
            else:
                raise ValueError('recons_params should be an instance of QReconsParam or _QFTRP')
        if self._recons_params:
            self._recons_params.sigChanged.disconnect(self._update_params)
        self._recons_params = _recons_params
        self.load(self._recons_params)
        self._recons_params.sigChanged.connect(self._update_params)

    def _update_params(self):
        """Update all parameter"""
        self.load(self._recons_params)

    def _makeConnection(self):
        self._qcbShowProj.toggled.connect(self._showProjChanged)
        self._qcbShowSlice.toggled.connect(self._showSliceChanged)
        self._qleAngleOffset.editingFinished.connect(self._angleOffsetValueChanged)
        self._qleAngleOffset.editingFinished.connect(self._angleOffsetChanged)

    def __buildShowProj(self):
        self._qcbShowProj = qt.QCheckBox('show graphical proj during reconstruction', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbShowProj, 'SHOWPROJ')
        self._qcbShowProj.hide()
        return self._qcbShowProj

    def _showProjChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='SHOWPROJ', value=(int(b)))

    def __buildShowSlice(self):
        self._qcbShowSlice = qt.QCheckBox('show graphical slice during reconstruction', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbShowSlice, 'SHOWSLICE')
        self._qcbShowSlice.hide()
        return self._qcbShowSlice

    def _showSliceChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='SHOWSLICE', value=(int(b)))

    def __buildAngleOffset(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('Final image rotation angle (degree):', parent=widget))
        self._qleAngleOffset = qt.QLineEdit('', widget)
        validator = qt.QDoubleValidator(parent=(self._qleAngleOffset))
        self._qleAngleOffset.setValidator(validator)
        widget.layout().addWidget(self._qleAngleOffset)
        self.LinkLineEditWithH5Variable(self._qleAngleOffset, 'ANGLE_OFFSET_VALUE', float)
        self.linkGroupWithH5Variable(group=None, h5ParamName='ANGLE_OFFSET',
          setter=None,
          getter=(self._getAngleOffsetParamVal))
        return widget

    def _getAngleOffsetParamVal(self):
        """

        :return: True if ANGLE_OFFSET_VALUE != 0
        """
        return int(float(self._qleAngleOffset.text()) != 0.0)

    def _angleOffsetChanged(self):
        if self._isLoading is False:
            value = self._getAngleOffsetParamVal()
            self._recons_params._set_parameter_value(parameter='ANGLE_OFFSET', value=value)

    def _angleOffsetValueChanged(self):
        if self._isLoading is False:
            value = float(self._qleAngleOffset.text())
            self._recons_params._set_parameter_value(parameter='ANGLE_OFFSET_VALUE', value=value)