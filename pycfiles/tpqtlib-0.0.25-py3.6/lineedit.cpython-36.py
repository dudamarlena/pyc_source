# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/lineedit.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 3937 bytes
"""
Module that contains classes to create different kind of line edits
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *

class BaseLineEdit(QLineEdit, object):
    __doc__ = "\n    Basic line edit that takes a different color if it's empty\n    "

    def __init__(self, default='', off_color=(125, 125, 125), on_color=(255, 255, 255), parent=None):
        super(BaseLineEdit, self).__init__(parent=parent)
        self._value = ''
        self._default = ''
        self._off_color = off_color
        self._on_color = on_color
        self.set_default(default)
        self.textChanged.connect(self._on_change)

    def get_value(self):
        if self.text() == self._default:
            return ''
        else:
            return self._value

    def set_value(self, value):
        self._value = value

    value = property(get_value, set_value)

    def focusInEvent(self, event):
        if self.text() == self._default:
            self.setText('')
            self.setStyleSheet(self._get_on_style())

    def focusOutEvent(self, event):
        if self.text() == '':
            self.setText(self._default)
            self.setStyleSheet(self._get_off_style())

    def set_default(self, text):
        self.setText(text)
        self._default = text
        self.setStyleSheet(self._get_off_style())

    def _get_on_style(self):
        return 'QLineEdit{color:rgb(%s, %s, %s);}' % (self._on_color[0], self._on_color[1], self._on_color[2])

    def _get_off_style(self):
        return 'QLineEdit{color:rgb(%s, %s, %s);}' % (self._off_color[0], self._off_color[1], self._off_color[2])

    def _on_change(self, text):
        if text != self._default:
            self.setStyleSheet(self._get_on_style())
            self._value = text
        else:
            self.setStyleSheet(self._get_off_style())


class BaseAttrLineEdit(QLineEdit, object):
    attr_type = None
    valueChanged = Signal()

    def __init__(self, parent=None):
        super(BaseAttrLineEdit, self).__init__(parent=parent)
        self.returnPressed.connect(self.update)
        self.editingFinished.connect(self.update)

    def get_value(self):
        pass

    value = property(get_value)


class FloatLineEdit(BaseAttrLineEdit, object):
    attr_type = 'float'
    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super(FloatLineEdit, self).__init__(parent=parent)

    def get_value(self):
        if not self.text():
            return 0.0
        else:
            return float(self.text())

    value = property(get_value)

    def setText(self, text):
        super(FloatLineEdit, self).setText('%.2f' % float(text))

    def update(self):
        if self.text():
            self.setText(self.text())
        super(FloatLineEdit, self).update()
        self.valueChanged.emit(float(self.text()))


class IntLineEdit(QLineEdit, object):
    attr_type = 'int'
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(IntLineEdit, self).__init__(parent=parent)

    def get_value(self):
        if not self.text():
            return 0
        else:
            return int(self.text())

    value = property(get_value)

    def setText(self, text):
        super(IntLineEdit, self).setText('%s' % int(text))

    def update(self):
        if self.text():
            self.setText(self.text())
        super(IntLineEdit, self).update()
        self.valueChanged.emit(int(self.text()))