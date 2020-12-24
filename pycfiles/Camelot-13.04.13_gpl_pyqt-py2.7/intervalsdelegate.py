# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/intervalsdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from customdelegate import DocumentationMetaclass, CustomDelegate
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading

class IntervalsDelegate(CustomDelegate):
    """Custom delegate for visualizing camelot.container.IntervalsContainer
  data:
  """
    __metaclass__ = DocumentationMetaclass

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        intervals_container = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        field_attributes = variant_to_pyobject(index.data(Qt.UserRole))
        editable, color, background_color = False, None, None
        if field_attributes != ValueLoading:
            editable = field_attributes.get('editable', False)
            background_color = field_attributes.get('background_color', QtGui.QColor(index.model().data(index, Qt.BackgroundRole)))
            color = field_attributes.get('color', None)
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif not editable:
            painter.fillRect(option.rect, option.palette.window())
        else:
            painter.fillRect(option.rect, background_color)
        if intervals_container and intervals_container != ValueLoading:
            rect = option.rect
            xscale = float(rect.width() - 4) / (intervals_container.max - intervals_container.min)
            xoffset = intervals_container.min * xscale + rect.x()
            yoffset = rect.y() + rect.height() / 2
            for interval in intervals_container.intervals:
                qcolor = QtGui.QColor(interval.color or color)
                pen = QtGui.QPen(qcolor)
                pen.setWidth(3)
                painter.setPen(pen)
                xscale_interval = xscale
                x1, x2 = xoffset + interval.begin * xscale_interval, xoffset + interval.end * xscale_interval
                painter.drawLine(x1, yoffset, x2, yoffset)
                painter.drawEllipse(x1 - 1, yoffset - 1, 2, 2)
                painter.drawEllipse(x2 - 1, yoffset - 1, 2, 2)
                pen = QtGui.QPen(Qt.white)

        painter.restore()
        return

    def createEditor(self, parent, option, index):
        pass

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass