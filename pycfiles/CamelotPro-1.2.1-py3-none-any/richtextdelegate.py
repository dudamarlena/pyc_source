# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/richtextdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.view.proxy import ValueLoading

class RichTextDelegate(CustomDelegate):
    """Custom delegate for rich text (HTML) string values
  """
    __metaclass__ = DocumentationMetaclass
    editor = editors.RichTextEditor

    def __init__(self, parent=None, editable=True, **kwargs):
        CustomDelegate.__init__(self, parent, editable)
        self.editable = editable
        self._height = self._height * 10
        self._width = self._width * 3

    def paint(self, painter, option, index):
        from camelot.view.utils import text_from_richtext
        painter.save()
        self.drawBackground(painter, option, index)
        value = unicode(index.model().data(index, Qt.EditRole).toString())
        value_str = ''
        if value not in (None, ValueLoading):
            value_str = (' ').join(text_from_richtext(value))[:256]
        self.paint_text(painter, option, index, value_str)
        painter.restore()
        return