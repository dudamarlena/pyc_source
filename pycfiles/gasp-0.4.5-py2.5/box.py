# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/input/box.py
# Compiled at: 2007-10-25 10:12:01
import os, gasp.testing
from gasp import *
wait = 0
begin_graphics()
b = Box((100, 100), 200, 200)
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(b)
b = Box((100, 100), 200, 200, filled=True, color=(50, 100, 150))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(b)
b = Box((100, 100), 200, 200, color=(150, 100, 50), thickness=5)
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(b)
end_graphics()