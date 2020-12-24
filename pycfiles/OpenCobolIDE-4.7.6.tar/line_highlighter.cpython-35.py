# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/modes/line_highlighter.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 2626 bytes
"""
This module contains the care line highlighter mode
"""
from pyqode.qt import QtGui
from pyqode.core.api.decoration import TextDecoration
from pyqode.core.api.mode import Mode

class LineHighlighterMode(Mode):
    __doc__ = ' Highlights a line in the editor.'

    @property
    def background(self):
        """
        Background color of the highlighted line.
        """
        return self._color

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

    @property
    def line(self):
        if self._block:
            return self._block.blockNumber()
        else:
            return self._block

    @line.setter
    def line(self, value):
        if value is None:
            self._block = value
            self._clear_deco()
        else:
            self._block = self.editor.document().findBlockByNumber(value)
            self.refresh()

    def __init__(self):
        super(LineHighlighterMode, self).__init__()
        self._decoration = None
        self._block = None
        self._color = QtGui.QColor('#DD8080')

    def on_state_changed(self, state):
        if state:
            self.editor.new_text_set.connect(self.refresh)
            self.refresh()
        else:
            self.editor.new_text_set.disconnect(self.refresh)
            self._clear_deco()

    def on_install(self, editor):
        super(LineHighlighterMode, self).on_install(editor)
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
        if self.enabled and self.line:
            self._clear_deco()
            brush = QtGui.QBrush(self._color)
            self._decoration = TextDecoration(self.editor.textCursor(), start_line=self.line)
            self._decoration.set_background(brush)
            self._decoration.set_full_width()
            self._decoration.draw_order = 255
            self.editor.decorations.append(self._decoration)

    def clone_settings(self, original):
        self.background = original.background