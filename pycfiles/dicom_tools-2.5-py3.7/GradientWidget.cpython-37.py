# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/GradientWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2901 bytes
from ..Qt import QtGui, QtCore
from .GraphicsView import GraphicsView
import graphicsItems.GradientEditorItem as GradientEditorItem
import weakref, numpy as np
__all__ = [
 'GradientWidget']

class GradientWidget(GraphicsView):
    __doc__ = '\n    Widget displaying an editable color gradient. The user may add, move, recolor,\n    or remove colors from the gradient. Additionally, a context menu allows the \n    user to select from pre-defined gradients.\n    '
    sigGradientChanged = QtCore.Signal(object)
    sigGradientChangeFinished = QtCore.Signal(object)

    def __init__(self, parent=None, orientation='bottom', *args, **kargs):
        """
        The *orientation* argument may be 'bottom', 'top', 'left', or 'right' 
        indicating whether the gradient is displayed horizontally (top, bottom)
        or vertically (left, right) and on what side of the gradient the editable 
        ticks will appear.
        
        All other arguments are passed to 
        :func:`GradientEditorItem.__init__ <pyqtgraph.GradientEditorItem.__init__>`.
        
        Note: For convenience, this class wraps methods from 
        :class:`GradientEditorItem <pyqtgraph.GradientEditorItem>`.
        """
        GraphicsView.__init__(self, parent, useOpenGL=False, background=None)
        self.maxDim = 31
        kargs['tickPen'] = 'k'
        self.item = GradientEditorItem(*args, **kargs)
        self.item.sigGradientChanged.connect(self.sigGradientChanged)
        self.item.sigGradientChangeFinished.connect(self.sigGradientChangeFinished)
        self.setCentralItem(self.item)
        self.setOrientation(orientation)
        self.setCacheMode(self.CacheNone)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        self.setFrameStyle(QtGui.QFrame.NoFrame | QtGui.QFrame.Plain)

    def setOrientation(self, ort):
        """Set the orientation of the widget. May be one of 'bottom', 'top', 
        'left', or 'right'."""
        self.item.setOrientation(ort)
        self.orientation = ort
        self.setMaxDim()

    def setMaxDim(self, mx=None):
        if mx is None:
            mx = self.maxDim
        else:
            self.maxDim = mx
        if self.orientation in ('bottom', 'top'):
            self.setFixedHeight(mx)
            self.setMaximumWidth(16777215)
        else:
            self.setFixedWidth(mx)
            self.setMaximumHeight(16777215)

    def __getattr__(self, attr):
        return getattr(self.item, attr)