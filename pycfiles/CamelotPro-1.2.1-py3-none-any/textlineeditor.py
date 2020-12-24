# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/textlineeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from customeditor import AbstractCustomEditor, draw_tooltip_visualization

class TextLineEditor(QtGui.QLineEdit, AbstractCustomEditor):

    def __init__(self, parent, length=20, field_name='text_line', **kwargs):
        QtGui.QLineEdit.__init__(self, parent)
        self.setObjectName(field_name)
        AbstractCustomEditor.__init__(self)
        if length:
            self.setMaxLength(length)

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        if value is not None:
            self.setText(unicode(value))
        else:
            self.setText('')
        return value

    def get_value(self):
        value_loading = AbstractCustomEditor.get_value(self)
        if value_loading is not None:
            return value_loading
        else:
            value = unicode(self.text())
            if self.value_is_none and not value:
                return
            return value

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        self.set_background_color(background_color)
        self.set_enabled(editable)
        self.setToolTip(unicode(tooltip or ''))

    def set_enabled(self, editable=True):
        value = self.text()
        self.setEnabled(editable)
        self.setText(value)

    def paintEvent(self, event):
        super(TextLineEditor, self).paintEvent(event)
        if self.toolTip():
            draw_tooltip_visualization(self)