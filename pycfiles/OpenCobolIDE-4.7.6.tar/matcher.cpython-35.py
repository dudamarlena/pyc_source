# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/modes/matcher.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 9836 bytes
"""
This module contains the symbol matcher mode
"""
from pyqode.core.api import get_block_symbol_data
from pyqode.core.api.decoration import TextDecoration
from pyqode.core.api.mode import Mode
from pyqode.qt import QtGui
PAREN = 0
SQUARE = 1
BRACE = 2
OPEN = 0
CLOSE = 1

class SymbolMatcherMode(Mode):
    __doc__ = ' Highlights matching symbols (parentheses, braces,...)\n\n    .. note:: This mode requires the document to be filled with\n        :class:`pyqode.core.api.TextBlockUserData`, i.e. a\n        :class:`pyqode.core.api.SyntaxHighlighter` must be installed on\n        the editor instance.\n\n    '
    SYMBOLS = {PAREN: ('(', ')'), 
     SQUARE: ('[', ']'), 
     BRACE: ('{', '}')}

    @property
    def match_background(self):
        """
        Background color of matching symbols.
        """
        return self._match_background

    @match_background.setter
    def match_background(self, value):
        self._match_background = value
        self._refresh_decorations()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).match_background = value
                except KeyError:
                    pass

    @property
    def match_foreground(self):
        """
        Foreground color of matching symbols.
        """
        return self._match_foreground

    @match_foreground.setter
    def match_foreground(self, value):
        self._match_foreground = value
        self._refresh_decorations()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).match_foreground = value
                except KeyError:
                    pass

    @property
    def unmatch_background(self):
        """
        Background color of non-matching symbols.
        """
        return self._unmatch_background

    @unmatch_background.setter
    def unmatch_background(self, value):
        self._unmatch_background = value
        self._refresh_decorations()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).unmatch_background = value
                except KeyError:
                    pass

    @property
    def unmatch_foreground(self):
        """
        Foreground color of matching symbols.
        """
        return self._unmatch_foreground

    @unmatch_foreground.setter
    def unmatch_foreground(self, value):
        self._unmatch_foreground = value
        self._refresh_decorations()
        if self.editor:
            for clone in self.editor.clones:
                try:
                    clone.modes.get(self.__class__).unmatch_foreground = value
                except KeyError:
                    pass

    def __init__(self):
        super(SymbolMatcherMode, self).__init__()
        self._decorations = []
        self._match_background = QtGui.QBrush(QtGui.QColor('#B4EEB4'))
        self._match_foreground = QtGui.QColor('red')
        self._unmatch_background = QtGui.QBrush(QtGui.QColor('transparent'))
        self._unmatch_foreground = QtGui.QColor('red')

    def _clear_decorations(self):
        for deco in self._decorations:
            self.editor.decorations.remove(deco)

        self._decorations[:] = []

    def symbol_pos(self, cursor, character_type=OPEN, symbol_type=PAREN):
        """
        Find the corresponding symbol position (line, column) of the specified
        symbol. If symbol type is PAREN and character_type is OPEN, the
        function will look for '('.

        :param cursor: QTextCursor
        :param character_type: character type to look for (open or close char)
        :param symbol_type: symbol type (index in the SYMBOLS map).
        """
        retval = (None, None)
        original_cursor = self.editor.textCursor()
        self.editor.setTextCursor(cursor)
        block = cursor.block()
        data = get_block_symbol_data(self.editor, block)
        self._match(symbol_type, data, block.position())
        for deco in self._decorations:
            if deco.character == self.SYMBOLS[symbol_type][character_type]:
                retval = (
                 deco.line, deco.column)
                break

        self.editor.setTextCursor(original_cursor)
        self._clear_decorations()
        return retval

    def _refresh_decorations(self):
        for deco in self._decorations:
            self.editor.decorations.remove(deco)
            if deco.match:
                deco.set_foreground(self._match_foreground)
                deco.set_background(self._match_background)
            else:
                deco.set_foreground(self._unmatch_foreground)
                deco.set_background(self._unmatch_background)
            self.editor.decorations.append(deco)

    def on_state_changed(self, state):
        if state:
            self.editor.cursorPositionChanged.connect(self.do_symbols_matching)
        else:
            self.editor.cursorPositionChanged.disconnect(self.do_symbols_matching)

    def _match(self, symbol, data, cursor_pos):
        symbols = data[symbol]
        for i, info in enumerate(symbols):
            pos = self.editor.textCursor().position() - self.editor.textCursor().block().position()
            if info.character == self.SYMBOLS[symbol][OPEN] and info.position == pos:
                self._create_decoration(cursor_pos + info.position, self._match_left(symbol, self.editor.textCursor().block(), i + 1, 0))
            elif info.character == self.SYMBOLS[symbol][CLOSE] and info.position == pos - 1:
                self._create_decoration(cursor_pos + info.position, self._match_right(symbol, self.editor.textCursor().block(), i - 1, 0))

    def _match_left(self, symbol, current_block, i, cpt):
        while current_block.isValid():
            data = get_block_symbol_data(self.editor, current_block)
            parentheses = data[symbol]
            for j in range(i, len(parentheses)):
                info = parentheses[j]
                if info.character == self.SYMBOLS[symbol][OPEN]:
                    cpt += 1
                    continue
                    if info.character == self.SYMBOLS[symbol][CLOSE] and cpt == 0:
                        self._create_decoration(current_block.position() + info.position)
                        return True
                    if info.character == self.SYMBOLS[symbol][CLOSE]:
                        cpt -= 1

            current_block = current_block.next()
            i = 0

        return False

    def _match_right(self, symbol, current_block, i, nb_right_paren):
        while current_block.isValid():
            data = get_block_symbol_data(self.editor, current_block)
            parentheses = data[symbol]
            for j in range(i, -1, -1):
                if j >= 0:
                    info = parentheses[j]
                if info.character == self.SYMBOLS[symbol][CLOSE]:
                    nb_right_paren += 1
                    continue
                    if info.character == self.SYMBOLS[symbol][OPEN]:
                        if nb_right_paren == 0:
                            self._create_decoration(current_block.position() + info.position)
                            return True
                        nb_right_paren -= 1

            current_block = current_block.previous()
            data = get_block_symbol_data(self.editor, current_block)
            parentheses = data[symbol]
            i = len(parentheses) - 1

        return False

    def do_symbols_matching(self):
        """
        Performs symbols matching.
        """
        self._clear_decorations()
        current_block = self.editor.textCursor().block()
        data = get_block_symbol_data(self.editor, current_block)
        pos = self.editor.textCursor().block().position()
        for symbol in [PAREN, SQUARE, BRACE]:
            self._match(symbol, data, pos)

    def _create_decoration(self, pos, match=True):
        cursor = self.editor.textCursor()
        cursor.setPosition(pos)
        cursor.movePosition(cursor.NextCharacter, cursor.KeepAnchor)
        deco = TextDecoration(cursor, draw_order=10)
        deco.line = cursor.blockNumber()
        deco.column = cursor.columnNumber()
        deco.character = cursor.selectedText()
        deco.match = match
        if match:
            deco.set_foreground(self._match_foreground)
            deco.set_background(self._match_background)
        else:
            deco.set_foreground(self._unmatch_foreground)
            deco.set_background(self._unmatch_background)
        self._decorations.append(deco)
        self.editor.decorations.append(deco)
        return cursor

    def clone_settings(self, original):
        self.match_background = original.match_background
        self.match_foreground = original.match_foreground
        self.unmatch_background = original.unmatch_background
        self.unmatch_foreground = original.unmatch_foreground