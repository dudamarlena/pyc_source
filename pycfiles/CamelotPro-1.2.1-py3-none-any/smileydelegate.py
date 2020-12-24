# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/smileydelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls.editors.smileyeditor import SmileyEditor, default_icons

class SmileyDelegate(CustomDelegate):
    """Delegate for Smiley's
  """
    __metaclass__ = DocumentationMetaclass
    editor = SmileyEditor

    def __init__(self, parent, editable=True, icons=default_icons, **kwargs):
        CustomDelegate.__init__(self, parent=parent, editable=editable, icons=icons, **kwargs)
        self.icons_by_name = dict(icons)

    def paint(self, painter, option, index):
        painter.save()
        icon_name = unicode(index.model().data(index, Qt.DisplayRole).toString())
        background_color = QtGui.QColor(index.model().data(index, Qt.BackgroundRole))
        self.drawBackground(painter, option, index)
        rect = option.rect
        rect = QtCore.QRect(rect.left() + 3, rect.top() + 6, rect.width() - 5, rect.height())
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif not self.editable:
            painter.fillRect(option.rect, option.palette.window())
        else:
            painter.fillRect(option.rect, background_color)
        if icon_name:
            pixmap = self.icons_by_name[icon_name].getQPixmap()
            QtGui.QApplication.style().drawItemPixmap(painter, rect, 1, pixmap)
        painter.restore()