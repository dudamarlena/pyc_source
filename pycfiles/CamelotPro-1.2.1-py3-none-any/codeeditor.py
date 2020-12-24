# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/codeeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from camelot.view.model_thread import object_thread
from customeditor import CustomEditor, set_background_color_palette, draw_tooltip_visualization
import re

class PartEditor(QtGui.QLineEdit):

    def __init__(self, mask, max_length, first=False, last=False):
        super(PartEditor, self).__init__()
        self.setInputMask(mask)
        self.firstPart = first
        self.last = last
        self.max_length = max_length
        self.textEdited.connect(self.text_edited)

    def focusInEvent(self, event):
        super(PartEditor, self).focusInEvent(event)
        self.setCursorPosition(0)

    def focusOutEvent(self, event):
        super(PartEditor, self).focusOutEvent(event)
        if self.isModified():
            self.editingFinished.emit()

    def paintEvent(self, event):
        super(PartEditor, self).paintEvent(event)
        if self.firstPart and self.toolTip():
            draw_tooltip_visualization(self)

    @QtCore.pyqtSlot(str)
    def text_edited(self, text):
        if self.cursorPosition() == self.max_length:
            if self.last:
                self.editingFinished.emit()
            else:
                self.focusNextChild()


class CodeEditor(CustomEditor):

    def __init__(self, parent=None, parts=['99', 'AA'], editable=True, field_name='code', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setObjectName(field_name)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.value = None
        self.parts = parts
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignLeft)
        for i, part in enumerate(parts):
            part = re.sub('\\W*', '', part)
            part_length = len(part)
            editor = PartEditor(part, part_length, i == 0, i == len(parts) - 1)
            editor.setFocusPolicy(Qt.StrongFocus)
            if i == 0:
                self.setFocusProxy(editor)
            if not editable:
                editor.setEnabled(False)
            space_width = editor.fontMetrics().size(Qt.TextSingleLine, 'A').width()
            editor.setMaximumWidth(space_width * (part_length + 1))
            editor.setObjectName('part_%i' % i)
            layout.addWidget(editor)
            editor.editingFinished.connect(self.emit_editing_finished)

        self.setLayout(layout)
        return

    @QtCore.pyqtSlot()
    def emit_editing_finished(self):
        for editor in self._get_part_editors():
            if editor.isModified():
                self.editingFinished.emit()
                return

    def _get_part_editors(self):
        for i in range(len(self.parts)):
            part_editor = self.findChild(QtGui.QWidget, 'part_%s' % i)
            yield part_editor

    def set_enabled(self, editable=True):
        for editor in self._get_part_editors():
            editor.setEnabled(editable)

    def set_value(self, value):
        assert object_thread(self)
        value = CustomEditor.set_value(self, value)
        if value:
            old_value = self.get_value()
            if value != old_value:
                for part_editor, part in zip(self._get_part_editors(), value):
                    part_editor.setText(unicode(part))

        else:
            for part_editor in self._get_part_editors():
                part_editor.setText('')

    def get_value(self):
        assert object_thread(self)
        value = []
        for part_editor in self._get_part_editors():
            value.append(unicode(part_editor.text()))

        return CustomEditor.get_value(self) or value

    def set_background_color(self, background_color):
        for editor in self._get_part_editors():
            set_background_color_palette(editor, background_color)

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        assert object_thread(self)
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.layout().itemAt(0).widget().setToolTip(unicode(tooltip or ''))