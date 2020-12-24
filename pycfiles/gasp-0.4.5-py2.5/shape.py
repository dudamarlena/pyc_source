# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/input/shape.py
# Compiled at: 2007-10-25 10:12:01
import os, gasp.testing
from gasp import *
wait = 0
begin_graphics()
b = Box((100, 100), 200, 200, filled=True)
gasp.testing.grab_screen()
sleep(wait)
move_to(b, (200, 200))
gasp.testing.grab_screen()
sleep(wait)
move_by(b, 100, 100)
gasp.testing.grab_screen()
sleep(wait)
move_by(b, -100, -100)
gasp.testing.grab_screen()
sleep(wait)
rotate_to(b, 30)
gasp.testing.grab_screen()
sleep(wait)
rotate_by(b, 70)
gasp.testing.grab_screen()
sleep(wait)
rotate_by(b, -40)
gasp.testing.grab_screen()
sleep(wait)
end_graphics()