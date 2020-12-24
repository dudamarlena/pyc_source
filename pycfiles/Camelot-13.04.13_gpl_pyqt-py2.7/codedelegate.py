# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/codedelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading

class CodeDelegate(CustomDelegate):
    __metaclass__ = DocumentationMetaclass
    editor = editors.CodeEditor

    def __init__(self, parent=None, parts=[], separator='.', **kwargs):
        CustomDelegate.__init__(self, parent=parent, parts=parts, **kwargs)
        self.parts = parts
        self.separator = separator

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if value not in (None, ValueLoading):
            value_str = self.separator.join([ unicode(i) for i in value ])
        self.paint_text(painter, option, index, value_str, horizontal_align=Qt.AlignRight)
        painter.restore()
        return