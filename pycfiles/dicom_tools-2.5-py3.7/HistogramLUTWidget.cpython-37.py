# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/HistogramLUTWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 940 bytes
"""
Widget displaying an image histogram along with gradient editor. Can be used to adjust the appearance of images.
This is a wrapper around HistogramLUTItem
"""
from ..Qt import QtGui, QtCore
from .GraphicsView import GraphicsView
import graphicsItems.HistogramLUTItem as HistogramLUTItem
__all__ = [
 'HistogramLUTWidget']

class HistogramLUTWidget(GraphicsView):

    def __init__(self, parent=None, *args, **kargs):
        background = kargs.get('background', 'default')
        GraphicsView.__init__(self, parent, useOpenGL=False, background=background)
        self.item = HistogramLUTItem(*args, **kargs)
        self.setCentralItem(self.item)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.setMinimumWidth(95)

    def sizeHint(self):
        return QtCore.QSize(115, 200)

    def __getattr__(self, attr):
        return getattr(self.item, attr)