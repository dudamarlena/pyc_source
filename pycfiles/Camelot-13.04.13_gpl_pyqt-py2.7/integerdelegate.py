# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/integerdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading

class IntegerDelegate(CustomDelegate):
    """Custom delegate for integer values"""
    __metaclass__ = DocumentationMetaclass
    editor = editors.IntegerEditor

    def __init__(self, parent=None, unicode_format=None, **kwargs):
        CustomDelegate.__init__(self, parent=parent, **kwargs)
        self.unicode_format = unicode_format
        self.locale = QtCore.QLocale()

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        if value in (None, ValueLoading):
            value_str = ''
        else:
            value_str = self.locale.toString(long(value))
        if self.unicode_format is not None:
            value_str = self.unicode_format(value)
        self.paint_text(painter, option, index, value_str, horizontal_align=Qt.AlignRight)
        painter.restore()
        return