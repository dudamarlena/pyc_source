# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/GlobalState.py
# Compiled at: 2014-12-13 19:09:11
# Size of source mod 2**32: 1057 bytes
from vaitk import core
from .EditorMode import EditorMode

class GlobalState(core.VObject):
    __doc__ = '\n    Represents global state of the editor that is not dependent on\n    the currently selected buffer.\n    '

    def __init__(self):
        super().__init__()
        self._editor_mode = EditorMode.COMMAND
        self._current_search = None
        self._clipboard = None
        self.editorModeChanged = core.VSignal(self)

    @property
    def editor_mode(self):
        return self._editor_mode

    @editor_mode.setter
    def editor_mode(self, mode):
        if self._editor_mode != mode:
            self._editor_mode = mode
            self.editorModeChanged.emit(mode)

    @property
    def current_search(self):
        return self._current_search

    @current_search.setter
    def current_search(self, search):
        assert len(search) == 2
        self._current_search = search

    @property
    def clipboard(self):
        return self._clipboard

    @clipboard.setter
    def clipboard(self, text):
        self._clipboard = text