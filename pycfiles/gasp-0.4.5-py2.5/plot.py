# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/input/plot.py
# Compiled at: 2007-10-25 10:12:01
import os, gasp.testing
from gasp import *
wait = 0
begin_graphics()
p = Plot((100, 100))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(p)
p = Plot((100, 100), size=10)
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(p)
p = Plot((100, 100), color=(150, 100, 50))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(p)
p = Plot((100, 100), color=(50, 100, 150), size=10)
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(p)
end_graphics()