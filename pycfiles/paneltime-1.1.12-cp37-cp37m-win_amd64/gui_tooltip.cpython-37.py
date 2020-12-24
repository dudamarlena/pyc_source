# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_tooltip.py
# Compiled at: 2020-02-11 05:43:58
# Size of source mod 2**32: 1218 bytes
import tkinter as tk

class CreateToolTip(object):
    __doc__ = '\n\tcreate a tooltip for a given widget\n\t'

    def __init__(self, widget, text='widget info'):
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)
        self.widget.bind('<ButtonPress>', self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.showtip(event)

    def leave(self, event=None):
        self.hidetip()

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry('+%d+%d' % (x, y))
        label = tk.Label((self.tw), text=(self.text), justify='left', background='#ffffff',
          relief='solid',
          borderwidth=1,
          wraplength=(self.wraplength))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()