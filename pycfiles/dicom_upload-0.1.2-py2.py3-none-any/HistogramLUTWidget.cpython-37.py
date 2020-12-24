# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/HistogramLUTWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 940 bytes
__doc__ = '\nWidget displaying an image histogram along with gradient editor. Can be used to adjust the appearance of images.\nThis is a wrapper around HistogramLUTItem\n'
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