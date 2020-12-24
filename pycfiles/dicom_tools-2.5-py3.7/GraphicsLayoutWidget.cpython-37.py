# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/GraphicsLayoutWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1478 bytes
from ..Qt import QtGui
import graphicsItems.GraphicsLayout as GraphicsLayout
from .GraphicsView import GraphicsView
__all__ = ['GraphicsLayoutWidget']

class GraphicsLayoutWidget(GraphicsView):
    __doc__ = '\n    Convenience class consisting of a :class:`GraphicsView \n    <pyqtgraph.GraphicsView>` with a single :class:`GraphicsLayout\n    <pyqtgraph.GraphicsLayout>` as its central item. \n\n    This class wraps several methods from its internal GraphicsLayout:\n    :func:`nextRow <pyqtgraph.GraphicsLayout.nextRow>`\n    :func:`nextColumn <pyqtgraph.GraphicsLayout.nextColumn>`\n    :func:`addPlot <pyqtgraph.GraphicsLayout.addPlot>`\n    :func:`addViewBox <pyqtgraph.GraphicsLayout.addViewBox>`\n    :func:`addItem <pyqtgraph.GraphicsLayout.addItem>`\n    :func:`getItem <pyqtgraph.GraphicsLayout.getItem>`\n    :func:`addLabel <pyqtgraph.GraphicsLayout.addLabel>`\n    :func:`addLayout <pyqtgraph.GraphicsLayout.addLayout>`\n    :func:`removeItem <pyqtgraph.GraphicsLayout.removeItem>`\n    :func:`itemIndex <pyqtgraph.GraphicsLayout.itemIndex>`\n    :func:`clear <pyqtgraph.GraphicsLayout.clear>`\n    '

    def __init__(self, parent=None, **kargs):
        GraphicsView.__init__(self, parent)
        self.ci = GraphicsLayout(**kargs)
        for n in ('nextRow', 'nextCol', 'nextColumn', 'addPlot', 'addViewBox', 'addItem',
                  'getItem', 'addLayout', 'addLabel', 'removeItem', 'itemIndex',
                  'clear'):
            setattr(self, n, getattr(self.ci, n))

        self.setCentralItem(self.ci)