# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\pycker\gui\ttk_spinbox.py
# Compiled at: 2017-05-30 16:06:54
# Size of source mod 2**32: 608 bytes
__doc__ = '\nAdd Spinbox widget to ttk (better looking themes).\n\nAuthor: Keurfon Luu <keurfon.luu@mines-paristech.fr>\nLicense: MIT\n'
import sys
if sys.version_info[0] < 3:
    import ttk
else:
    import tkinter.ttk as ttk
__all__ = [
 'Spinbox']

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kwargs):
        ttk.Entry.__init__(self, master, 'ttk::spinbox', **kwargs)

    def current(self, newindex=None):
        return self.tk.call(self._w, 'current', newindex)

    def set(self, value):
        return self.tk.call(self._w, 'set', value)