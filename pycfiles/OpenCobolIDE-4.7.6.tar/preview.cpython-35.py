# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/widgets/preview.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 1934 bytes
"""
This module contains a widget that can show the html preview of an
editor.
"""
from weakref import proxy
from pyqode.qt import QtCore, QtWidgets
from pyqode.core.api import DelayJobRunner

class HtmlPreviewWidget(QtWidgets.QTextEdit):
    __doc__ = '\n    Display html preview of a document as rich text in a QTextEdit.\n    '
    hide_requested = QtCore.Signal()
    show_requested = QtCore.Signal()

    def __init__(self, parent=None):
        super(HtmlPreviewWidget, self).__init__(parent)
        self._editor = None
        self._timer = DelayJobRunner(delay=1000)

    def set_editor(self, editor):
        try:
            self.setHtml(editor.to_html())
        except (TypeError, AttributeError):
            self.setHtml('<center>No preview available...</center>')
            self._editor = None
            self.hide_requested.emit()
        else:
            if self._editor is not None and editor != self._editor:
                try:
                    self._editor.textChanged.disconnect(self._on_text_changed)
                except TypeError:
                    pass

                editor.textChanged.connect(self._on_text_changed)
                self._editor = proxy(editor)
                self.show_requested.emit()

    def _on_text_changed(self, *_):
        self._timer.request_job(self._update_preview)

    def _update_preview(self):
        try:
            p = self.textCursor().position()
            v = self.verticalScrollBar().value()
            self.setHtml(self._editor.to_html())
            c = self.textCursor()
            c.setPosition(p)
            self.setTextCursor(c)
            self.verticalScrollBar().setValue(v)
        except (TypeError, AttributeError):
            self.setHtml('<center>No preview available...</center>')
            self.hide_requested.emit()