# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /build/plink/build/lib/plink/gui.py
# Compiled at: 2019-07-15 20:56:41
# Size of source mod 2**32: 3391 bytes
from __future__ import unicode_literals
import sys
try:
    if sys.version_info[0] < 3:
        import tkinter as Tk_, tkFileDialog, tkMessageBox, tkSimpleDialog
        import tkinter.ttk as ttk
    else:
        import tkinter as Tk_
        import tkinter.filedialog as tkFileDialog
        import tkinter.messagebox as tkMessageBox
        import tkinter.simpledialog as tkSimpleDialog
        import tkinter.ttk as ttk
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

if sys.platform == 'linux2' or sys.platform == 'linux':
    closed_hand_cursor = 'fleur'
    open_hand_cursor = 'hand1'
else:
    if sys.platform == 'darwin':
        closed_hand_cursor = 'closedhand'
        open_hand_cursor = 'openhand'
    else:
        closed_hand_cursor = 'hand2'
        open_hand_cursor = 'hand1'

def asksaveasfile(mode='w', **options):
    """
    Ask for a filename to save as, and returned the opened file.
    Modified from tkFileDialog to more intelligently handle
    default file extensions. 
    """
    if sys.platform == 'darwin':
        if 'defaultextension' in options:
            if 'initialfile' not in options:
                options['initialfile'] = 'untitled' + options['defaultextension']
    return (tkFileDialog.asksaveasfile)(mode=mode, **options)


if sys.platform == 'linux2':

    def askopenfile(parent=None):
        return tkFileDialog.askopenfile(parent=parent,
          mode='r',
          title='Open SnapPea Projection File')


else:

    def askopenfile(parent=None):
        return tkFileDialog.askopenfile(parent=parent,
          mode='r',
          title='Open SnapPea Projection File',
          defaultextension='.lnk',
          filetypes=[
         ('Link and text files', '*.lnk *.txt', 'TEXT'),
         ('All text files', '', 'TEXT'),
         ('All files', '')])


scut = {'Left':'←', 
 'Up':'↑', 
 'Right':'→', 
 'Down':'↓'}
canvas_shifts = {'Down':(0, 5), 
 'Up':(0, -5), 
 'Right':(5, 0), 
 'Left':(-5, 0)}
vertex_shifts = {'Down':(0, 1), 
 'Up':(0, -1), 
 'Right':(1, 0), 
 'Left':(-1, 0)}