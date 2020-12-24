# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/datedelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.constants import camelot_small_icon_width
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading
from camelot.view.utils import local_date_format

class DateDelegate(CustomDelegate):
    """Custom delegate for date values"""
    __metaclass__ = DocumentationMetaclass
    editor = editors.DateEditor

    def __init__(self, parent=None, **kwargs):
        CustomDelegate.__init__(self, parent, **kwargs)
        self.date_format = local_date_format()
        self._width = self._font_metrics.averageCharWidth() * (len(self.date_format) + 2) + camelot_small_icon_width * 2

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if value not in (None, ValueLoading):
            value_str = QtCore.QDate(value).toString(self.date_format)
        self.paint_text(painter, option, index, value_str, horizontal_align=Qt.AlignRight)
        painter.restore()
        return