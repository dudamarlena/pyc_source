# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /build/plink/build/lib/plink/gui.py
# Compiled at: 2019-07-15 20:56:41
from __future__ import unicode_literals
import sys
try:
    if sys.version_info[0] < 3:
        import tkinter as Tk_, tkFileDialog, tkMessageBox, tkSimpleDialog, tkinter.ttk as ttk
    else:
        import tkinter as Tk_, tkinter.filedialog as tkFileDialog, tkinter.messagebox as tkMessageBox, tkinter.simpledialog as tkSimpleDialog, tkinter.ttk as ttk
    from . import canvasvg
except ImportError:
    Tk_, tkFileDialog, tkMessageBox, tkSimpleDialog, canvasvg = (None, None, None,
                                                                 None, None)

try:
    from urllib import pathname2url
except:
    from urllib.request import pathname2url

try:
    import pyx
    have_pyx = True
except ImportError:
    have_pyx = False

if sys.platform == b'linux2' or sys.platform == b'linux':
    closed_hand_cursor = b'fleur'
    open_hand_cursor = b'hand1'
elif sys.platform == b'darwin':
    closed_hand_cursor = b'closedhand'
    open_hand_cursor = b'openhand'
else:
    closed_hand_cursor = b'hand2'
    open_hand_cursor = b'hand1'

def asksaveasfile(mode=b'w', **options):
    """
    Ask for a filename to save as, and returned the opened file.
    Modified from tkFileDialog to more intelligently handle
    default file extensions. 
    """
    if sys.platform == b'darwin':
        if b'defaultextension' in options and b'initialfile' not in options:
            options[b'initialfile'] = b'untitled' + options[b'defaultextension']
    return tkFileDialog.asksaveasfile(mode=mode, **options)


if sys.platform == b'linux2':

    def askopenfile(parent=None):
        return tkFileDialog.askopenfile(parent=parent, mode=b'r', title=b'Open SnapPea Projection File')


else:

    def askopenfile(parent=None):
        return tkFileDialog.askopenfile(parent=parent, mode=b'r', title=b'Open SnapPea Projection File', defaultextension=b'.lnk', filetypes=[
         ('Link and text files', '*.lnk *.txt', 'TEXT'),
         ('All text files', '', 'TEXT'),
         ('All files', '')])


scut = {b'Left': b'←', 
   b'Up': b'↑', 
   b'Right': b'→', 
   b'Down': b'↓'}
canvas_shifts = {b'Down': (0, 5), 
   b'Up': (0, -5), 
   b'Right': (5, 0), 
   b'Left': (-5, 0)}
vertex_shifts = {b'Down': (0, 1), 
   b'Up': (0, -1), 
   b'Right': (1, 0), 
   b'Left': (-1, 0)}