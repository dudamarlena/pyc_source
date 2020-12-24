# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/datetimeeditor.py
# Compiled at: 2013-04-11 17:47:52
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from customeditor import CustomEditor, set_background_color_palette
from dateeditor import DateEditor
from camelot.view.proxy import ValueLoading

class TimeValidator(QtGui.QValidator):

    def __init__(self, parent, nullable):
        QtGui.QValidator.__init__(self, parent)
        self._nullable = nullable

    def validate(self, input, pos):
        parts = str(input).split(':')
        if len(parts) != 2:
            return (QtGui.QValidator.Invalid, pos)
        if str(input) == '--:--' and self._nullable:
            return (QtGui.QValidator.Acceptable, pos)
        for part in parts:
            if not part.isdigit():
                return (QtGui.QValidator.Invalid, pos)
            if len(part) not in (1, 2):
                return (QtGui.QValidator.Intermediate, pos)

        if int(parts[0]) not in range(0, 24):
            return (QtGui.QValidator.Invalid, pos)
        if int(parts[1]) not in range(0, 60):
            return (QtGui.QValidator.Invalid, pos)
        return (QtGui.QValidator.Acceptable, pos)


class DateTimeEditor(CustomEditor):
    """Widget for editing date and time separated and with popups"""

    def __init__(self, parent, editable=True, nullable=True, field_name='datetime', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        import itertools
        self.nullable = nullable
        layout = QtGui.QHBoxLayout()
        self.dateedit = DateEditor(self, editable=editable, nullable=nullable, **kwargs)
        self.dateedit.editingFinished.connect(self.editing_finished)
        layout.addWidget(self.dateedit, 1)
        self.timeedit = QtGui.QComboBox(self)
        self.timeedit.setEditable(True)
        if not editable:
            self.timeedit.setEnabled(False)
        time_entries = [ entry for entry in itertools.chain(*(('%02i:00' % i, '%02i:30' % i) for i in range(0, 24)))
                       ]
        self.timeedit.addItems(time_entries)
        self.timeedit.setValidator(TimeValidator(self, nullable))
        self.timeedit.activated.connect(self.editing_finished)
        self.timeedit.lineEdit().editingFinished.connect(self.editing_finished)
        self.timeedit.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.timeedit, 1)
        self.setFocusProxy(self.dateedit)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    @QtCore.pyqtSlot(QtCore.QString)
    @QtCore.pyqtSlot(int)
    @QtCore.pyqtSlot()
    def editing_finished(self, _arg=None):
        if self.time() and self.date():
            self.editingFinished.emit()

    def get_value(self):
        time_value = self.time()
        date_value = self.date()
        if time_value not in (None, ValueLoading) and date_value not in (None, ValueLoading):
            value = datetime.datetime(hour=time_value.hour(), minute=time_value.minute(), second=time_value.second(), year=date_value.year, month=date_value.month, day=date_value.day)
        else:
            value = None
        return CustomEditor.get_value(self) or value

    def set_value(self, value):
        value = CustomEditor.set_value(self, value)
        if value:
            self.dateedit.set_value(value.date())
            self.timeedit.lineEdit().setText('%02i:%02i' % (value.hour, value.minute))
        else:
            self.dateedit.set_value(None)
            self.timeedit.lineEdit().setText('--:--')
        return

    def date(self):
        return self.dateedit.get_value()

    def time(self):
        text = str(self.timeedit.currentText())
        if text == '--:--':
            return None
        else:
            parts = text.split(':')
            return QtCore.QTime(int(parts[0]), int(parts[1]))

    def set_enabled(self, editable=True):
        self.timeedit.setEnabled(editable)
        self.dateedit.setEnabled(editable)

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.dateedit.line_edit.setToolTip(unicode(tooltip or ''))

    def set_background_color(self, background_color):
        self.dateedit.set_background_color(background_color)
        set_background_color_palette(self.timeedit.lineEdit(), background_color)