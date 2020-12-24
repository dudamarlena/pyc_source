# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CSpinBox.py
# Compiled at: 2012-04-13 00:17:33
__doc__ = '\nCreated on Mar 13, 2012\n\n@author: bkraus\n'
from Tkinter import Spinbox
from gui.cGui.config.GuiConfig import getBackgroundColor

class CSpinBox(Spinbox):
    """
    Extension of Tkinter.Spinbox
    """

    def __init__(self, master, **cnf):
        Spinbox.__init__(self, master, cnf)
        self.config(highlightbackground=getBackgroundColor())