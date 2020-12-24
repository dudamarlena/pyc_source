# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/chartdelegate.py
# Compiled at: 2013-04-11 17:47:52
from camelot.view.controls.editors.charteditor import ChartEditor
from camelot.view.controls.delegates.customdelegate import CustomDelegate
import logging
LOGGER = logging.getLogger('camelot.view.controls.delegates.chartdelegate')

class ChartDelegate(CustomDelegate):
    """Custom delegate for Matplotlib charts
    """
    editor = ChartEditor

    def __init__(self, parent=None, **kwargs):
        super(ChartDelegate, self).__init__(parent)

    def setModelData(self, editor, model, index):
        pass