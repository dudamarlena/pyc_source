# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/panels/read_only.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 2579 bytes
"""
Contains a panel to manage unicode decoding/encoding errors.

"""
from pyqode.core.api.panel import Panel
from pyqode.core.api.decoration import TextDecoration
from pyqode.qt import QtCore, QtGui, QtWidgets

class ReadOnlyPanel(Panel):
    __doc__ = ' Displays a message if the opened file is read-only '

    @property
    def color(self):
        """
        Returns the panel color.
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._refresh_stylesheet()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).color = value
                except KeyError:
                    pass

    @property
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, value):
        self._foreground = value
        self._refresh_stylesheet()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).foreground = value
                except KeyError:
                    pass

    def _refresh_stylesheet(self):
        try:
            self._lbl_stylesheet = 'color: %s;background: %s' % (
             self._foreground.name(),
             self._color.name())
            self.ui.lblDescription.setStyleSheet(self._lbl_stylesheet)
        except AttributeError:
            pass

    def __init__(self):
        super(ReadOnlyPanel, self).__init__(dynamic=True)
        from pyqode.core._forms.pnl_read_only_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._color = None
        self.color = QtGui.QColor('#8AADD4')
        self._foreground = None
        self.foreground = QtGui.QColor('#FFFFFF')
        self.hide()

    def paintEvent(self, event):
        """ Fills the panel background. """
        super(ReadOnlyPanel, self).paintEvent(event)
        if self.isVisible():
            painter = QtGui.QPainter(self)
            self._background_brush = QtGui.QBrush(self._color)
            painter.fillRect(event.rect(), self._background_brush)