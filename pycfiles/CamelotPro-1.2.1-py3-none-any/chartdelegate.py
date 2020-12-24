# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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