# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/labeleditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from customeditor import AbstractCustomEditor, draw_tooltip_visualization

class LabelEditor(QtGui.QLabel, AbstractCustomEditor):
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None, text='<loading>', field_name='label', **kwargs):
        QtGui.QLabel.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        self.text = text

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        if value:
            self.setText(value)

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        self.setToolTip(unicode(tooltip or ''))

    def paintEvent(self, event):
        if self.toolTip():
            draw_tooltip_visualization(self)