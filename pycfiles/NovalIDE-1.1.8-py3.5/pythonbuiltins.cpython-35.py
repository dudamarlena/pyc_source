# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/interpreter/pythonbuiltins.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 614 bytes
import tkinter as tk
from tkinter import ttk
import noval.ttkwidgets.listboxframe as listboxframe, noval.ui_utils as ui_utils

class PythonBuiltinsPanel(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.listview = listboxframe.ListboxFrame(self, listbox_class=ui_utils.ThemedListbox)
        self.listview.pack(fill='both', expand=1)

    def SetBuiltiins(self, interpreter):
        self.listview.listbox.delete(0, 'end')
        if interpreter is not None:
            for name in interpreter.Builtins:
                self.listview.listbox.insert(0, name)