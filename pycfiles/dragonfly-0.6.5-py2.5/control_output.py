# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\control_output.py
# Compiled at: 2009-01-19 04:06:55
"""
This file implements an edit control which can be used as a Python stream
for text-based output.  It can for example be assigned to standard
output and standard error to display Python print statements and
exception trace back.

"""
import sys, win32con
from dragonfly.windows.control_base import ControlBase

class OutputText(ControlBase):

    def __init__(self, parent, size, **kwargs):
        flavor = 'EDIT'
        text = ''
        style = win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.ES_LEFT | win32con.ES_MULTILINE | win32con.ES_AUTOVSCROLL | win32con.WS_TABSTOP | win32con.WS_BORDER | win32con.ES_READONLY | win32con.WS_VSCROLL
        ControlBase.__init__(self, parent, flavor, text, size, style, **kwargs)

    def set_as_output(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, data):
        length = win32gui.GetWindowTextLength(self.handle)
        win32gui.SendMessage(self.handle, win32con.EM_SETSEL, length, length)
        win32gui.SendMessage(self.handle, win32con.EM_REPLACESEL, False, data)

    def flush(self):
        pass