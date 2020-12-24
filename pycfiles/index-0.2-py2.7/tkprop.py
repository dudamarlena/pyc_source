# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\lib\tkprop.py
# Compiled at: 2013-09-15 13:30:49
from __future__ import division, absolute_import, print_function, unicode_literals
from .dump import *

class base_cls(object):

    def __init__(self, _dict):
        self.title(b'Property')
        frame = ttk.Frame(self, padding=b'3')
        frame.pack(fill=tk.BOTH, expand=1)
        self.tree = ttk.Treeview(frame, columns=('Types', 'Values', 'iid'))
        self.tree.heading(b'#0', text=b'Key')
        self.tree.heading(b'Types', text=b'Type')
        self.tree.heading(b'Values', text=b'Value')
        self.tree.heading(b'iid', text=b'iid')
        self.tree.column(b'#0', minwidth=50, width=150, stretch=False)
        self.tree.column(b'Types', minwidth=50, width=100, stretch=False, anchor=b'center')
        self.tree.column(b'Values')
        self.tree.column(b'iid', minwidth=50, width=100, stretch=False, anchor=b'center')
        self.tree.pack(fill=tk.BOTH, expand=1)
        self.buildTree(_dict)
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def escape(self, value):
        if isinstance(value, string_types):
            value = value.replace(b'\\', b'\\\\')
        return value

    def buildTree(self, obj, name=b'root', parent=b''):
        item = self.tree.insert(parent, b'end')
        if obj is None:
            value = (
             plain_type(obj), b'None', item)
            self.tree.item(item, text=name, value=value, tags=('none', ))
            return
        else:
            if isinstance(obj, simple_types):
                value = (
                 plain_type(obj), self.escape(plain(obj)), item)
                self.tree.item(item, text=name, value=value)
                return
            value = (
             plain_type(obj), b'', item)
            self.tree.item(item, text=name, value=value, tags=('self.tree', ))
            if not parent:
                self.tree.tag_configure(b'none', background=b'Gray')
                self.tree.tag_configure(b'self.tree', background=b'Lightgrey')
                self.tree.item(item, open=1)
            if isinstance(obj, collections_types):
                i = 0
                for key in obj:
                    self.buildTree(key, i, item)
                    i += 1

                return
            if isinstance(obj, dict):
                for key in sorted(obj):
                    value = obj[key]
                    self.buildTree(value, key, item)

                return
            return


class rootDialog(tk.Tk, base_cls):

    def __init__(self, _dict):
        tk.Tk.__init__(self)
        base_cls.__init__(self, _dict)


class propertyDialog(tk.Toplevel, base_cls):

    def __init__(self, _dict):
        tk.Toplevel.__init__(self)
        base_cls.__init__(self, _dict)