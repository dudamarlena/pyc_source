# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/textediteditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtCore
from wideeditor import WideEditor
from customeditor import AbstractCustomEditor, QtGui

class TextEditEditor(QtGui.QTextEdit, AbstractCustomEditor, WideEditor):
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, parent, length=20, editable=True, field_name='text', **kwargs):
        QtGui.QTextEdit.__init__(self, parent)
        self.setObjectName(field_name)
        AbstractCustomEditor.__init__(self)
        self.setReadOnly(not editable)

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        self.setText(unicode(value))
        return value

    def get_value(self):
        val = AbstractCustomEditor.get_value(self)
        if val is not None:
            return val
        else:
            return unicode(self.toPlainText())

    def set_enabled(self, editable=True):
        self.setEnabled(editable)