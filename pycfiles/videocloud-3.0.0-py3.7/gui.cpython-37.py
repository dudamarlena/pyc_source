# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\videocloud\gui.py
# Compiled at: 2019-07-22 17:51:18
# Size of source mod 2**32: 284 bytes
import tkinter as tk
master = tk.Tk()
master.geometry('600x300')
tk.Label(master, text='Video URL').grid(row=0)
tk.Label(master, text='Font').grid(row=1)
e1 = tk.Entry(master)
e2 = tk.Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
master.mainloop()