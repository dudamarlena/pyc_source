# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/theme.py
# Compiled at: 2019-07-15 23:56:54
from __future__ import unicode_literals
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk_
    from tkinter import ttk
    from tkFont import Font
else:
    import tkinter as Tk_
    from tkinter import ttk
    from tkinter.font import Font

class SnapPyStyle:

    def __init__(self):
        self.ttk_style = ttk_style = ttk.Style()
        if sys.platform == b'darwin':
            try:
                test = Tk_._default_root.winfo_rgb(b'systemWindowBackgroundColor')
                self.windowBG = b'systemWindowBackgroundColor'
                self.groupBG = b'systemWindowBackgroundColor1'
                self.subgroupBG = b'systemWindowBackgroundColor2'
            except:
                self.windowBG = b'#ececec'
                self.groupBG = b'#e3e3e3'
                self.subgroupBG = b'#dbdbdb'

        else:
            self.windowBG = ttk_style.lookup(b'TLabelframe', b'background')
            self.groupBG = self.subgroupBG = self.windowBG
        self.font_info = fi = Font(font=ttk_style.lookup(b'TLabel', b'font')).actual()
        fi[b'size'] = abs(fi[b'size'])