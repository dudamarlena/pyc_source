# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_right_tabs.py
# Compiled at: 2020-01-08 06:54:37
# Size of source mod 2**32: 799 bytes
import tkinter as tk
from tkinter import ttk
from gui import gui_charts
from gui import gui_data_objects
from gui import gui_options

class right_tab_widget:

    def __init__(self, window):
        self.win = window
        s = ttk.Style()
        s.configure('new.TFrame', background='white')
        self.tabs = ttk.Notebook(window.frm_right)
        self.add_chart_tab()
        self.data_tree = gui_data_objects.data_objects(self.tabs, window)
        self.options = gui_options.options(self.tabs, window)

    def add_chart_tab(self):
        self.chart_tab = ttk.Frame((self.tabs), style='new.TFrame')
        self.process_charts = gui_charts.process_charts(self.win, self.chart_tab)
        self.tabs.add((self.chart_tab), text='charts')