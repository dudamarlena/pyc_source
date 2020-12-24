# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/timedelegate.py
# Compiled at: 2013-04-11 17:47:52
import datetime
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.utils import create_constant_function, variant_to_pyobject
from camelot.view.proxy import ValueLoading

class TimeDelegate(CustomDelegate):
    __metaclass__ = DocumentationMetaclass
    editor = editors.TimeEditor

    def __init__(self, parent=None, editable=True, **kwargs):
        CustomDelegate.__init__(self, parent, editable)
        locale = QtCore.QLocale()
        self.time_format = locale.timeFormat(locale.ShortFormat)

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if value not in (None, ValueLoading):
            time = QtCore.QTime(value.hour, value.minute, value.second)
            value_str = time.toString(self.time_format)
        self.paint_text(painter, option, index, value_str)
        painter.restore()
        return

    def setModelData(self, editor, model, index):
        value = editor.time()
        t = datetime.time(hour=value.hour(), minute=value.minute(), second=value.second())
        model.setData(index, create_constant_function(t))