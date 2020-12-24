# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/ftseries.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 6151 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '03/05/2019'
from silx.gui import qt
from tomwer.core.process.reconstruction.ftseries.params import ReconsParams, beamgeo, axis, paganin
from tomwer.core.process.reconstruction.ftseries.params import pyhst, ft
import tomwer.core.process.reconstruction.darkref as dkrf
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class _QAxisRP(axis.AxisRP, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        axis.AxisRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()


class _QBeamGeoRP(beamgeo.BeamGeoRP, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        beamgeo.BeamGeoRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()


class _QDKRFRP(dkrf.DKRFRP, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        dkrf.DKRFRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()


class _QFTRP(ft.FTRP, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        ft.FTRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()


class _QPaganinRP(paganin.PaganinRP, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        paganin.PaganinRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()


class _QPyhstRP(pyhst.PyhstRP, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        pyhst.PyhstRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()


class QReconsParams(ReconsParams, qt.QObject):
    sigChanged = qt.Signal()

    def __init__(self, empty=False):
        ReconsParams.__init__(self, empty=empty)
        qt.QObject.__init__(self)
        if self._ft:
            self._ft.sigChanged.connect(self.changed)
        if self._pyhst:
            self._pyhst.sigChanged.connect(self.changed)
        if self.axis:
            self._axis.sigChanged.connect(self.changed)
        if self.paganin:
            self._paganin.sigChanged.connect(self.changed)
        if self.beam_geo:
            self._beam_geo.sigChanged.connect(self.changed)
        if self.dkrf:
            self._dkrf.sigChanged.connect(self.changed)

    def _createSubParamsSet(self, empty):
        self._ft = None if empty else _QFTRP()
        self._pyhst = None if empty else _QPyhstRP()
        self._axis = None if empty else _QAxisRP()
        self._paganin = None if empty else _QPaganinRP()
        self._beam_geo = None if empty else _QBeamGeoRP()
        self._dkrf = None if empty else _QDKRFRP()

    def changed(self):
        self.sigChanged.emit()

    def _copy_ft_rp(self, other_rp):
        create_connection = self.ft is None
        ReconsParams._copy_ft_rp(self, other_rp=other_rp)
        if create_connection:
            self._ft.sigChanged.connect(self.changed)

    def _copy_pyhst_rp(self, other_rp):
        create_connection = self.pyhst is None
        ReconsParams._copy_pyhst_rp(self, other_rp=other_rp)
        if create_connection:
            self._pyhst.sigChanged.connect(self.changed)

    def _copy_axis_rp(self, other_rp):
        create_connection = self.axis is None
        ReconsParams._copy_axis_rp(self, other_rp=other_rp)
        if create_connection:
            self._axis.sigChanged.connect(self.changed)

    def _copy_paganin_rp(self, other_rp):
        create_connection = self.paganin is None
        ReconsParams._copy_paganin_rp(self, other_rp=other_rp)
        if create_connection:
            self._paganin.sigChanged.connect(self.changed)

    def _copy_beam_geo_rp(self, other_rp):
        create_connection = self.beam_geo is None
        ReconsParams._copy_beam_geo_rp(self, other_rp=other_rp)
        if create_connection:
            self._beam_geo.sigChanged.connect(self.changed)

    def _copy_dkrf_rp(self, other_rp):
        create_connection = self.dkrf is None
        ReconsParams._copy_dkrf_rp(self, other_rp=other_rp)
        if create_connection:
            self._dkrf.sigChanged.connect(self.changed)