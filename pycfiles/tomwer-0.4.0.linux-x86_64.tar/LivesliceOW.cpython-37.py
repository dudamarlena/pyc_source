# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/visualization/LivesliceOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3018 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '26/06/2018'
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from tomwer.core.utils import getFirstProjFile
from tomwer.core.scan.scanbase import TomoBase
try:
    from liveslice.gui.liveslice_gui import ReconstructionApp
except:
    has_liveslice = False
else:
    has_liveslice = True
import logging
_logger = logging.getLogger(__name__)
if has_liveslice is True:

    class LiveSliceOW(widget.OWWidget):
        __doc__ = '\n        Simple widget displaying the live slice interface if found\n\n\n        :param parent: the parent widget\n        '
        name = 'live slice'
        id = 'orange.widgets.tomwer.liveslice'
        priority = 36
        icon = 'icons/liveslice.png'
        category = 'esrfWidgets'
        keywords = ['tomography', 'live slice', 'reconstruction',
         'visualization']
        want_main_area = True
        resizing_enabled = True
        compress_signal = False

        class Inputs:
            data_in = Input(name='data', type=TomoBase)

        def __init__(self, parent=None):
            widget.OWWidget.__init__(self, parent)
            layout = gui.vBox(self.mainArea, self.name).layout()
            self._mainWidget = ReconstructionApp()
            self._mainWidget.close_button.hide()
            layout.addWidget(self._mainWidget)

        @Inputs.data_in
        def updateScan(self, scanID):
            if scanID is not None:
                first_proj_file = getFirstProjFile(scanID)
                if first_proj_file is not None:
                    self._mainWidget.setSinoPath(first_proj_file)
                    self._mainWidget.initiate()