# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/modes/caret_line_highlight.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 2729 bytes
"""
This module contains the care line highlighter mode
"""
from pyqode.core.api.decoration import TextDecoration
from pyqode.core.api.mode import Mode
from pyqode.core.api.utils import drift_color
from pyqode.qt import QtGui

class CaretLineHighlighterMode(Mode):
    __doc__ = ' Highlights the caret line '

    @property
    def background(self):
        """
        Background color of the caret line. Default is to use a color slightly
        darker/lighter than the background color. You can override the
        automatic color by setting up this property
        """
        if self._color or not self.editor:
            return self._color
        else:
            return drift_color(self.editor.background, 110)

    @background.setter
    def background(self, value):
        self._color = value
        self.refresh()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).background = value
                except KeyError:
                    pass

    def __init__(self):
        super(CaretLineHighlighterMode, self).__init__()
        self._decoration = None
        self._pos = -1
        self._color = None

    def on_state_changed(self, state):
        if state:
            self.editor.cursorPositionChanged.connect(self.refresh)
            self.editor.new_text_set.connect(self.refresh)
            self.refresh()
        else:
            self.editor.cursorPositionChanged.disconnect(self.refresh)
            self.editor.new_text_set.disconnect(self.refresh)
            self._clear_deco()

    def on_install(self, editor):
        super(CaretLineHighlighterMode, self).on_install(editor)
        self.refresh()

    def _clear_deco(self):
        """ Clear line decoration """
        if self._decoration:
            self.editor.decorations.remove(self._decoration)
            self._decoration = None

    def refresh(self):
        """
        Updates the current line decoration
        """
        if self.enabled:
            self._clear_deco()
            if self._color:
                color = self._color
            else:
                color = drift_color(self.editor.background, 110)
            brush = QtGui.QBrush(color)
            self._decoration = TextDecoration(self.editor.textCursor())
            self._decoration.set_background(brush)
            self._decoration.set_full_width()
            self.editor.decorations.append(self._decoration)

    def clone_settings(self, original):
        self.background = original.background