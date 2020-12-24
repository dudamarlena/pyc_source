# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/FilterOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3028 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/07/2018'
from silx.gui import qt
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input, Output
from tomwer.web.client import OWClient
from tomwer.gui.conditions.filter import FileNameFilterWidget
from tomwer.core.scan.scanbase import TomoBase
import logging
logger = logging.getLogger(__name__)

class NameFilterOW(widget.OWWidget, OWClient):
    name = 'scan filter'
    id = 'orange.widgets.tomwer.filterow'
    description = "Simple widget which filter some data directory if the namedoesn't match with the pattern defined."
    icon = 'icons/namefilter.svg'
    priority = 106
    category = 'esrfWidgets'
    keywords = ['tomography', 'selection', 'tomwer', 'folder', 'filter']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name='data', type=TomoBase)

    class Outputs:
        data_out = Output(name='data', type=TomoBase)

    def __init__(self, parent=None):
        """
        """
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, logger)
        self.widget = FileNameFilterWidget(parent=self)
        self.widget.setContentsMargins(0, 0, 0, 0)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        layout.addWidget(spacer)

    @Inputs.data_in
    def applyfilter(self, scan):
        if self.widget.isFiltered(scan):
            assert isinstance(scan, TomoBase)
            self.Outputs.data_out.send(scan)