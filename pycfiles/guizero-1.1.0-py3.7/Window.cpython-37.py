# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\Window.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 1177 bytes
from tkinter import Toplevel
from .base import BaseWindow
from . import utilities as utils

class Window(BaseWindow):

    def __init__(self, master, title='guizero', width=500, height=500, layout='auto', bg=None, visible=True):
        description = '[Window] oject'
        self._modal = False
        tk = Toplevel(master.tk)
        super(Window, self).__init__(master, tk, description, title, width, height, layout, bg, visible)

    def _close_window(self):
        if self._on_close is None:
            self.hide()
        else:
            self._on_close()

    def hide(self):
        """Hide the window."""
        self.tk.withdraw()
        self._visible = False
        if self._modal:
            self.tk.grab_release()

    def show(self, wait=False):
        """Show the window."""
        self.tk.deiconify()
        self._visible = True
        self._modal = wait
        if self._modal:
            self.tk.grab_set()