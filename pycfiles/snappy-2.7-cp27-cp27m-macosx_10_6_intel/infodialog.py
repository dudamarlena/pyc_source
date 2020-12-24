# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/infodialog.py
# Compiled at: 2017-06-01 15:41:21
from __future__ import unicode_literals
import sys, os, datetime
if sys.version_info[0] < 3:
    import Tkinter as Tk_
    from tkSimpleDialog import Dialog
    import ttk
else:
    import tkinter as Tk_
    from tkinter.simpledialog import Dialog
    from tkinter import ttk
from .version import version as SnapPy_version
from IPython import __version__ as IPython_version
snappy_path = os.path.dirname(__file__)
icon_file = os.path.join(snappy_path, b'info_icon.gif')

class InfoDialog(Dialog):

    def __init__(self, master, title=b'', content=b''):
        self.content = content
        self.style = ttk.Style(master)
        if sys.platform == b'darwin':
            self.bg = b'SystemDialogBackgroundActive'
        else:
            self.bg = self.style.lookup(b'Button', b'background')
        self.image = Tk_.PhotoImage(file=icon_file)
        Dialog.__init__(self, master, title=title)

    def body(self, master):
        self.config(bg=self.bg)
        self.resizable(False, False)
        box = Tk_.Frame(self, bg=self.bg)
        icon = Tk_.Label(box, image=self.image, bg=self.bg)
        icon.pack(side=Tk_.LEFT, pady=30, anchor=Tk_.N)
        message = Tk_.Message(box, text=self.content, bg=self.bg)
        message.pack(side=Tk_.LEFT, padx=20, pady=10)
        box.pack()

    def buttonbox(self):
        box = Tk_.Frame(self, bg=self.bg)
        button = ttk.Button(box, text=b'OK', width=5, command=self.ok, default=Tk_.ACTIVE)
        button.pack(side=Tk_.RIGHT, ipadx=10, padx=20, pady=20)
        self.bind(b'<Return>', self.ok)
        box.pack(anchor=Tk_.E)


about_snappy_text = b'\nFor information on how to use SnapPy, please see the Help menu.\n\nSnapPy is a program for studying the topology and geometry of 3-manifolds, with a focus on hyperbolic structures. It was written by Marc Culler, Nathan Dunfield, Matthias Gӧrner, and Jeff Weeks, with additional contributions by many others.  Its homepage is\n\n     http://snappy.computop.org/\n\nThis is version %s of SnapPy, running on Python %s using Tk %s and IPython %s.\n\nDevelopment of SnapPy was made possible in part by generous support from the National Science Foundation of the United States.\n\nSnapPy is copyright © 2009-%d by Marc Culler, Nathan Dunfield, Matthias Gӧrner, Jeff Weeks, and others and is distributed under the GNU Public License, version 2 or later.  \n' % (SnapPy_version,
 sys.version.split()[0],
 Tk_.Tcl().eval(b'info patchlevel'),
 IPython_version,
 datetime.datetime.now().year)

def about_snappy(window):
    InfoDialog(window, b'About SnapPy', about_snappy_text)


if __name__ == b'__main__':
    root = Tk_.Tk()
    info = InfoDialog(root, title=b'About SnapPy', content=about_snappy_text)