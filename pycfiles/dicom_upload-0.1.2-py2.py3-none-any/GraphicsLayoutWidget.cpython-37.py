# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/GraphicsLayoutWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1478 bytes
from ..Qt import QtGui
import graphicsItems.GraphicsLayout as GraphicsLayout
from .GraphicsView import GraphicsView
__all__ = ['GraphicsLayoutWidget']

class GraphicsLayoutWidget(GraphicsView):
    """GraphicsLayoutWidget"""

    def __init__(self, parent=None, **kargs):
        GraphicsView.__init__(self, parent)
        self.ci = GraphicsLayout(**kargs)
        for n in ('nextRow', 'nextCol', 'nextColumn', 'addPlot', 'addViewBox', 'addItem',
                  'getItem', 'addLayout', 'addLabel', 'removeItem', 'itemIndex',
                  'clear'):
            setattr(self, n, getattr(self.ci, n))

        self.setCentralItem(self.ci)