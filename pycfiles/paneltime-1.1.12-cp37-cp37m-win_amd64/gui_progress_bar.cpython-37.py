# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_progress_bar.py
# Compiled at: 2020-02-25 05:51:55
# Size of source mod 2**32: 670 bytes
import tkinter as tk

class bar(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, background='white', height=25)
        self.text = tk.StringVar(self)
        self.text_lbl = tk.Label(self, textvariable=(self.text), background='white', height=20)
        self.progress = tk.Frame(self, background='#9cff9d', height=5, width=0)
        self.text_lbl.grid(row=0, column=0, sticky=(tk.W))
        self.progress.grid(row=1, column=0, sticky=(tk.W))

    def set_progress(self, percent, text):
        total_width = self.winfo_width()
        self.progress.config(width=(int(total_width * percent)))
        self.progress.grid()
        self.text.set(text)
        print(percent)