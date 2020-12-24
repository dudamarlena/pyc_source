# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/filedialog.py
# Compiled at: 2017-05-26 08:27:22
import sys
if sys.version_info[0] < 3:
    import tkFileDialog
else:
    import tkinter.filedialog as tkFileDialog
askopenfile = tkFileDialog.askopenfile

def asksaveasfile(mode='w', **options):
    """
    Ask for a filename to save as, and returned the opened file.
    Modified from tkFileDialog to more intelligently handle
    default file extensions. 
    """
    if sys.platform == 'darwin':
        if 'defaultextension' in options and 'initialfile' not in options:
            options['initialfile'] = 'untitled' + options['defaultextension']
    return tkFileDialog.asksaveasfile(mode=mode, **options)


if __name__ == '__main__':
    asksaveasfile(defaultextension='.txt')