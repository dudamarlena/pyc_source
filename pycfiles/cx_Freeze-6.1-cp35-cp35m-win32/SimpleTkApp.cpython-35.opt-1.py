# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\Tkinter\SimpleTkApp.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 178 bytes
from tkinter import Tk, Label, Button, BOTTOM
root = Tk()
root.title('Button')
Label(text='I am a button').pack(pady=15)
Button(text='Button').pack(side=BOTTOM)
root.mainloop()