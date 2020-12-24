# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\action_paste.py
# Compiled at: 2009-03-05 11:50:40
"""
Paste action -- insert a specific text by pasting it from the clipboard
============================================================================

"""
import win32con
from dragonfly.actions.action_base import DynStrActionBase, ActionError
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text
from dragonfly.windows.clipboard import Clipboard

class Paste(DynStrActionBase):
    """
        Paste-from-clipboard action.

        Constructor arguments:
         - *contents* (*str*) -- contents to paste
         - *format* (*int*, Win32 clipboard format) --
           clipboard format
         - *paste* (instance derived from *ActionBase*) --
           paste action
         - *static* (boolean) --
           flag indicating whether the
           specification contains dynamic elements

        This action inserts the given *contents* into the Windows system 
        clipboard, and then performs the *paste* action to paste it into 
        the foreground application.  By default, the *paste* action is the 
        :kbd:`Control-v` keystroke.  The default clipboard format to use 
        is the *Unicode* text format.

    """
    _default_format = win32con.CF_UNICODETEXT
    _default_paste = Key('c-v/5')

    def __init__(self, contents, format=None, paste=None, static=False):
        if not format:
            format = self._default_format
        if not paste:
            paste = self._default_paste
        if isinstance(contents, basestring):
            spec = contents
            self.contents = None
        else:
            spec = ''
            self.contents = contents
        self.format = format
        self.paste = paste
        DynStrActionBase.__init__(self, spec, static=static)
        return

    def _parse_spec(self, spec):
        if self.contents:
            return self.contents
        else:
            return spec

    def _execute_events(self, events):
        original = Clipboard()
        original.copy_from_system()
        if self.format == win32con.CF_UNICODETEXT:
            events = unicode(events)
        elif self.format == win32con.CF_TEXT:
            events = str(events)
        clipboard = Clipboard(contents={self.format: events})
        clipboard.copy_to_system()
        self.paste.execute()
        original.copy_to_system()
        return True