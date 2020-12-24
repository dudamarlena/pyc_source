# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_main_tabs.py
# Compiled at: 2020-01-08 06:39:58
# Size of source mod 2**32: 3101 bytes
import tkinter as tk
from tkinter import ttk
from gui import gui_scrolltext
import tempstore

class main_tabs:

    def __init__(self, window):
        self.win = window
        self.main_tabs = ttk.Notebook(window.frm_left)
        self.main_tabs.bind('<<NotebookTabChanged>>', self.main_tab_pressed)
        self.stat_tab = tk.Frame(self.main_tabs)
        self.main_tabs.add((self.stat_tab), text='regression')
        self.stat_tab.rowconfigure(0, weight=1)
        self.stat_tab.columnconfigure(0, weight=1)
        self.main_tabs.grid(column=0, row=0, sticky=(tk.NSEW))
        self.text_boxes = text_boxes()
        self.add_tab = tk.Frame(self.main_tabs)
        self.main_tabs.add((self.add_tab), text='...')
        self.box = gui_scrolltext.ScrollText(self.stat_tab, 0, True)
        self.box.insert('1.0', 'This tab is dedicated to the regression table. Use other tabs for running scripts')
        self.add_editors()

    def add_editors(self):
        text_dict = tempstore.load_obj(tempstore.fname_editors)
        if text_dict is None:
            self.add_editor('script').focus()
            return
        for i in text_dict:
            self.add_editor(i, text_dict[i]).focus()

    def save_editors(self):
        text_dict = dict()
        for i in self.text_boxes.name_to_textbox:
            text_dict[i] = self.text_boxes.name_to_textbox[i].get_all()

        tempstore.save_obj(tempstore.fname_editors, text_dict)

    def main_tab_pressed(self, event):
        tab = self.current_editor()
        if tab.title() == '...':
            self.add_editor()
        else:
            if tab.title() == 'regression':
                self.win.buttons.run_disable()
            else:
                self.win.buttons.run_enable()

    def insert_current_editor(self, chars):
        tb = self.current_editor(True)
        tb.write(chars)
        tb.text_box.focus()

    def current_editor(self, return_obj=False):
        selection = self.main_tabs.select()
        tab = self.main_tabs.tab(selection, 'text')
        if not return_obj:
            return tab
        else:
            text = self.text_boxes.name_to_textbox[tab]
            return text

    def selected_tab_text(self):
        tb = self.current_editor(True)
        text = tb.get('1.0', tk.END)
        return text

    def add_editor(self, name=None, text=None):
        for i in range(1000):
            if name is not None:
                break
            else:
                name = f"script {i + 2}"
                if name not in self.text_boxes.name_to_textbox:
                    break

        tf = tk.Frame(self.main_tabs)
        tf.rowconfigure(0, weight=1)
        tf.columnconfigure(0, weight=1)
        self.main_tabs.add(tf, text=name)
        text_box = self.text_boxes.add(name, tf, text)
        self.main_tabs.select(tf)
        self.main_tabs.insert('end', self.add_tab)
        return text_box


class text_boxes:

    def __init__(self):
        self.name_to_textbox = dict()
        self.obj_to_textbox = dict()
        self.name_to_textbox = dict()
        self.obj_to_name = dict()
        self.name_to_obj = dict()

    def add(self, name, frame, text=None):
        txtbox = gui_scrolltext.ScrollText(frame, 0, text=text)
        self.name_to_textbox[name] = txtbox
        self.obj_to_textbox[frame] = txtbox
        self.obj_to_name[frame] = name
        self.name_to_obj[name] = frame
        return txtbox

    def remove(self, name=None, frame=None):
        pass