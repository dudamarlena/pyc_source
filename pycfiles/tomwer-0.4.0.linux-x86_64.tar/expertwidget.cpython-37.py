# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/reconsparamseditor/expertwidget.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 7896 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructEditor
from tomwer.synctools.ftseries import QReconsParams, _QFTRP
logger = TomwerLogger(__name__)

class ExpertWidget(H5StructEditor, qt.QWidget):
    __doc__ = '\n    Create the widget inside the Expert tab of the SimplifyH5ParamEditor\n    \n    :param reconsparams: reconstruction parameters edited by the widget\n    '

    def __init__(self, reconsparams, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='FT')
        self._recons_params = None
        self.setReconsParams(recons_params=reconsparams)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._ExpertWidget__buildNumPart())
        self.layout().addWidget(self._ExpertWidget__buildVersion())
        self.layout().addWidget(self._ExpertWidget__buildDataBase())
        self.layout().addWidget(self._ExpertWidget__buildNoCheck())
        self.layout().addWidget(self._ExpertWidget__buildZeroOffMask())
        self.layout().addWidget(self._ExpertWidget__buildFixHD())
        self.spacer = qt.QWidget(self)
        self.spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self.spacer)
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
        assert isinstance(self._recons_params, _QFTRP)
        self.load(self._recons_params)

    def _makeConnection(self):
        self._qsbNumPart.valueChanged.connect(self._numPartChanged)
        self._qcbDataBase.toggled.connect(self._dataBaseChanged)
        self._qcbNocheck.toggled.connect(self._noCheckChanged)
        self._qcbZeroRegionMask.toggled.connect(self._zeroRegionMaskChanged)
        self._qcbFixHD.toggled.connect(self._fixHDChanged)

    def __buildNumPart(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('length of the numerical part in the data filenames '))
        self._qsbNumPart = qt.QSpinBox(parent=widget)
        self._qsbNumPart.setMinimum(0)
        widget.layout().addWidget(self._qsbNumPart)
        self.linkGroupWithH5Variable(group=(self._qsbNumPart), h5ParamName='NUM_PART',
          setter=(self._setNumericalPart),
          getter=(self._getNumericalPart))
        return widget

    def _numPartChanged(self):
        if self._isLoading is False:
            value = self._qsbNumPart.value()
            self._recons_params._set_parameter_value(parameter='NUM_PART', value=value)

    def __buildVersion(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QHBoxLayout())
        widget.layout().addWidget(qt.QLabel('Version used:', parent=widget))
        self._qleVersion = qt.QLabel('', widget)
        widget.layout().addWidget(self._qleVersion)
        self.linkGroupWithH5Variable((self._qleVersion), 'VERSION',
          getter=(self._qleVersion.text),
          setter=(self._qleVersion.setText))
        spacer = qt.QWidget(widget)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        widget.layout().addWidget(spacer)
        widget.hide()
        return widget

    def __buildDataBase(self):
        self._qcbDataBase = qt.QCheckBox('put scan in tomoDB', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbDataBase, 'DATABASE')
        self._qcbDataBase.hide()
        return self._qcbDataBase

    def _dataBaseChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='DATABASE', value=(int(b)))

    def __buildNoCheck(self):
        self._qcbNocheck = qt.QCheckBox('force reconstruction of slices in ftseries', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbNocheck, 'NO_CHECK')
        return self._qcbNocheck

    def _noCheckChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='NO_CHECK', value=(int(b)))

    def __buildZeroOffMask(self):
        self._qcbZeroRegionMask = qt.QCheckBox('Set to zero the region outside the reconstruction mask', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbZeroRegionMask, 'ZEROOFFMASK')
        return self._qcbZeroRegionMask

    def _zeroRegionMaskChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='ZEROOFFMASK', value=(int(b)))

    def __buildFixHD(self):
        self._qcbFixHD = qt.QCheckBox('disable try fixed header size determination', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbFixHD, 'FIXHD')
        return self._qcbFixHD

    def _fixHDChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='FIXHD', value=(int(b)))

    def _setNumericalPart(self, val):
        self._qsbNumPart.setValue(val)

    def _getNumericalPart(self):
        return self._qsbNumPart.value()