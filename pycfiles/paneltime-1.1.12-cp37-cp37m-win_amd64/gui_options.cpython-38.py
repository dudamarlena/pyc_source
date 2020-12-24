# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \\ad.uit.no\uit\data\esi000data\dokumenter\forskning\papers\paneltime\paneltime\paneltime\gui\gui_options.py
# Compiled at: 2020-01-28 04:15:45
# Size of source mod 2**32: 8262 bytes
import tkinter as tk
from tkinter import ttk
from gui import gui_charts
import time
from gui import gui_scrolltext
import options as default_options
from gui import gui_scrolltext
NON_NUMERIC_TAG = '|~|'
font = 'Arial 9 '
tags = dict()
tags['option'] = {'fg':'#025714',  'bg':'#e6eaf0',  'font':font + 'bold'}
tags['unselected'] = {'fg':'black',  'bg':'white',  'font':font}

class options(ttk.Treeview):

    def __init__(self, tabs, window):
        s = ttk.Style()
        s.configure('new.TFrame', background='white', font=font)
        self.tabs = tabs
        self.win = window
        self.options = window.globals['options']
        self.default_options = default_options.options()
        self.main_frame = tk.Frame(tabs)
        self.canvas = tk.Canvas(self.main_frame)
        self.opt_frame = tk.Frame(self.main_frame)
        ttk.Treeview.__init__(self, (self.canvas), style='new.TFrame')
        self.level__dicts = [dict(), dict(), dict()]
        yscrollbar = ttk.Scrollbar((self.canvas), orient='vertical', command=(self.yview))
        self.configure(yscrollcommand=(yscrollbar.set))
        xscrollbar = ttk.Scrollbar((self.canvas), orient='horizontal', command=(self.xview))
        self.configure(xscrollcommand=(xscrollbar.set))
        self.gridding(xscrollbar, yscrollbar)
        self.tree_construction()
        self.binding()
        self.tabs.add((self.main_frame), text='options')
        self.tabs.grid(row=0, column=0, sticky=(tk.NSEW))
        self.script = ''

    def get_script(self):
        opt = self.options.__dict__
        def_opt = self.default_options.__dict__
        s = ''
        for i in opt:
            if hasattr(opt[i], 'value') and opt[i].value != def_opt[i].value:
                s += f"pt.options.{i}.set({opt[i].value})\n"
        else:
            self.script = s

    def binding(self):
        self.bind('<Double-Button-1>', self.tree_double_click)
        self.bind('<<TreeviewSelect>>', self.tree_click)
        self.bind('<Key>', self.key_down)
        self.bind('<KeyRelease>', self.key_up)

    def tree_construction(self):
        self['columns'] = ('one', 'two')
        self.column('#0', stretch=(tk.YES))
        self.column('one', width=50, stretch=(tk.YES))
        self.column('two', width=50, stretch=(tk.YES))
        self.heading('#0', text='Option', anchor=(tk.W))
        self.heading('one', text='value', anchor=(tk.W))
        self.heading('two', text='type', anchor=(tk.W))
        self.alt_time = time.perf_counter()
        for k in tags:
            tag_configure(self, k, tags[k])
        else:
            self.tree = dict()
            self.add_options_to_tree()

    def gridding(self, xscrollbar, yscrollbar):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tabs.rowconfigure(0, weight=1)
        self.tabs.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=7, uniform='fred')
        self.main_frame.rowconfigure(1, weight=5, uniform='fred')
        self.main_frame.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.opt_frame.rowconfigure(0, weight=1)
        self.opt_frame.columnconfigure(0, weight=1)
        self.main_frame.grid(row=0, column=0, sticky=(tk.NSEW))
        self.canvas.grid(row=0, column=0, sticky=(tk.NSEW))
        self.opt_frame.grid(row=1, column=0, sticky='nw')
        xscrollbar.grid(row=1, column=0, sticky='ew')
        yscrollbar.grid(row=0, column=1, sticky='ns')
        self.grid(row=0, column=0, sticky=(tk.NSEW))

    def key_down(self, event):
        if event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
            self.configure(cursor='target')
            self.alt_time = time.perf_counter()

    def key_up(self, event):
        if event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
            self.configure(cursor='arrow')

    def tree_double_click(self, event):
        item = self.selection()[0]
        item = self.item(item)['text']
        self.win.main_tabs.insert_current_editor(item)

    def tree_click(self, event):
        item = self.selection()
        if len(item) == 0:
            return
        else:
            item = item[0]
            levels = item.split(';')
            if levels[1] == '':
                return
                if len(levels) == 3:
                    parent_itm = ';'.join(levels[:-1])
                    fname, j, k = levels
                    value, vtype = self.item(parent_itm)['values']
                    self.item(parent_itm, values=(k, vtype))
                    self.item(parent_itm, open=False)
            elif len(levels) == 2:
                i, j = levels
                if self.item(item)['open']:
                    self.item(item, open=False)
                else:
                    self.item(item, open=True)
                self.hide_all_frames()
                self.tree[i][j].grid(row=1, column=0)
        self.get_script()
        self.win.insert_script()

    def close_all(self):
        for i in self.tree:
            for j in self.tree[i]:
                self.item(j, open=False)

    def add_options_to_tree(self):
        for i in self.options.categories_srtd:
            self.insert('', 1, f"{i};", text=i)
            self.add_node(i, self.options.categories[i])
            self.item(f"{i};", open=True)

    def hide_all_frames(self):
        for i in self.tree:
            for j in self.tree[i]:
                self.tree[i][j].grid_remove()

    def add_node(self, cat, options):
        d = dict()
        self.tree[cat] = d
        for j in options:
            if type(j.dtype) == str:
                dtype = j.dtype
            else:
                dtype = j.dtype.__name__
            self.insert(f"{cat};", 2, f"{cat};{j.name}", text=(j.name), values=(j.value, dtype))
            d[j.name] = option_frame(self.opt_frame, j, self, f"{cat};{j.name}")
            self.add_options(j, cat)

    def add_options(self, option, cat):
        if not option.selection_var:
            return
        for i in range(len(option.value_description)):
            desc = option.value_description[i]
            val = option.permissible_values[i]
            self.insert(f"{cat};{option.name}", 3, f"{cat};{option.name};{i}", values=(val,), text=desc, tags=('option', ))


def tag_configure(tree, name, d, value=None):
    tree.tag_configure(name, foreground=(d['fg']))
    tree.tag_configure(name, background=(d['bg']))
    tree.tag_configure(name, font=(d['font']))
    if value is not None:
        tree.item(name, value=value)


class option_frame(tk.Frame):

    def __init__(self, master, option, option_tree, node_name):
        tk.Frame.__init__(self, master)
        self.option_tree = option_tree
        self.node_name = node_name
        self.option = option
        desc = option.descr_for_vector_setting
        if not type(option.description) == list:
            desc += option.description
        else:
            self.desc = tk.Label(self, text=desc, anchor='nw', justify=(tk.LEFT))
            self.desc.grid(row=0, column=0, sticky=(tk.NSEW))
            if option.is_inputlist:
                self.cntrl = tk.Frame(self)
                for i in range(len(option.description)):
                    self.add_control_multi(option, self.cntrl, i)
                else:
                    self.cntrl.grid(row=1, column=0, sticky=(tk.NSEW))

            else:
                if not option.selection_var:
                    self.add_control_single(option)
                    self.cntrl.grid(row=1, column=0, sticky=(tk.NSEW))

    def add_control_single(self, option):
        if option.dtype == str:
            self.cntrl = gui_scrolltext.ScrollText(self)
            if option.value is not None:
                self.cntrl.insert('1.0', option.value)
        else:
            self.cntrl = managed_text(self, option.dtype, option, self.option_tree, self.node_name)
            self.cntrl.text.set(option.value)

    def add_control_multi(self, option, master, i):
        line = tk.Frame(self.cntrl)
        line.columnconfigure(0, weight=1)
        line.columnconfigure(1, weight=1)
        self.items = dict()
        desc = option.description[i]
        lbl = tk.Label(line, text=desc, anchor='ne')
        self.items[desc] = managed_text(line, option.dtype, option, self.option_tree, self.node_name, i)
        self.items[desc].text.set(str(option.value[i]))
        self.items[desc].grid(row=0, column=2)
        lbl.grid(row=0, column=0)
        line.grid(row=i)


class managed_text(tk.Entry):

    def __init__(self, master, dtype, option, option_tree, node_name, i=None):
        self.text = tk.StringVar()
        vcmd = (master.register(self.onValidate), '%P')
        tk.Entry.__init__(self, master, textvariable=(self.text), validate='key', validatecommand=vcmd)
        self.option_tree = option_tree
        self.node_name = node_name
        self.dtype = dtype
        self.bind('<Key>', self.key_down)
        self.bind('<FocusOut>', self.lost_focus)
        self.option = option
        self.i = i
        self.master = master

    def key_down(self, event):
        if event.char == '\r':
            self.set_value()

    def lost_focus(self, event):
        self.set_value()

    def onValidate(self, P):
        if P == 'None':
            P = None
        else:
            if self.option.dtype == int:
                P = int(P)
            else:
                if self.option.dtype == float:
                    P = float(P)
        ok = self.option.set(P, self.i)
        self.option_tree.item((self.node_name), values=(self.option.value))
        self.option_tree.focus()
        return ok