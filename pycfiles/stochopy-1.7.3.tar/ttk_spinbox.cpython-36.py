# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\stochopy\gui\ttk_spinbox.py
# Compiled at: 2018-02-07 04:11:40
# Size of source mod 2**32: 635 bytes
"""
Add Spinbox widget to ttk (better looking themes).

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import sys
if sys.version_info[0] < 3:
    import ttk
else:
    import tkinter.ttk as ttk
__all__ = [
 'Spinbox']

class Spinbox(ttk.Entry):

    def __init__(self, master=None, **kwargs):
        (ttk.Entry.__init__)(self, master, 'ttk::spinbox', **kwargs)

    def current(self, newindex=None):
        return self.tk.call(self._w, 'current', newindex)

    def set(self, value):
        return self.tk.call(self._w, 'set', value)