# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/input/line.py
# Compiled at: 2007-10-25 10:12:01
import os, gasp.testing
from gasp import *
wait = 0
begin_graphics()
l = Line((0, 0), (100, 100))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(l)
l = Line((0, 0), (100, 100), color=(0, 255, 0))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(l)
l = Line((0, 100), (100, 100))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(l)
l = Line((100, 0), (100, 100))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(l)
l = Line((100, 0), (0, 100))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(l)
end_graphics()