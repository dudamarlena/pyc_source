# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/colordelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading

class ColorDelegate(CustomDelegate):
    __metaclass__ = DocumentationMetaclass
    editor = editors.ColorEditor

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        field_attributes = variant_to_pyobject(index.model().data(index, Qt.UserRole))
        color = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        editable = True
        background_color = None
        if field_attributes != ValueLoading:
            editable = field_attributes.get('editable', True)
            background_color = field_attributes.get('background_color', None)
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif not editable:
            painter.fillRect(option.rect, background_color or option.palette.window())
        else:
            painter.fillRect(option.rect, background_color or option.palette.base())
        if color not in (None, ValueLoading):
            qcolor = QtGui.QColor()
            qcolor.setRgb(*color)
            rect = QtCore.QRect(option.rect.left() + 1, option.rect.top() + 1, option.rect.width() - 2, option.rect.height() - 2)
            painter.fillRect(rect, qcolor)
        painter.restore()
        return