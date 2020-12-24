# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/clipboard/pyperclip.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1138 bytes
from __future__ import absolute_import, unicode_literals
import pyperclip
from prompt_tool_kit.selection import SelectionType
from .base import Clipboard, ClipboardData
__all__ = ('PyperclipClipboard', )

class PyperclipClipboard(Clipboard):
    """PyperclipClipboard"""

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