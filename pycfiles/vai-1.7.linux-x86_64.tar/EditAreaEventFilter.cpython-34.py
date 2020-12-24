# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/EditAreaEventFilter.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1550 bytes
import vaitk
from vaitk import core, gui
from .models import EditorMode

class EditAreaEventFilter(core.VObject):
    __doc__ = '\n    Event filter to detect the use of commandbar initiation\n    keys, such as :, / and ?\n    '

    def __init__(self, command_bar, global_state, buffer_list):
        super().__init__()
        self._command_bar = command_bar
        self._global_state = global_state
        self._buffer_list = buffer_list

    def eventFilter(self, event):
        if not isinstance(event, gui.VKeyEvent):
            return False
        if self._global_state.editor_mode != EditorMode.COMMAND:
            return False
        if event.key() == vaitk.Key.Key_Colon:
            self._global_state.editor_mode = EditorMode.COMMAND_INPUT
            self._command_bar.setFocus()
            return True
        if event.key() == vaitk.Key.Key_Slash:
            self._global_state.editor_mode = EditorMode.SEARCH_FORWARD
            self._command_bar.setFocus()
            return True
        if event.key() == vaitk.Key.Key_Question:
            self._global_state.editor_mode = EditorMode.SEARCH_BACKWARD
            self._command_bar.setFocus()
            return True
        if event.key() == vaitk.Key.Key_N and event.modifiers() & vaitk.KeyModifier.ControlModifier:
            self._buffer_list.selectNext()
            return True
        if event.key() == vaitk.Key.Key_P and event.modifiers() & vaitk.KeyModifier.ControlModifier:
            self._buffer_list.selectPrev()
            return True
        return False