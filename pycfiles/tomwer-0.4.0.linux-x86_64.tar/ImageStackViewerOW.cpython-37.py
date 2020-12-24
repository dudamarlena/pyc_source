# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/visualization/ImageStackViewerOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3427 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '01/12/2016'
from silx.gui import qt
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.gui.viewerqwidget import ScanWidget
from tomwer.core.scan.scanbase import TomoBase
import logging
logger = logging.getLogger(__name__)

class ImageStackViewerOW(widget.OWWidget):
    __doc__ = 'a simple viewer of image stack\n\n    :param parent:the parent widget\n    :param FtserieReconstruction ftseries: the initial reconstruction to show\n    '
    name = 'data viewer'
    id = 'orange.widgets.tomwer.imagestackviewer'
    description = 'Show a small recap of the reconstruction runned'
    icon = 'icons/eye.png'
    priority = 70
    category = 'esrfWidgets'
    keywords = ['tomography', 'file', 'tomwer', 'acquisition', 'validation']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name='data', type=TomoBase)

    def __init__(self, parent=None, ftseries=None):
        widget.OWWidget.__init__(self, parent)
        self.tabsWidget = {}
        self._scanWidgetLayout = gui.vBox(self.mainArea, self.name).layout()
        self.viewer = ScanWidget(parent=self, canLoadOtherScan=False)
        self._scanWidgetLayout.addWidget(self.viewer)
        self._scanWidgetLayout.setContentsMargins(0, 0, 0, 0)
        if ftseries is not None:
            self.viewer.updateData(ftseries)

    @Inputs.data_in
    def addScan(self, ftseriereconstruction):
        if ftseriereconstruction is None:
            return
        _ftserie = ftseriereconstruction
        if type(ftseriereconstruction) is str:
            _ftserie = ScanFactory.create_scan_object(_ftserie)
        assert isinstance(_ftserie, TomoBase)
        return self.viewer.updateData(_ftserie)

    def updateFromPath(self, path):
        if path is not None:
            return self.viewer.updateFromPath(path)

    def sizeHint(self):
        return qt.QSize(400, 500)