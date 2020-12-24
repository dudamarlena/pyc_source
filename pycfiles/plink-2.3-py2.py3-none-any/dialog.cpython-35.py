# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /build/plink/build/lib/plink/dialog.py
# Compiled at: 2019-07-15 20:56:41
# Size of source mod 2**32: 2210 bytes
"""
This module exports the InfoDialog class, used for displaying information
about the PLink program.
"""
from .gui import *
if tkSimpleDialog:
    baseclass = tkSimpleDialog.Dialog
else:
    baseclass = object

class InfoDialog(baseclass):

    def __init__(self, parent, title, content=''):
        self.parent = parent
        self.content = content
        Tk_.Toplevel.__init__(self, parent)
        NW = Tk_.N + Tk_.W
        if title:
            self.title(title)
        canvas = Tk_.Canvas(self, width=58, height=58)
        canvas.grid(row=0, column=0, sticky=NW)
        text = Tk_.Text(self, font='Helvetica 14', width=50, height=16, padx=10)
        text.insert(Tk_.END, self.content)
        text.grid(row=0, column=1, sticky=NW, padx=10, pady=10)
        text.config(state=Tk_.DISABLED)
        self.buttonbox()
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.ok)
        self.focus_set()
        self.wait_window(self)

    def buttonbox(self):
        box = ttk.Frame(self)
        w = ttk.Button(box, text='OK', width=10, command=self.ok, default=Tk_.ACTIVE)
        w.pack(side=Tk_.LEFT, padx=5, pady=5)
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        box.grid(row=1, columnspan=2)

    def ok(self, event=None):
        self.parent.focus_set()
        self.app = None
        self.destroy()