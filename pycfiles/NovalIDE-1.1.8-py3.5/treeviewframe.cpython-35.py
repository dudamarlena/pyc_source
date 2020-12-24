# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/ttkwidgets/treeviewframe.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1448 bytes
import tkinter as tk
from tkinter import ttk

class TreeViewFrame(ttk.Frame):

    def __init__(self, master, columns=[], displaycolumns='#all', show_scrollbar=True, borderwidth=0, relief='flat', treeview_class=ttk.Treeview, show='tree', **tree_kw):
        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=None)
        if show_scrollbar:
            self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        if columns != []:
            tree_kw.update(dict(columns=columns, displaycolumns=displaycolumns))
        self.tree = treeview_class(self, yscrollcommand=self.vert_scrollbar.set, **tree_kw)
        self.tree['show'] = show
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.vert_scrollbar['command'] = self.tree.yview
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _clear_tree(self):
        for child_id in self.tree.get_children():
            self.tree.delete(child_id)

    def clear(self):
        self._clear_tree()

    def on_select(self, event):
        node_id = self.tree.focus()
        self.tree.selection_set(node_id)
        self.tree.focus(node_id)