# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/stardelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from camelot.core.utils import variant_to_pyobject
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.view.art import Icon

class StarDelegate(CustomDelegate):
    """Delegate for integer values from ( default from 1 to 5)(Rating Delegate)  
    """
    __metaclass__ = DocumentationMetaclass
    editor = editors.StarEditor
    star_icon = Icon('tango/16x16/status/weather-clear.png')

    def __init__(self, parent=None, editable=True, maximum=5, **kwargs):
        CustomDelegate.__init__(self, parent=parent, editable=editable, maximum=maximum, **kwargs)
        self.maximum = maximum

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        stars = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        rect = option.rect
        rect = QtCore.QRect(rect.left() + 3, rect.top() + 6, rect.width() - 5, rect.height())
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            if not self.editable:
                painter.fillRect(option.rect, option.palette.window())
            pixmap = self.star_icon.getQPixmap()
            style = QtGui.QApplication.style()
            for i in range(self.maximum):
                if i + 1 <= stars:
                    style.drawItemPixmap(painter, rect, 1, pixmap)
                    rect = QtCore.QRect(rect.left() + 20, rect.top(), rect.width(), rect.height())

        painter.restore()