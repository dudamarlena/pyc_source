# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/pbar.py
# Compiled at: 2018-03-22 15:26:32
try:
    from m_lib.pbar.tty_pbar import ttyProgressBar
except ImportError:
    ttyProgressBar = None

if ttyProgressBar:

    class ml_ttyProgressBar(object):

        def __init__(self, width=20):
            self.max = None
            self.pbar = None
            self.width = width
            return

        def set_max(self, max_value):
            self.max = max_value
            self.pbar = ttyProgressBar(0, max_value, width1=self.width)

        def display(self, value):
            if self.pbar:
                self.pbar.display(value)

        def close(self):
            if self.pbar:
                self.pbar.erase()
                self.pbar = None
            return