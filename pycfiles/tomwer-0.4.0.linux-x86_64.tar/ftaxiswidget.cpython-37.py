# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/reconsparamseditor/ftaxiswidget.py
# Compiled at: 2020-02-17 09:32:20
# Size of source mod 2**32: 7853 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.synctools.ftseries import QReconsParams
from tomwer.gui.reconstruction.ftserie.h5editor.h5structseditor import H5StructsEditor
try:
    from silx.gui.widgets.UrlSelectionTable import UrlSelectionDialog, ColumnMode
except ImportError:
    from tomwer.gui.UrlSelectionTable import UrlSelectionDialog, ColumnMode

logger = TomwerLogger(__name__)

class FTAxisWidget(H5StructsEditor, qt.QWidget):
    __doc__ = '\n    Widget containing all the information to edit the AXIS parameters\n\n    :param reconsparams: reconstruction parameters edited by the widget\n    '

    def __init__(self, reconsparams, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructsEditor.__init__(self, structsManaged=('FT', 'FTAXIS'))
        assert isinstance(reconsparams, QReconsParams)
        self._recons_params = None
        self.setReconsParams(recons_params=reconsparams)
        self.setLayout(qt.QVBoxLayout())
        self._qcbHalfAcq = qt.QCheckBox('Half acquisition (HA)', parent=self)
        self.layout().addWidget(self._qcbHalfAcq)
        self._doAxisCorrection = qt.QCheckBox('apply axis correction', parent=self)
        self._doAxisCorrection.setToolTip('If activated then ask to pyhst to do axis translation correction')
        self.layout().addWidget(self._doAxisCorrection)
        self._doAxisCorrection.hide()
        self._useTomwerAxis = qt.QCheckBox('use center of rotation computed upstream (if any)', parent=self)
        self._useTomwerAxis.setToolTip('If selected, the value computed upstream in this flow will be used. \nThis option has priority over other options')
        self.layout().addWidget(self._useTomwerAxis)
        self._useOldTomwerAxis = qt.QCheckBox('use center of rotation calculation from previous session (if any)', parent=self)
        self._useOldTomwerAxis.setToolTip('If the scan has already been processed by tomwer, the value of the center of rotation used had been recorded. \n')
        self.layout().addWidget(self._useOldTomwerAxis)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self.linkGroupWithH5Variable(group=(self._doAxisCorrection), structID='FTAXIS',
          h5ParamName='DO_AXIS_CORRECTION',
          setter=(self._setDoAxisCorrection),
          getter=(self._getDoAxisCorrection))
        self.linkGroupWithH5Variable(group=(self._useTomwerAxis), structID='FTAXIS',
          h5ParamName='USE_TOMWER_AXIS',
          setter=(self._setUseTomwerAxis),
          getter=(self._getUseTomwerAxis))
        self.linkGroupWithH5Variable(group=(self._useOldTomwerAxis), structID='FTAXIS',
          h5ParamName='TRY_USE_OLD_TOMWER_AXIS',
          setter=(self._setTryUseOldTomwerAxis),
          getter=(self._getTryUseOldTomwerAxis))
        self.linkCheckboxWithH5Variable((self._qcbHalfAcq), structID='FT',
          h5ParamName='HALF_ACQ')
        self._doAxisCorrection.toggled.connect(self._doAxisCorrectionChanged)
        self._useTomwerAxis.toggled.connect(self._useTomwerAxisChanged)
        self._useOldTomwerAxis.toggled.connect(self._useOldTomwerAxisChanged)
        self._qcbHalfAcq.toggled.connect(self._HALFACQChanged)

    def setReconsParams(self, recons_params):
        """
        Define the `.ReconsParams` that the widget edit. Those parameters will
        be copied in all the TomoBase process by the widget

        :param recons_params: tomographic parameter to edit
        :type recons_params: `.ReconsParams`
        """
        assert isinstance(recons_params, QReconsParams)
        if self._recons_params:
            self._recons_params.sigChanged.disconnect(self._update_params)
        self._recons_params = recons_params
        self.load(self._recons_params)
        self._recons_params.sigChanged.connect(self._update_params)

    def _update_params(self):
        """Update all parameter"""
        self.load(self._recons_params)

    def _setDoAxisCorrection(self, doAxisCorrrection: bool) -> None:
        assert type(doAxisCorrrection) is bool
        self._doAxisCorrection.setChecked(doAxisCorrrection)

    def _getDoAxisCorrection(self) -> bool:
        return self._doAxisCorrection.isChecked()

    def _setUseTomwerAxis(self, useTomwerAxis: bool) -> None:
        assert type(useTomwerAxis) is bool
        self._useTomwerAxis.setChecked(useTomwerAxis)

    def _getUseTomwerAxis(self) -> bool:
        return self._useTomwerAxis.isChecked()

    def _setTryUseOldTomwerAxis(self, useOldTomwerAxis: bool) -> None:
        assert type(useOldTomwerAxis) is bool
        self._useOldTomwerAxis.setChecked(useOldTomwerAxis)

    def _getTryUseOldTomwerAxis(self) -> bool:
        return self._useOldTomwerAxis

    def _doAxisCorrectionChanged(self, *args, **kwargs) -> None:
        doAxisCorrection = self._getDoAxisCorrection()
        self._recons_params['FTAXIS']['DO_AXIS_CORRECTION'] = doAxisCorrection

    def _useTomwerAxisChanged(self, *args, **kwargs) -> None:
        self._recons_params['FTAXIS']['USE_TOMWER_AXIS'] = self._getUseTomwerAxis()

    def _useOldTomwerAxisChanged(self, *args, **kwargs) -> None:
        self._recons_params['FTAXIS']['TRY_USE_OLD_TOMWER_AXIS'] = self._getTryUseOldTomwerAxis()

    def _HALFACQChanged(self, b):
        self._recons_params['FT']['HALF_ACQ'] = int(b)