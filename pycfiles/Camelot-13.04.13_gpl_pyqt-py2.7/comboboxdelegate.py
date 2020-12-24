# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/comboboxdelegate.py
# Compiled at: 2013-04-11 17:47:52
import logging
logger = logging.getLogger('camelot.view.controls.delegates.comboboxdelegate')
from customdelegate import CustomDelegate, DocumentationMetaclass
from PyQt4.QtCore import Qt
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading

class ComboBoxDelegate(CustomDelegate):
    __metaclass__ = DocumentationMetaclass
    editor = editors.ChoicesEditor

    def setEditorData(self, editor, index):
        value = variant_to_pyobject(index.data(Qt.EditRole))
        field_attributes = variant_to_pyobject(index.data(Qt.UserRole))
        editor.set_field_attributes(**field_attributes)
        editor.set_value(value)

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.data(Qt.DisplayRole))
        if value in (None, ValueLoading):
            value = ''
        self.paint_text(painter, option, index, unicode(value))
        painter.restore()
        return