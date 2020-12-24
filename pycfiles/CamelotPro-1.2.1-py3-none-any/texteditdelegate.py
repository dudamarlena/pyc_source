# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/texteditdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.view.proxy import ValueLoading
from camelot.core.utils import ugettext, variant_to_pyobject

class TextEditDelegate(CustomDelegate):
    """Custom delegate for simple string values"""
    __metaclass__ = DocumentationMetaclass
    editor = editors.TextEditEditor

    def __init__(self, parent=None, **kwargs):
        CustomDelegate.__init__(self, parent, **kwargs)

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if value not in (None, ValueLoading):
            value_str = ugettext(value)
        self.paint_text(painter, option, index, value_str)
        painter.restore()
        return