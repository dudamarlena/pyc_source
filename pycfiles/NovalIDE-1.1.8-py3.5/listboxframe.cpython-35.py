# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/ttkwidgets/listboxframe.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 985 bytes
import tkinter as tk
from tkinter import ttk

class ListboxFrame(ttk.Frame):

    def __init__(self, master, show_scrollbar=True, borderwidth=0, relief='flat', listbox_class=tk.Listbox, **kw):
        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=None)
        if show_scrollbar:
            self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        self.listbox = listbox_class(self, yscrollcommand=self.vert_scrollbar.set, selectborderwidth=0, borderwidth=0, **kw)
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW)
        self.vert_scrollbar['command'] = self.listbox.yview
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)