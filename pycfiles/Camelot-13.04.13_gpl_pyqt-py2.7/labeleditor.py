# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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