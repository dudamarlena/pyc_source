# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_right_tabs.py
# Compiled at: 2020-02-25 05:51:55
# Size of source mod 2**32: 1387 bytes
import tkinter as tk
from tkinter import ttk
from gui import gui_charts
from gui import gui_data_objects
from gui import gui_options

class right_tab_widget:

    def __init__(self, window, main_tabs):
        self.win = window
        frm = tk.Frame(window.frm_right)
        self.sel_data = tk.StringVar(frm)
        lbl_desc = tk.Label(frm, text='Selected dataset:', background='white', font='Arial 9')
        lbl = tk.Label(frm, textvariable=(self.sel_data), background='white', font='Arial 9 bold')
        self.tabs = ttk.Notebook(window.frm_right)
        self.optionset = gui_options.optionset(self.tabs, window)
        self.data_tree = gui_data_objects.data_objects(self.tabs, window, self)
        self.preferences, pref_frame = gui_options.add_preferences_tab(self.tabs, window)
        self.tabs.add((self.data_tree.main_frame), text='datasets')
        self.tabs.add((self.optionset.main_frame), text='options')
        self.tabs.add(pref_frame, text='preferences')
        lbl_desc.grid(row=0, column=0)
        lbl.grid(row=0, column=1)
        frm.grid(row=0, column=0, sticky=(tk.NW))
        self.tabs.grid(row=1, column=0, sticky=(tk.NSEW))
        self.sql_script = ''

    def main_tabs_pressed(self, event):
        pass