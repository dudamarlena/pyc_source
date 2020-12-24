# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\Tkinter\SimpleTkApp.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 178 bytes
from tkinter import Tk, Label, Button, BOTTOM
root = Tk()
root.title('Button')
Label(text='I am a button').pack(pady=15)
Button(text='Button').pack(side=BOTTOM)
root.mainloop()