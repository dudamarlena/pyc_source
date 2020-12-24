# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/utils/roi.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 4904 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '02/10/2018'
import logging
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
import Orange.data
from orangecontrib.est.utils import Converter
from silx.gui import qt
import est.core.process.roi
from est.core.types import XASObject
from est.gui.roiselector import ROISelector
_logger = logging.getLogger(__file__)

class RoiSelectionOW(OWWidget):
    __doc__ = '\n    Widget used to make the selection of a region of Interest to treat in a\n    Dataset.\n    '
    name = 'ROI definition'
    id = 'orange.widgets.xas.utils.roiselection'
    description = 'Select data Region Of Interest'
    icon = 'icons/image-select-box.svg'
    priority = 10
    category = 'esrfWidgets'
    keywords = ['dataset', 'data', 'selection', 'ROI', 'Region of Interest']
    process_function = est.core.process.roi.ROIProcess
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    _roi_origin = Setting(tuple())
    _roi_size = Setting(tuple())

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)
        data_table = Input('Data', Orange.data.Table)

    class Outputs:
        res_xas_obj = Output('xas_obj', XASObject)

    def __init__(self):
        super().__init__()
        self._widget = ROISelector(parent=self)
        layout = gui.vBox(self.mainArea, 'data selection').layout()
        layout.addWidget(self._widget)
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        layout.addWidget(self._buttons)
        self._buttons.hide()
        self._buttons.accepted.connect(self.validate)
        self.setROI = self._widget.setROI
        self.getROI = self._widget.getROI

    @Inputs.data_table
    def processFrmDataTable(self, data_table):
        if data_table is None:
            return
        self.process(Converter.toXASObject(data_table=data_table))

    @Inputs.xas_obj
    def process(self, xas_obj):
        if xas_obj is None:
            return
        self._widget.setXasObject(xas_obj=xas_obj)
        self._buttons.show()
        self.show()

    def validate(self):
        """
        callback when the ROI has been validated
        """
        if self._widget.getXasObject() is None:
            return
        try:
            roi_process = est.core.process.roi.ROIProcess()
            xas_roi = est.core.process.roi._ROI.from_silx_def(self.getROI()).to_dict()
            roi_prop = {'roi': xas_roi}
            roi_process.setProperties(roi_prop)
            xas_obj = roi_process.process(xas_obj=(self._widget.getXasObject().copy()))
            self.Outputs.res_xas_obj.send(xas_obj)
        except Exception as e:
            try:
                _logger.error(e)
            finally:
                e = None
                del e

        else:
            OWWidget.accept(self)

    def updateProperties(self):
        self._roi_origin = tuple(self._widget.getROI().getOrigin())
        self._roi_size = tuple(self._widget.getROI().getSize())