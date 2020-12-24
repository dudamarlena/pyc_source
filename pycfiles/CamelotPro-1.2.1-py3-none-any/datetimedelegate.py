# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/datetimedelegate.py
# Compiled at: 2013-04-11 17:47:52
from customdelegate import CustomDelegate, DocumentationMetaclass, ValueLoading
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

class DateTimeDelegate(CustomDelegate):
    __metaclass__ = DocumentationMetaclass
    editor = editors.DateTimeEditor

    def __init__(self, parent=None, editable=True, **kwargs):
        CustomDelegate.__init__(self, parent, editable=editable, **kwargs)
        locale = QtCore.QLocale()
        self.datetime_format = locale.dateTimeFormat(locale.ShortFormat)

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if value not in (None, ValueLoading):
            date_time = QtCore.QDateTime(value.year, value.month, value.day, value.hour, value.minute, value.second)
            value_str = date_time.toString(self.datetime_format)
        self.paint_text(painter, option, index, value_str, horizontal_align=Qt.AlignRight)
        painter.restore()
        return