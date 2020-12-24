# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/pbar/tty_pbar.py
# Compiled at: 2016-07-25 14:36:49
"""Progress bar (TTY version)"""
import sys, os

class ttyProgressBar:
    """
      Simple progress indicator - displays bar "graph" using standard tty
      commands - space, backspace, etc. This method is compatible with
      (almost) all UNIX consoles and DOS boxes.

      Example:

         ====------  42%

      This is a "bar" (width 10 chars) for 42%

      Certainly, to use it nicely, do not write anything on screen
      (to stdout or stderr), while using it (or use erase()/redraw() methods).
      Erase or delete it after using.
   """
    left_c = '#'
    right_c = '_'
    space_c = ' '
    back_c = chr(8)
    if os.name == 'dos' or os.name == 'nt':
        left_c = chr(178)
        right_c = chr(176)

    def __init__(self, min, max, out=sys.stderr, width1=10, width2=5):
        self.min = min
        self.current = min
        self.max = max - min
        self.width1 = width1
        self.width2 = width2
        self.out = out
        self.redraw()

    def __del__(self):
        self.erase()

    def display(self, current):
        """
         Draw current value on indicator.
         Optimized to draw as little as possible.
      """
        self.current = current
        current -= self.min
        lng = current * self.width1 // self.max
        if current >= self.max:
            percent = 100
        else:
            percent = current * 100 // self.max
        flush = False
        if self.lng != lng:
            self.lng = lng
            self.out.write(ttyProgressBar.back_c * (self.width1 + self.width2))
            self.out.write(ttyProgressBar.left_c * lng)
            self.out.write(ttyProgressBar.right_c * (self.width1 - lng) + ttyProgressBar.space_c)
            self.percent = -1
            flush = True
        elif self.percent != percent:
            self.out.write(ttyProgressBar.back_c * (self.width2 - 1))
            flush = True
        if self.percent != percent:
            self.percent = percent
            self.out.write(str(percent).rjust(3) + '%')
            flush = True
        if flush:
            self.out.flush()
        self.visible = True

    def erase(self):
        if self.visible:
            self.out.write(ttyProgressBar.back_c * (self.width1 + self.width2))
            self.out.write(ttyProgressBar.space_c * (self.width1 + self.width2))
            self.out.write(ttyProgressBar.back_c * (self.width1 + self.width2))
            self.out.flush()
            self.visible = False

    def redraw(self):
        self.lng = -1
        self.percent = -1
        self.out.write(ttyProgressBar.space_c * (self.width1 + self.width2))
        self.display(self.current)