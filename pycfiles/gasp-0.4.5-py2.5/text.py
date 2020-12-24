# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/input/text.py
# Compiled at: 2007-10-25 10:12:01
import os, gasp.testing
from gasp import *
wait = 0
begin_graphics()
t = Text('Huston, we have a problem', (100, 100))
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(t)
t = Text('Huston, we have a problem', (100, 100), size=40)
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(t)
t = Text('Huston, we have a problem', (100, 100), color=(255, 0, 0), size=40)
gasp.testing.grab_screen()
sleep(wait)
remove_from_screen(t)
end_graphics()