# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/gui/manual_gui_tests.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Feb 8, 2010
Works on Ubuntu and OSX

@author: brianthorne
"""
from Tkinter import *
from ttk import *
from os import walk, path
import re, logging
logging.basicConfig(level=logging.DEBUG)
logging.info('GUI test module loaded, logging enabled')
PATH_TO_SCRIPT = path.dirname(path.realpath(__file__))
EXAMPLES_DIRECTORY = path.split(PATH_TO_SCRIPT)[0]

def go(*args):
    print 'Going'


from codegroup import make_tree, fill_tree, ExamplesGroup
if __name__ == '__main__':
    root = Tk()
    root.title('TreeView Test')
    mainframe = Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    entry = Entry(mainframe, width=7)
    entry.grid(column=2, row=1, sticky=(W, E))
    Button(mainframe, text='Do Something', command=go).grid(column=3, row=3, sticky=W)
    Label(mainframe, text='Testing Treeview').grid(column=1, row=4)
    import os
    src_dir = os.path.normpath(__file__ + '../../../')
    actor_dir = os.path.join(src_dir, 'actors')
    ExamplesGroup('Actors', mainframe, actor_dir, (go, go))
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    entry.focus()
    root.bind('<Return>', go)
    root.mainloop()