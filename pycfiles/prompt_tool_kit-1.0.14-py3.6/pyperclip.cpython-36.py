# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/clipboard/pyperclip.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1138 bytes
from __future__ import absolute_import, unicode_literals
import pyperclip
from prompt_tool_kit.selection import SelectionType
from .base import Clipboard, ClipboardData
__all__ = ('PyperclipClipboard', )

class PyperclipClipboard(Clipboard):
    __doc__ = '\n    Clipboard that synchronizes with the Windows/Mac/Linux system clipboard,\n    using the pyperclip module.\n    '

    def __init__(self):
        self._data = None

    def set_data(self, data):
        assert isinstance(data, ClipboardData)
        self._data = data
        pyperclip.copy(data.text)

    def get_data(self):
        text = pyperclip.paste()
        if self._data:
            if self._data.text == text:
                return self._data
        return ClipboardData(text=text,
          type=(SelectionType.LINES if '\n' in text else SelectionType.LINES))