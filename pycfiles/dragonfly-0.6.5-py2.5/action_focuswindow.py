# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\action_focuswindow.py
# Compiled at: 2009-03-11 12:10:21
"""
FocusWindow action -- bring a window to the foreground
============================================================================

"""
import win32con
from .action_base import ActionBase, ActionError
from ..windows.window import Window

class FocusWindow(ActionBase):
    """
        Bring a window to the foreground action.

        Constructor arguments:
         - *executable* (*str*) -- part of the filename of the
           application's executable to which the target window belongs;
           not case sensitive.
         - *title* (*str*) -- part of the title of the target window;
           not case sensitive.

        This action searches all visible windows for a window which 
        matches the given parameters.

    """

    def __init__(self, executable=None, title=None):
        if executable:
            self.executable = executable.lower()
        else:
            self.executable = None
        if title:
            self.title = title.lower()
        else:
            self.title = None
        ActionBase.__init__(self)
        arguments = []
        if executable:
            arguments.append('executable=%r' % executable)
        if title:
            arguments.append('title=%r' % title)
        self._str = (', ').join(arguments)
        return

    def _execute(self, data=None):
        executable = self.executable
        title = self.title
        if data and isinstance(data, dict):
            if executable:
                executable = (executable % data).lower()
            if title:
                title = (title % data).lower()
        windows = Window.get_all_windows()
        for window in windows:
            if not window.is_visible:
                continue
            if window.executable.endswith('natspeak.exe') and window.classname == '#32770' and window.get_position().dy < 50:
                continue
            if executable:
                if window.executable.lower().find(executable) == -1:
                    continue
            if title:
                if window.title.lower().find(title) == -1:
                    continue
            window.set_foreground()
            return

        raise ActionError('Failed to find window (%s).' % self._str)