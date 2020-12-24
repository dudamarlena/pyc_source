# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/Notebook.py
# Compiled at: 2012-04-13 00:17:33
__doc__ = '\nCreated on Mar 12, 2012\n\n@author: bkraus\n'
import Tkinter
from Tkinter import IntVar
from Tkinter import Frame
from Tkinter import Radiobutton

class Notebook:

    def __init__(self, master, width=0, height=0):
        self.active_fr = None
        self.count = 0
        self.choice = IntVar(0)
        self.rb_fr = Frame(master, borderwidth=2, relief=Tkinter.RIDGE)
        self.rb_fr.grid(row=0, column=0, columnspan=10, sticky='NWE')
        self.screen_fr = Frame(master, borderwidth=2, relief=Tkinter.RIDGE, width=width, height=height)
        self.screen_fr.grid(row=1, column=0, columnspan=1, rowspan=1, sticky='WESN')
        self.screen_fr.rowconfigure(0, weight=1)
        self.screen_fr.columnconfigure(0, weight=1)
        return

    def __call__(self):
        """
        Returns the main content panel to which all tabs will be added to
        so they can reference it on construction.
        
        Returns:
            The main content panel.
        """
        return self.screen_fr

    def add_screen(self, fr, title):
        b = Radiobutton(self.rb_fr, text=title, indicatoron=0, variable=self.choice, value=self.count, padx=10, command=lambda : self.display(fr))
        b.grid(row=0, column=self.count)
        if not self.active_fr:
            self.display(fr)
        self.count += 1
        return b

    def display(self, fr):
        if self.active_fr:
            self.active_fr.grid_forget()
        fr.grid(row=0, column=0, sticky='NESW')
        self.active_fr = fr