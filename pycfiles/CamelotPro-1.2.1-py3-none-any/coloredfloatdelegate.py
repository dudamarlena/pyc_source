# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/coloredfloatdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.proxy import ValueLoading
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject
from camelot.view.art import Icon

class ColoredFloatDelegate(CustomDelegate):
    """Custom delegate for float values.

  The class attribute icons is used to customize the icons displayed.
  """
    __metaclass__ = DocumentationMetaclass
    editor = editors.ColoredFloatEditor
    icons = {1: 'tango/16x16/actions/go-up.png', 
       -1: 'tango/16x16/actions/go-down-red.png', 
       0: 'tango/16x16/actions/zero.png'}

    def __init__(self, parent=None, precision=2, reverse=False, neutral=False, unicode_format=None, **kwargs):
        CustomDelegate.__init__(self, parent=parent, reverse=reverse, neutral=neutral, precision=precision, unicode_format=unicode_format, **kwargs)
        self.precision = precision
        self.reverse = reverse
        self.neutral = neutral
        self.unicode_format = unicode_format
        self._locale = QtCore.QLocale()

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        field_attributes = variant_to_pyobject(index.data(Qt.UserRole))
        fontColor = QtGui.QColor()
        editable, prefix, suffix, background_color, arrow = (True, '', '', None, None)
        if field_attributes != ValueLoading:
            editable = field_attributes.get('editable', True)
            prefix = field_attributes.get('prefix', '')
            suffix = field_attributes.get('suffix', '')
            background_color = field_attributes.get('background_color', None)
            arrow = field_attributes.get('arrow', None)
        fontColor = QtGui.QColor()
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif editable:
            painter.fillRect(option.rect, background_color or option.palette.base())
            fontColor.setRgb(0, 0, 0)
        else:
            painter.fillRect(option.rect, background_color or option.palette.window())
            fontColor.setRgb(130, 130, 130)
        if arrow:
            comparator = arrow.y
        else:
            comparator = value
        iconpath = self.icons[cmp(comparator, 0)]
        icon = QtGui.QIcon(Icon(iconpath).getQPixmap())
        icon.paint(painter, option.rect.left(), option.rect.top() + 1, option.rect.height(), option.rect.height(), Qt.AlignVCenter)
        value_str = ''
        if value != None and value != ValueLoading:
            if self.unicode_format != None:
                value_str = self.unicode_format(value)
            else:
                value_str = unicode(self._locale.toString(float(value), 'f', self.precision))
        value_str = unicode(prefix) + ' ' + unicode(value_str) + ' ' + unicode(suffix)
        fontColor = fontColor.darker()
        painter.setPen(fontColor.toRgb())
        rect = QtCore.QRect(option.rect.left() + 23, option.rect.top(), option.rect.width() - 23, option.rect.height())
        painter.drawText(rect.x() + 2, rect.y(), rect.width() - 4, rect.height(), Qt.AlignVCenter | Qt.AlignRight, value_str)
        painter.restore()
        return