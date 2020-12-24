# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/head_controller/KeyLogger.py
# Compiled at: 2019-10-26 18:23:54
# Size of source mod 2**32: 206 bytes
import curses
while 1:
    c = stdscr.getch()
    if c == ord('p'):
        PrintDocument()
    elif c == ord('q'):
        break
    elif c == curses.KEY_HOME:
        x = y = 0