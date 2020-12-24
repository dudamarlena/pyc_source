# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkpip\lib\listboxdata.py
# Compiled at: 2013-08-24 00:54:30
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, logging
from .backwardcompat import *

class ListBoxData(tk.Listbox):

    def __init__(self, master=None):
        self.v = tk.Variable(master)
        tk.Listbox.__init__(self, master, listvariable=self.v)
        ListBoxData.clear(self)

    def clear(self):
        self.v.set(())
        self._datas = []

    def __iter__(self):
        values = self.v.get()
        for i in range(len(values)):
            yield (
             i, self.value(i), self.data(i))

    def value(self, pos):
        try:
            pos = self.index(pos)
            values = self.v.get()
            return values[pos]
        except ValueError as e:
            print(pos, e)

    def data(self, pos):
        try:
            pos = self.index(pos)
            return self._datas[pos]
        except ValueError as e:
            print(pos, e)

    def setValue(self, pos, value):
        pos = self.index(pos)
        values = list(self.v.get())
        values[pos] = value
        self.v.set(tuple(values))

    def setData(self, pos, data):
        pos = self.index(pos)
        self._datas[pos] = data

    def get_selected(self):
        selection = self.curselection()
        if selection:
            selected = int(selection[0])
            try:
                value = self.value(selected)
                data = self.data(selected)
            except IndexError as e:
                logging.warning((b'Index Error: {0} [{1}]!').format(selected, e))
                value = None
                data = None

            return (selected, value, data)
        else:
            return (None, None, None)
            return

    def insert(self, pos, label, **kw):
        self.insert_data(pos, label, None, **kw)
        return

    def insert_data(self, pos, label, data, **kw):
        pos = self.index(pos)
        tk.Listbox.insert(self, pos, label, **kw)
        self._datas.insert(pos + 1, data)
        if data:
            itemconfig = data.get(b'_item')
            if itemconfig:
                self.itemconfig(pos, **itemconfig)

    def insert_items(self, items):
        if isinstance(items, list):
            for key in sorted(items):
                self.insert(tk.END, key)

        elif isinstance(items, dict):
            for key in sorted(items.keys()):
                self.insert_data(tk.END, key, items[key])


def test():
    root = Tk()
    listbox1 = ListBoxData(root)
    lb1_yscrollbar = Scrollbar(root, orient=tk.VERTICAL, command=listbox1.yview)
    listbox1[b'yscrollcommand'] = lb1_yscrollbar.set
    listbox1.pack(side=b'left', fill=b'both', expand=1)
    lb1_yscrollbar.pack(side=b'right', fill=b'both')
    root.mainloop()


if __name__ == b'__main__':
    test()