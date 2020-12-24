# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/visualization/RadioStackOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3365 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '01/08/2018'
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from tomwer.core.scan.scanbase import TomoBase
from tomwer.gui.stacks import RadioStack
import logging
logger = logging.getLogger(__name__)

class RadioStackOW(widget.OWWidget):
    __doc__ = '\n    This widget will make copy or virtual link to all received *slice* files\n    in order to group them all in one place and be able to browse those\n    (using the image stack of view in orange or a third software as silx view)\n\n    Options are:\n       - copy files or create sym link (set to sym link)\n       - overwrite if existing (set to False)\n\n    Behavior:\n        When the process receives a new data path ([scanPath]/[scan]) and if\n        no output folder has been defined manually them it will try to create\n        the folder [scanPath]/slices if not existing in order to redirect\n        the slices files.\n        If fails will ask for a directory.\n        If the output folder is already existing then move directly to the\n        copy. \n    '
    name = 'radio stack'
    id = 'orange.widgets.tomwer.slicesstack.radiostack'
    description = 'This widget will save all scan path given to here and extract received radio files with there shortestunique basename to be able to browse them'
    icon = 'icons/radiosstack.svg'
    priority = 27
    category = 'tomwer'
    keywords = ['tomography', 'radio', 'tomwer', 'stack', 'group']
    allows_cycle = True
    compress_signal = False
    want_main_area = True
    resizing_enabled = True

    class Inputs:
        data_in = Input(name='data', type=TomoBase)

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        self._box = gui.vBox(self.mainArea, self.name)
        self._viewer = RadioStack(parent=self)
        self._box.layout().addWidget(self._viewer)

    @Inputs.data_in
    def addLeafScan(self, scanID):
        self._viewer.addLeafScan(scanID)